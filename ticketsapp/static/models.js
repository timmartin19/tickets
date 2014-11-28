/**
 * Created by Tim Martin on 11/28/14.
 */
Tickets.Ticket = DS.Model.extend({
    client: DS.belongsTo('user', {
        inverse: 'client_tickets',
        async: true
    }),
    consultant: DS.belongsTo('user',{
        inverse: 'consultant_tickets',
        async: true
    }),
    title: DS.attr('string'),
    description: DS.attr('string'),
    due_date: DS.attr('date'),
    date_submitted: DS.attr('date'),
    last_updated: DS.attr('date'),
    status: DS.attr('string'),
    progress_report: DS.attr('string'),
    finished: DS.attr('boolean'),
    shortTitle: function(){
        if(this.get('title').length >= 23){
            return this.get('title').substr(0, 20) + '...';
        }else{
            return this.get('title');
        }
    }.property('title')
});

Tickets.User = DS.Model.extend({
    client_tickets: DS.hasMany('ticket', {
        async: true
    }),
    consultant_tickets: DS.hasMany('ticket', {
        async: true
    }),
    username: DS.attr('string'),
    first_name: DS.attr('string'),
    last_name: DS.attr('string'),
    fullName: function(){
        return this.get('first_name') + " " + this.get('last_name');
    }.property('first_name', 'last_name')
});