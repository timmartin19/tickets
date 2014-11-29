__author__ = 'Tim Martin'
from fabric.api import run, local, env, cd, settings, put, hide, get, lcd
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
domain = 'martin-consulting.org'
webapp_path = '/home/%s/webapps/%s_app/%s_app' % (webfaction_account_name, project_name, project_name)
db_password = '90mjQgWhZn'
virtual_env_wrapper = '~/bin/virtualenvwrapper.sh'
venv_name = '{0}_venv'.format(project_name)

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


def pack():
    local('git archive --format zip master --output=%s.zip' % project_name, capture=False)


def create_virtual_environment():
    with cd(webapp_path):
        run('virtualenv-2.7 {0}'.format(venv_name))


@run_in_local_dir
def deploy():
    # local("pip freeze > requirements.txt -f 'http://vkpypi:8EWash!@pypi.vkspider.com/packages'")
    pack()
    put('%s.zip' % project_name, '/home/%s/' % webfaction_account_name)
    with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
        run('unzip -o /home/%s/%s.zip -d %s' % (webfaction_account_name, project_name, webapp_path))

    with cd(webapp_path):
        print(webapp_path)
        with virtualenv(venv_name):
            run('pip install -r requirements.txt')
    deploy_settings()
    restart_apache()
    run('rm /home/%s/%s.zip' % (webfaction_account_name, project_name))

@run_in_local_dir
def deploy_settings():
    put('settings.py', os.path.join(webapp_path, 'oauthapp'))
    put('index.py', '/home/vkstage/webapps/{0}_app/htdocs'.format(project_name))


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
    static_path = '/home/%s/webapps/%s_app/%s_app/oauthapp/static/' % (
        webfaction_account_name, project_name, project_name)
    print static_path
    server.create_app(session_id, "%s_static" % project_name, 'symlink', False, static_path)
    print "creating website..."
    server.create_website(session_id, "%s_website" % project_name, server_ip, False, [domain],
                          ['%s_app' % project_name, '/'], ['%s_static' % project_name, '/media'])
    print "creating virtualenv..."
    create_virtual_environment()