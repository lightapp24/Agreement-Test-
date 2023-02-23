# -*- coding: utf-8 -*-

#  Copyright (c) 2023 Plotnikov S.E.
#  All rights reserved.
#

from odoo import api, fields, models


class Agreement(models.Model):
    """
    Agreement
    """

    _name = 'test.agreement'
    _order = 'number'
    _rec_name = 'number'

    number = fields.Char(required=True, readonly=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, tracking=True)
    kind_id = fields.Many2one('test.kind_agreement', string='Kind Of Agreement', required=True, tracking=True)
    start_date = fields.Date(required=True, tracking=True)
    end_date = fields.Date(required=True, tracking=True)
    author_id = fields.Many2one('res.users', string='Author', related='create_uid', tracking=True)

    state = fields.Selection([('draft', 'Draft'),
                             ('approval', 'Approval In Progress'),
                             ('active', 'Active'),
                             ('completed', 'Completed')],
                             default='draft', required=True, readonly=True, tracking=True)

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('uniq_number', 'unique(number)', "A Number Of Agreement already exists with this name."),
    ]

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('test.agreement.sequence')
        return super(Agreement, self).create(vals)

    def send_for_approval(self):
        self.ensure_one()
        if self.state == 'draft':
            self.state = 'approval'

    def send_for_revision(self):
        self.ensure_one()
        sudo_self = self.sudo()
        if sudo_self.state == 'approval':
            sudo_self.state = 'draft'
            # Отправка письма реализована с использованием queue_job,
            # это позволяет создать задачу в очереди на выполнение,
            # в данном конкретном случае можно было обойтись без создания задачи,
            # но хотелось более быстрого реагирования нажатия на кнопку
            self.with_delay().send_email()

    def send_email(self):
        self.ensure_one()
        sudo_self = self.sudo()
        template = sudo_self.env.ref('test_agreement.test_agreement_revision_msg')
        record_id = sudo_self.id
        template.send_mail(record_id, force_send=True)

    def approval(self):
        self.ensure_one()
        sudo_self = self.sudo()
        if sudo_self.state == 'approval':
            sudo_self.state = 'active'

    def set_as_completed(self):
        self.ensure_one()
        sudo_self = self.sudo()
        if sudo_self.state == 'active':
            sudo_self.state = 'completed'

    @api.model
    def move_old_record_to_completed(self):
        current_date = fields.Date.today()
        records = self.search([('state', '=', 'active'),('end_date','<',current_date)])

        for record in records:
            # Так же используется queue_job,
            # создается задача для каждой записи
            # и в зависимости от настроек системы может выполнятся параллельно
            record.with_delay().set_as_completed()
