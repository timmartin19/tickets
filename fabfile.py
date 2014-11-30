__author__ = 'Tim Martin'
from fabric.api import run, local, env, cd, settings, put, hide, get, lcd, prefix
from fabvenv import virtualenv
import fabfile_deets
import xmlrpclib
import os
from functools import wraps

env.hosts = fabfile_deets.hosts
env.user = fabfile_deets.user
env.password = fabfile_deets.password
server_ip = fabfile_deets.server_ip

webfaction_account_name = env.user
project_name = 'tickets'
app_name = 'ticketsapp'
domain = 'martin-consulting.org'
webapp_path = '/home/%s/webapps/%s_app/%s_app' % (webfaction_account_name, project_name, project_name)
db_password = '90mjQgWhZn'
virtual_env_wrapper = '~/bin/virtualenvwrapper.sh'
venv_name = '{0}'.format(project_name)
static_path = '/home/{0}/webapps/{1}_app/{1}_app/static_collected'.format(webfaction_account_name, project_name, app_name)

base_dir = os.path.dirname(os.path.abspath(__file__))


def run_in_local_dir(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        with lcd(base_dir):
            return f(*args, **kwargs)
    return wrapped


@run_in_local_dir
def get_logs():
    get('/home/{0}/logs/user/access_{1}_app.log*'.format(env.user, project_name))
    get('/home/{0}/logs/user/error_{1}_app.log*'.format(env.user, project_name))

@run_in_local_dir
def get_conf():
    get('/home/{0}/webapps/{1}_app/apache2/conf/httpd.conf'.format(webfaction_account_name, project_name))

@run_in_local_dir
def deploy_conf():
    put(os.path.join(base_dir, 'deployment', 'httpd.conf'),
        '/home/{0}/webapps/{1}_app/apache2/conf'.format(webfaction_account_name, project_name))
    put(os.path.join(base_dir, 'deployment', 'wsgi.py'),
        '/home/{0}/webapps/{1}_app/{1}_app/{2}'.format(webfaction_account_name, project_name, app_name))

@run_in_local_dir
def deploy_static():
    local('python manage.py bower install')
    local('python manage.py collectstatic')
    put(os.path.join(base_dir, 'static_collected'),
        '/home/{0}/webapps/{1}_app/{1}_app'.format(webfaction_account_name, project_name))


def pack():
    local('git archive --format zip master --output=%s.zip' % project_name, capture=False)


def create_virtual_environment():
    with cd(webapp_path):
        run('virtualenv-2.7 {0}'.format(venv_name))


@run_in_local_dir
def deploy():
    # local("pip freeze > requirements.txt -f 'http://vkpypi:8EWash!@pypi.vkspider.com/packages'")
    pack()
    put('{0}.zip'.format(project_name), '/home/{0}/'.format(webfaction_account_name))
    run('unzip -o /home/{0}/{1}.zip -d {2}'.format(webfaction_account_name, project_name, webapp_path))
    with cd(webapp_path):
        with prefix('workon {0}'.format(venv_name)):
            run('pip install -r requirements.txt')
    deploy_conf()
    deploy_settings()
    deploy_static()
    restart_apache()
    run('rm /home/{0}/{1}.zip'.format(webfaction_account_name, project_name))
    local('rm {0}.zip'.format(project_name))

@run_in_local_dir
def deploy_settings():
    put('{0}/production.py'.format(project_name),
        '/home/{1}/webapps/{0}_app/{0}_app/{0}'.format(project_name, webfaction_account_name))


def restart_apache():
    with cd(os.path.join(webapp_path, '..')):
        run('apache2/bin/restart')


def migrate_db():
    with cd(webapp_path):
        with virtualenv(venv_name):
            run('python runmanager.py db migrate')
            run('python runmanager.py db upgrade')


def create_webfaction_site():
    print "authenticating..."
    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login(env.user, env.password)
    print "creating domain..."
    server.create_domain(session_id, domain)
    print "creating app..."
    server.create_app(session_id, "%s_app" % project_name, 'mod_wsgi34-python27', False, '')
    print "creating media app..."
    server.create_app(session_id, "%s_static" % project_name, 'symlink', False, static_path)
    print "creating website..."
    server.create_website(session_id, "%s_website" % project_name, server_ip, False, [domain],
                          ['%s_app' % project_name, '/'], ['%s_static' % project_name, '/media'])
    print "creating virtualenv..."
    create_virtual_environment()