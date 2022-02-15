from odoo import models , fields,api
from datetime import date
from odoo.exceptions import ValidationError
import re

class ItiPatient(models.Model):
    _name = 'hms.patient'
    _rec_name="First_name"
    state = fields.Selection([
        ('Undetermined', 'Undetermined'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Serious', 'Serious'),
        ],default='Good')

    First_name=fields.Char()
    Last_name=fields.Char()
    birth_date=fields.Date()
    history=fields.Html()
    CR_ratio=fields.Float()
    Blood_type=fields.Selection([
        ('a','A'),('b','B'),('o','O'),('ab','AB')
        
        ])
    PCR=fields.Boolean()
    Image=fields.Image()
    Address=fields.Text()
    age=fields.Integer(compute='_calc_age')
    departments_id=fields.Many2one('hms.departments')
    doctor_id=fields.Many2many('hms.doctors','doctor_patient')
    Capacity=fields.Integer(related="departments_id.Capacity")
    crm_ids = fields.One2many('res.partner', 'related_patient_id')
    Email = fields.Char()
    website=fields.Char(related="crm_ids.website")
    logs_history = fields.One2many(comodel_name="hms.logs", inverse_name="patient_id")


    @api.onchange('birth_date')
    def _onchange(self):
        if self.birth_date:
            self.age=date.today().year-self.birth_date.year
        else:
            self.birth_date=date.today()

    @api.onchange('age')
    def _on_age_change(self):
        if self.age < 30:
            self.PCR = True
            return{
                'warning':{"title":"alert","message":"pcr is checked"}
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
                raise ValidationError('Please,Enter a valid mail.')


    def _calc_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age=date.today().year - rec.birth_date.year
                pass
            else:
                rec.birth_date="2020-10-10"  
                

    # @api.model
    # def create(self,vals_list):
    #     vals_list['Email']=vals_list['First_name']+'@gmail.com'
    #     res=super().create(vals_list)
    #     return res

    _sql_constraints=[
        ('email_unique_constraint','UNIQUE(Email)','Email already exists')
    ]
    def Undetermined(self):
        self.state='Undetermined'
        self.env['hms.logs'].create({
            'description': f'State changed to {self.state}',
            'patient_id': self.id
        })

    def Good(self):
        self.state = 'Good'
        self.env['hms.logs'].create({
            'description': f'State changed to {self.state}',
            'patient_id': self.id
        })

    def Fair(self):
        self.state = 'Fair'
        self.env['hms.logs'].create({
            'description': f'State changed to {self.state}',
            'patient_id': self.id
        })

    def Serious(self):
        self.state = 'Serious'
        self.env['hms.logs'].create({
            'description': f'State changed to {self.state}',
            'patient_id': self.id
        })

    @api.model
    def create(self, vals_list):
        record = super().create(vals_list)
        self.env['hms.logs'].create({
            'description': 'Created Patient',
            'patient_id': record.id
        })
        return record