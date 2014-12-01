/**
 * Created by Tim Martin on 11/28/14.
 */
Tickets.BaseController = Ember.ObjectController.extend({
    clients: function(){
        if(this.get('model.is_staff') == true){
            return this.get('store').find('user', { is_staff: false});
        }else{
            return [];
        }
    }.property('store'),
    consultants: function(){
        return this.get('store').find('user', { is_staff: true });
    }.property('store')
});

Tickets.TicketsController = Ember.ArrayController.extend({
    needs: ['base'],
    actions: {
        createNewTicket: function(title, client, consultant, dueDate, description){
            if(!title || !consultant || !dueDate) {return false;}
            if(!title.trim()){return false;}
            if(client == null){ client=this.get('controllers.base.model'); }

            var newTicket = this.get('store').createRecord('ticket', {
                title: title,
                client: client,
                consultant: consultant,
                due_date: dueDate,
                description: description,
                status: 'not started'
            });
            newTicket.save();
        }
    }
});

Tickets.TicketController = Ember.ObjectController.extend({
    needs: ['base', 'tickets'],
    actions: {
        edit: function(){
            this.set('editing', true);
        },
        save: function(){
            this.set('editing', false);
            this.get('model').save();
        }
    },
    statusOptions: ['not started', 'in progress', 'finished'],
    editing: false,
    editingAndStaff: function(){
        return (this.get('editing') && this.get('controllers.base.model.is_staff'));
    }.property('editing', 'controller.base.model.is_staff')
});

Tickets.UsersController = Ember.ArrayController.extend({
    needs: ['base'],
    actions: {
        createNewUser:function(username, firstName, lastName, email, isStaff){
            if(!this.get('controllers.base.model.is_superuser')){return;}
            if(!username || !firstName || !lastName || !email){
                this.set('formError', true);
                return false;
            }else if(!username.trim() || !firstName.trim() || !lastName.trim() || !email.trim()){
                this.set('formError', true);
                return false;
            }
            var newUser = this.get('store').createRecord('user', {
                username: username,
                first_name: firstName,
                last_name: lastName,
                email: email,
                is_staff: isStaff
            });
            var self = this;
            newUser.save().then(function(nu){
                self.send('resetForm');
            }, function(){
                self.set('formError', true);
            })
        },
        resetForm: function(){
            this.set('newUserUsername', '');
            this.set('newUserFirstName', '');
            this.set('newUserLastName', '');
            this.set('newUserEmail', '');
            this.set('newUserIsStaff', false);
            this.set('formError', false);
            $('#newUserModal').modal('hide');
        }
    },
    formError: false
});

Tickets.UserController = Ember.ObjectController.extend({
    needs: ['base'],
    actions: {
        saveUser: function(){
            if(!this.get('controllers.base.model.is_superuser')){return;}
            this.get('model').save();
        }
    }
});