odoo.define("nano_custom_chart.form_view", function(require) {
    "use strict";

    var FormView = require("web.FormView");
    FormView.include({

        load_record: function(record) {
            var self = this;
            self._super.apply(this, arguments);
            if (self.model == 'res.partner') {
                this.append_org_chart(record);
            };
        },

        append_org_chart: function(record) {
            var self = this;
            var record_id = record.id;
            var partner = 'partner="' + record_id + '">';
            var $new_div = $('<div id="people" ' + partner);

            var $peopleDiv = self.$el.find('#people');
            var $formSheet = self.$el.find('.o_form_sheet');
            if (!$peopleDiv.length) {
                $peopleDiv = $new_div;
                $peopleDiv.appendTo($formSheet);
            } else if (record_id != $peopleDiv.attr('partner')) {
                $peopleDiv.replaceWith($new_div);
            };
        },

    });
});