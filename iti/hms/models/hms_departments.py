from odoo import models, fields


class ItiDepartments(models.Model):
    _name = 'hms.departments'
    _rec_name = 'name'
    name = fields.Char()
    Capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients_ids = fields.One2many('hms.patient', 'doctor_id')

