# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ClinicBooking(models.Model):
    ###############################
    #Class for Booking data
    ###############################
    _name = 'clinic.booking'
    _description = "object contain all doctor data"

    state = fields.Selection([('draft','Draft'),('wait_d_meeting','Wait Doctor Meeting'),
        ('stay_on_ward','Stay On Ward'),('medical_bill','Medical Bill')], string='State', default='draft')
    patient_id = fields.Many2one('clinic.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('clinic.doctor', string='Doctor', required=True)
    date = fields.Date(string="Date", default=fields.date.today())
    meeting_date = fields.Date(string="Meeting Date", required=True)
    paid_fees = fields.Boolean(string="Paid Fees")
    note = fields.Html(string="Note")

    @api.one
    def action_to_wait_d_meeting(self):
        """
        function to be sure that the paient had registered to meet doctor
        """
        if self.paid_fees == False:
            raise ValidationError(_("The Patient did not paid fees yet !"))
        self.state = 'wait_d_meeting'
      


    @api.one
    def clinic_ward_action(self):
        """
        function will call if the doctor decied that the patient must stay for sometime in clinin's ward
        """
        self.patient_id.write({'met_doctor': True})
        self.patient_id.write({'last_meeting': self.meeting_date})
        self.state = 'stay_on_ward'
        

    @api.one
    def medical_bill_action(self):
        """
        function will call if the doctor give the patient a medical bill
        """
        self.patient_id.write({'met_doctor': True})
        self.patient_id.write({'last_meeting': self.meeting_date})
        self.state = 'medical_bill'
        