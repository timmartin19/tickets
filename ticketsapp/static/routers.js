/**
 * Created by Tim Martin on 11/28/14.
 */

Tickets.Router.map(function(){
    this.resource('tickets', {path: '/'}, function(){
        this.resource('ticket', {path: '/ticket/:ticketId'});
    });
});

Tickets.TicketsRoute = Ember.Route.extend({
    model: function(){
        return this.store.find('ticket');
    }
});

Tickets.TicketRoute = Ember.Route.extend({
    model: function(params){
        return this.store.find('ticket', params.ticketId);
    }
});