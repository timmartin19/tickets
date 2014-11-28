/**
 * Created by Tim Martin on 11/28/14.
 */
window.Tickets = Ember.Application.create();

Tickets.ApplicationAdapter = DS.RESTAdapter.extend({
    namespace: 'api',
    plurals: {
        ticket: 'ticket',
        user: 'user'
    }
});

Ember.Inflector.inflector.uncountable('ticket');
Ember.Inflector.inflector.uncountable('user');

Tickets.TicketSerializer = DS.RESTSerializer.extend({
    extract: function(store, type, payload, id, requestType){
        alert(JSON.stringify(payload));
        return payload;
    }
});

Tickets.UserSerializer = DS.RESTSerializer.extend({
    extract: function(store, type, payload, id, requestType){
        return {user: payload};
    }
});