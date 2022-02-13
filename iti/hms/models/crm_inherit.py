from odoo import models, fields
from odoo.exceptions import UserError


class CrmInherit(models.Model):
    _inherit = 'res.partner'
    related_patient_id = fields.Many2one('hms.patient')

    def unlink(self):
        if self.related_patient_id:
            raise UserError('can not delete ')
        return super().unlink()    
