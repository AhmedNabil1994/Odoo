from odoo import models, fields
from odoo.exceptions import UserError


class CrmInherit(models.Model):
    _inherit = 'crm.lead'
    test = fields.Char()
    related_patient_id = fields.Many2one('hms.patient', ondelete='restrict')

    def unlink(self):
        if len(self.related_patient_id) != 0 :
            raise UserError('can not delete ')
