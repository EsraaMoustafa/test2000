# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website
from collections import OrderedDict

FIELDS = ['id', 'parent_id', 'name', 'phone', 'mobile', 'email']
ADDITION = {
    'phone': "Phone: %s",
    'mobile': "Mobile: %s"
}

class Main(Website):

    @http.route(['/res_partner/get_org_chart/<int:partner_id>'],
                type='http', auth="public", website=True)
    def get_org_chart(self, partner_id=0):

        Model = request.env['res.partner'].sudo()
        partner_ids = Model.browse(partner_id)
        manager = partner_ids.parent_id
        partner_ids |= manager
        partner_ids |= Model.search([('parent_id', 'child_of', partner_id)])
        data_source = self.get_chart_data_source(partner_ids)

        data = {'dataSource': data_source,
                'customize': {manager.id: {"color": "darkred"},
                              partner_id: {"color": "teal"}},
                'expandToLevel': manager and 3 or 2
                }

        return json.dumps(data)

    def get_chart_data_source(self, partner_ids):
        baseUri = '/web/image/' + 'res.partner/'
        res = []
        for partner in partner_ids:
            partner_dict = OrderedDict()
            for field in FIELDS:
                field_value = None
                if field == "parent_id":
                    field_value = getattr(partner, field, None)
                    field_value = field_value and field_value.id or None
                elif field.endswith("id") and field != 'id':
                    field_value = getattr(partner, field, None)
                    field_value = field_value and field_value.name or ''
                else:
                    field_value = getattr(partner, field, None)

                field_value = field in ADDITION and field_value and (
                    ADDITION[field] % field_value) or field_value
                partner_dict[field] = field_value

            partner_dict['image'] = baseUri + str(partner.id) + '/image'
            res.append(partner_dict)
        return res




