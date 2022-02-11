from odoo import models , fields,api
from datetime import date




class ItiPatient(models.Model):
    _name = 'hms.patient'
    state = fields.Selection([
        ('Undetermined', 'Undetermined'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Serious', 'Serious'),
        ],default='Good')

    First_name=fields.Char()
    Last_name=fields.Char()
    Birth_date=fields.Date()
    history=fields.Html()
    CR_ratio=fields.Float()
    Blood_type=fields.Selection([
        ('a','A'),('b','B'),('o','O'),('ab','AB')
        
        ])
    PCR=fields.Boolean()
    Image=fields.Image()
    Address=fields.Text()
    Age=fields.Integer()
    departments_id=fields.Many2one('hms.departments')
    doctor_id=fields.Many2many('hms.doctors','doctor_patient')
    Capacity=fields.Integer(related="departments_id.Capacity")
    @api.onchange('Birth_date')
    def _onchange(self):
        if self.Birth_date:
            self.Age=date.today().year-self.Birth_date.year
            if self.Age <= 30:
                self.PCR = True
                return {
                    'warning': {
                        'title': 'Alert',
                        'message': 'PCR has been checked '
                    }

                }
    

    def Undetermined(self):
        self.state='Undetermined'
    def Good(self):
        self.state='Good'
    def Fair(self):
        self.state='Fair'
    def Serious(self):
        self.state='Serious'