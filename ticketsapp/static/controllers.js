/**
 * Created by Tim Martin on 11/28/14.
 */
Tickets.TicketController = Ember.ObjectController.extend({
    actions: {
        edit: function(){
            this.set('editing', true);
        },
        save: function(){
            this.set('editing', false);
            this.get('model').save();
        }
    },
    users: function(){
        return this.get('store').find('user');
    }.property('model'),
    statusOptions: ['not started', 'in progress', 'finished'],
    editing: false
});