/**
 * Created by Tim Martin on 11/28/14.
 */

Tickets.currentUser = $('meta[name="userId"]').attr('content');

Tickets.Router.map(function(){
    this.resource('base', {path: '/'}, function(){
        this.resource('tickets', {path: '/'}, function(){
            this.resource('ticket', {path: '/ticket/:ticketId'});
        });
        this.resource('users', {path: '/users'}, function(){
            this.resource('user', { path: '/:userId'});
        });
    });
});

Tickets.BaseRoute = Ember.Route.extend({
    model: function(){
        return this.store.find('user', Tickets.currentUser);
    }
});

Tickets.TicketsRoute = Ember.Route.extend({
    model: function(){
        return this.store.find('ticket');
    },
    actions: {
        loading: function(transition, originRoute) {
            $('#usersTabLink').removeClass('active');
            $('#ticketsTabLink').addClass('active');
            return true;
        }
    }
});

Tickets.TicketRoute = Ember.Route.extend({
    model: function(params){
        return this.store.find('ticket', params.ticketId);
    }
});

Tickets.UsersRoute = Ember.Route.extend({
    model: function(){
        return this.store.find('user');
    },
    actions: {
        loading: function(transition, originRoute) {
            $('#usersTabLink').addClass('active');
            $('#ticketsTabLink').removeClass('active');
            return true;
        }
    }
});

Tickets.UserRoute = Ember.Route.extend({
    model: function(params){
        return this.store.find('user', params.userId);
    }
});