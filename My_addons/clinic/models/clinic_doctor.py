# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ClinicDoctor(models.Model):
    ###############################
    # Class for patient which is contain all patient data
    ###############################
    _name = 'clinic.doctor'
    _description = "object contain all patient data"

    first_name = fields.Char(string='First Name', required=True)
    second_name = fields.Char(string='Second Name', required=True)
    third_name = fields.Char(string='Third Name', required=True)
    forth_name = fields.Char(string='Fourth Name', required=True)
    name = fields.Char(string="Name", readonly=True, compute='get_patient_name')
    image = fields.Binary(string='Image', copy=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', default='male')
    birth_day = fields.Date(string='Birthday', required=True)
    age_year = fields.Integer(string="Years", compute='calculate_age')
    age_month = fields.Integer(string="Months", compute='calculate_age')
    age_day = fields.Integer(string="Days", compute='calculate_age')
    country_id = fields.Many2one('res.country',string='Country')
    phone = fields.Char(string="Phone")
    patient_ids=fields.One2many('clinic.patient','doctor_id',string="Patients")
    qualifications = fields.Html(string='Qualifications')
    specialty = fields.Char(string="Specialty")
    academic_degree=fields.Selection([('bachelor','Bachelor'),('master','Master'),('phd','PHD')],string='Academic Degree')
    university= fields.Char(string='University')
    graduate_year=fields.Date(string="Graduate Year")
    wait_d_booking=fields.Integer(string ="Booking Number" , compute="get_booking_number",readonly=True)
  
    


    @api.one
    def get_booking_number(self):
        """
        function to calculate the full nuber of avalialbe patient 
        """
        booking_ids  = self.env['clinic.booking'].search([('state','=','wait_d_meeting')])
        counter = 0 
        for rec in booking_ids:
            if rec.doctor_id==self:
                counter = counter + 1 

        self.wait_d_booking = counter  

    @api.multi
    def view_waiting_booking(self):
   
        booking_ids  = self.env['clinic.booking'].search([('state','=','wait_d_meeting')])
        
        booking = []

        for rec in booking_ids:
            if rec.doctor_id == self:
               booking.append(rec.id) 

        return{

            'name': _('ClinicBooking'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'clinic.booking',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id','in',booking)],
        }    

        
    @api.one
    def get_patient_name(self):
        """
        function to calculate the full name for the patient
        """
        self.name = self.first_name + ' ' + self.second_name + ' ' + self.third_name + ' ' + self.forth_name

    @api.constrains('phone')
    def phone_validation(self):

        phone_prefix=[1,9]
        phone_type=[1,0,9,2,6]
        check_value = 0

        if self.phone and self.country_id:
            if self.country_id.code == 'SD':
                phone= self.phone
                if len(phone)!= 9:
                    raise ValidationError(_("wrong Phone nunber, wrong length"))
                if len(phone)== 9:
                    for i in range(0,len(phone_prefix)):
                        if phone[0] == str(phone_prefix[i]):
                             check_value = 1
                    if check_value == 0:
                            raise ValidationError(_("Wrong phone , wrong key number"))
                    check_value = 0 
                    for i in range(0,len(phone_type)):
                         if phone[1]== str(phone_type[i]):
                             check_value = 1
                    if check_value == 0:
                            raise  ValidationError(_("wrong phone number,It is not real phone number"))
                    check_value = 0              
                    for i in range(0,len(phone)):
                        check_value = 0 
                        for j in range(0,10):
                            if phone[i] == str(j):
                                check_value = 1
                        if check_value == 0:
                            raise ValidationError(_(" Wrong number,Please dont enter Charcter"))                    

    @api.one
    def calculate_age(self):
        
        if self.birth_day :
            birth_day = str(self.birth_day)
            current_date = str(fields.Date.today())

            birth_day_year_as_int = int(birth_day[0] + birth_day[1] + birth_day[2] + birth_day[3])
            birth_day_month_as_int = int(birth_day[5] + birth_day[6])
            birth_day_day_as_int = int(birth_day[8] + birth_day[9])

            current_date_year_as_int = int(current_date[0] + current_date[1] + current_date[2] + current_date[3])
            current_date_month_as_int = int(current_date[5] + current_date[6])
            current_date_day_as_int = int(current_date[8] + current_date[9])

            period_years = current_date_year_as_int - birth_day_year_as_int
            period_months = current_date_month_as_int - birth_day_month_as_int
            period_days = current_date_day_as_int - birth_day_day_as_int

            months_list_1 = ['04', '06', '09', '11']
            months_list_2 = ['01', '03', '05', '07', '08', '10', '12']

            if period_days < 0:
                if str(current_date_month_as_int) == '02':
                    if current_date_year_as_int % 4 == 0:
                        period_days = 29 + period_days
                    if current_date_year_as_int % 4 != 0:
                        period_days = 28 + period_days
                for index in range(0, 4):
                    if current_date_month_as_int == int(months_list_1[index]):
                        period_days = 30 + period_days
                for index in range(0, 7):
                    if current_date_month_as_int == int(months_list_2[index]):
                        period_days = 31 + period_days
                period_months = period_months - 1
            if period_months < 0:
                period_months = 12 + period_months
                period_years = period_years - 1

            self.age_year = period_years
            self.age_month = period_months
            self.age_day = period_days




   

    




















































