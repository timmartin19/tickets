/**
 * Created by Tim Martin on 11/28/14.
 */
window.Tickets = Ember.Application.create();

Tickets.ApplicationAdapter = DS.RESTAdapter.extend({
    namespace: 'api',
    plurals: {
        ticket: 'ticket',
        user: 'user'
    },
    serialize: function(record, options){
        var json = this._super(record, options);
        alert(JSON.stringify(json));
        return json
    }
});

Ember.Inflector.inflector.uncountable('ticket');
Ember.Inflector.inflector.uncountable('user');

Tickets.TicketSerializer = DS.RESTSerializer.extend({
    extract: function(store, type, payload, id, requestType){
        return payload;
    },
    extractSingle: function(store, type, payload, id){
        return {'ticket': payload};
    },
    serializeIntoHash: function(hash, type, record, options){
        var json = this.serialize(record, options);
        for(var key in json){
            if(json.hasOwnProperty(key)){
                hash[key] = json[key];
            }
        }
    }
});

Tickets.UserSerializer = DS.RESTSerializer.extend({
    extract: function(store, type, payload, id, requestType){
        return payload;
    },
    extractSingle: function(store, type, payload, id){
        return {user: payload};
    },
    serializeIntoHash: function(hash, type, record, options){
        var json = this.serialize(record, options);
        for(var key in json){
            if(json.hasOwnProperty(key)){
                hash[key] = json[key];
            }
        }
    }
});