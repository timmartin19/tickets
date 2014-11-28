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
    }.property('title'),
    formattedDueDate: function(){
        return moment(this.get('due_date')).format('MMM Do, YYYY')
    }.property('due_date'),
    formattedDateSubmitted: function(){
        return moment(this.get('date_submitted')).format('MMM Do, YYYY')
    }.property('date_submitted'),
    formattedLastUpdated: function(){
        return moment(this.get('last_updated')).format('MMM Do, YYYY')
    }.property('last_updated')
});

Tickets.User = DS.Model.extend({
    client_tickets: DS.hasMany('ticket', {
        inverse: 'client'
    }),
    consultant_tickets: DS.hasMany('ticket', {
        inverse: 'consultant'
    }),
    username: DS.attr('string'),
    first_name: DS.attr('string'),
    last_name: DS.attr('string'),
    is_superuser: DS.attr('boolean'),
    is_staff: DS.attr('boolean'),
    fullName: function(){
        return this.get('first_name') + " " + this.get('last_name');
    }.property('first_name', 'last_name')
});