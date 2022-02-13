from odoo import models , fields,api
from datetime import date
from odoo.exceptions import ValidationError
import re

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
    Age=fields.Integer(compute='_calc_age')
    departments_id=fields.Many2one('hms.departments')
    doctor_id=fields.Many2many('hms.doctors','doctor_patient')
    Capacity=fields.Integer(related="departments_id.Capacity")
    crm_ids = fields.One2many('res.partner', 'related_patient_id')
    Email = fields.Char()
    website=fields.Char(related="crm_ids.website")

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


    def match_regex(cls, user_input, pattern):
        if re.fullmatch(pattern, user_input):
            return True
        else:
            return False

    @api.constrains('Email')
    def _email_validation(self):
        if self.Email:
            if not self.match_regex(str(self.Email), r"[a-zA-z0-9]+\.[_a-z]+@[a-zA-z]+\.[a-zA-Z]+"):
                raise ValidationError('Please,Enter a vakid mail.')


    def _calc_age(self):
        for rec in self:
            rec.Age=date.today().year - rec.Birth_date.year

    # @api.model
    # def create(self,vals_list):
    #     vals_list['Email']=vals_list['First_name']+'@gmail.com'
    #     res=super().create(vals_list)
    #     return res

    _sql_constraints=[
        ('email_unique_constraint','UNIQUE(Email)','Email already exists')
    ]