# -*- coding: utf-8 -*-

#  Copyright (c) 2023 Plotnikov S.E.
#  All rights reserved.
#

from odoo import fields, models


class KindOfAgreement(models.Model):
    """
    Kind Of Agreement
    """

    _name = 'test.kind_agreement'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True, tracking=True)

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('uniq_name', 'unique(name)', "A Kind Of Agreement already exists with this name. Name must be unique!"),
    ]
