odoo.define('gym_surveys.form_controller', function(require) {
    'use strict';
    

    var Widget = require('web.AbstractField');
    var registry = require('web.field_registry');
    var rpc = require('web.rpc');

    var json_text_form = Widget.extend({
        "template": "json_text_form_template",
        events:{
            'click .custom_form_button': 'save_form_data',
        },

        start: function(){
            var options = this.nodeOptions;
            this.active_field = options.active_id
            this.target_field = options.target_field
            console.log(this.active_field)
            this._parseJSON();
        },

        _parseJSON: function(){

            var json_text = this.value;
            try{
                this.json = JSON.parse(json_text)
            }catch(error){
                this.do_warn('JSON error', error);
                return this.do_action({
                    type: 'ir.actions.act_window_close',
                    tag: "reload",
                });
            }

            for(var i=0; i<this.json.length; i++){
                let object = this.json[i];
                let id = object["id"]
                let title = object["title"]
                let required = object["required"]
                this._addField(id,title,required);
            }
            
        },

        _addField: function(id, title, required){
            var form = this.$el.find("form");
            form.append(`<label id=${id} for=${id}>${title}</label><br/>`);
            form.append(`<textarea name=${id} id=${id} ${required? "required":""}></textarea><br/>`)
        },

        save_form_data: function(e){
            this.$(".custom_form_button").disabled=true;
            var form = this.$el.find("form")[0];
            var formData = new FormData(form);
            var data = [];
            for (var key of formData.keys()){
                var value = formData.get(key);
                data = {
                    "question_id": parseInt(key),
                    "answer": value
                }
                this._create_answer(data)
            }
            var self = this;
            setTimeout(()=>{
                self.do_action({
                    type: 'ir.actions.client',
                    tag: 'reload',
                })
            }, 2500);

        },

        _create_answer: function(data){

            rpc.query({
                model: 'gym.survey.question.answer',
                method: 'create',
                args: [data],
            })
        }
    });

    registry.add('json_text_form', json_text_form);
    return json_text_form;

});