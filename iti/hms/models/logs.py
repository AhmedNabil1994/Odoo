from odoo import models, fields


class Logs(models.Model):
    _name = 'hms.logs'
    _rec_name = 'description'

    patient_id = fields.Many2one(comodel_name="hms.patient")
    description = fields.Text()