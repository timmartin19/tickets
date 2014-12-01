/**
 * Created by Tim Martin on 11/28/14.
 */


Tickets.TicketContainerComponent = Ember.Component.extend({});

Tickets.TicketsTableComponent = Ember.Component.extend({
    viewableTickets: function(){
        var ticketsTableComponent = this;
        var ticketsToDisplay = this.get('tickets').filter(function(ticket, index, self) {
            if (!ticket.get('finished') || ticketsTableComponent.get('viewFinished')) { return true; }
        });
        return  Ember.ArrayController.create({
            model: ticketsToDisplay,
            sortProperties: [ticketsTableComponent.get('sortProperty')],
            sortAscending: ticketsTableComponent.get('sortAscending')
        });
    }.property('tickets', 'viewFinished', 'sortProperty', 'sortAscending'),
    actions: {
        sortBy: function(property){
            if(this.get('sortProperty') == property) {
                this.set('sortAscending', !this.get('sortAscending'));
            }
            this.set('sortProperty', property);
        }
    },
    viewFinished: false,
    sortProperty: ['due_date'],
    sortAscending: false
});

Tickets.DateField = Ember.TextField.extend({
    picker: null,
    updateValue: function() {
        var date = moment(this.get("date"));
        if (date.isValid()) {
            this.set("value", date.format("L"));
            this.get("picker").setDate(date.format("L"));
        } else {
            this.set("value", null);
        }
    }.observes("date"),
    updateDate: function() {
        var date = moment(this.get("value"));
        if (date.isValid()) {
            this.set("date", date.toDate());
        } else {
            this.set("date", null);
        }
    }.observes("value"),
    didInsertElement: function() {
        var picker = new Pikaday({
            field: this.$()[0],
            format: "MM/DD/YYYY"
        });
        this.set("picker", picker);
        this.updateValue();
    },
    willDestroyElement: function(){
        var picker = this.get("picker");
        if (picker) {
            picker.destroy();
        }
        this.set("picker", null);
    }
});