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

    editing: false
});