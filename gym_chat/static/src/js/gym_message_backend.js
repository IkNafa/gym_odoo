odoo.define('gym_chat.gym_message_backend', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ReportWidget = require('web.Widget');
    var rpc = require('web.rpc');


    var report_backend = Widget.extend(ControlPanelMixin, {
        // Stores all the parameters of the action.

        events: {
            'click .send': 'send_message',
            'click .chat_user': 'change_active_user',
        },
        init: function (parent, action) {
            this.action = action;
            this.actionManager = parent;
            this.given_context = {};
            this.odoo_context = action.context;
            this.controller_url = action.context.url;
            if (action.context.context) {
                this.given_context = action.context.context;
            }
            this.given_context.active_id = action.context.active_id ||
                action.params.active_id;
            this.given_context.model = action.context.active_model || false;
            this.given_context.ttype = action.context.ttype || false;
            return this._super.apply(this, arguments);
        },
        willStart: function () {
            return $.when(this.get_html());
        },
        set_html: function () {
            var self = this;
            var def = $.when();
            if (!this.report_widget) {
                this.report_widget = new ReportWidget(this, this.given_context);
                def = this.report_widget.appendTo(this.$el);
            }
            def.then(function () {
                self.report_widget.$el.html(self.html);
            });
        },
        start: function () {
            this.set_html();

            this.get_user_name();
            this.chat = this.$('.chat')[0]

            if(this.active_user){
                this.load_messages();
            }else{
                var input = this.$(".chat-text")[0];
                input.disabled= true;
            }

            this.$(`li[name=${this.active_user}]`).addClass("active")

            return this._super();
        },
        // Fetches the html and is previous report.context if any,
        // else create it
        get_html: function () {
            var self = this;
            var defs = [];
            return this._rpc({
                model: this.given_context.model,
                method: 'get_html',
                args: [self.given_context],
                context: self.odoo_context,
            })
                .then(function (result) {
                    self.html = result.html;
                    defs.push(self.update_cp());
                    return $.when.apply($, defs);
                });
        },
        // Updates the control panel and render the elements that have yet
        // to be rendered
        update_cp: function () {
            if (this.$buttons) {
                var status = {
                    breadcrumbs: this.actionManager.get_breadcrumbs(),
                    cp_content: {$buttons: this.$buttons},
                };
                return this.update_control_panel(status);
            }
        },
        do_show: function () {
            this._super();
            this.update_cp();
        },
        canBeRemoved: function () {
            return $.when();
        },
        
        send_message: function() {
            var message = this.$(".chat-text")[0];
            if(message.value == null || message.value == ""){
                return;
            }
            this.create_message(this.active_user,message.value);
            message.value = ''
        },

        create_message: function(to,message){
            var self = this;
            rpc.query({
                model: 'gym.message',
                method: 'create',
                args: [{
                    'to_id': to,
                    'message': message,
                }],
            }).then(() => {
                self.start();
            })
        },
        get_user_name: function(){
            var domain = [['id','=',this.odoo_context.uid]]
            var fields = ['name']
            var args = [domain, fields];
            var self = this;

            rpc.query({
                model: 'res.users',
                method: 'search_read',
                args: args
            }).then(function (result) {
                self.user_name = result[0].name
            });
        },
        change_active_user: function(ev){
            var currentTarget = ev.currentTarget;
            this.active_user = parseInt(currentTarget.getAttribute("name"));
            this.$(".chat_user").removeClass("active")
            currentTarget.classList.add("active");
            this.start();
        },
        load_messages: function(){
            var domain = ['|',['to_id','=',this.active_user],['from_id','=',this.active_user]]
            var fields = ['datetime','to_name','from_name','message']
            var args = [domain, fields];
            var self = this;

            rpc.query({
                model: 'gym.message',
                method: 'search_read',
                args: args
            }).then(function (result) {
                for(var message of result){
                    self.add_message(message);
                }
            });
        },

        add_message: function(message){
            var align = message.from_name == this.user_name? "right":"left";
            this.chat.innerHTML = `
            <li class="${align} clearfix">
                <div class="chat-body clearfix">
                    <div class="header">
                        <strong class="primary-font">${message.from_name}</strong>
                        <small class="pull-right text-muted"><i class="fa fa-clock-o"></i> ${message.datetime}</small>
                    </div>
                    <p>
                        ${message.message}
                    </p>
                </div>
            </li>` + this.chat.innerHTML
        }
    });

    core.action_registry.add(
        "gym_message_backend",
        report_backend
    );
    return report_backend;
});