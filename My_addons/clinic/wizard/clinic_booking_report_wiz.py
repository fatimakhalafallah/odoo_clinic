# -*- coding: utf-8 -*-
##############################################################

from odoo import fields, models, api, _
import time
from datetime import date
from odoo.exceptions import ValidationError ,UserError

class ClinicBookingWiz(models.TransientModel):
    _name = "clinic.booking.report.wiz"

    state = fields.Selection([('draft','Draft'),('wait_d_meeting','Wait Doctor Meeting'),('stay_on_ward','Stay On Ward'),('medical_bill','Medical Bill')], string='State')
    patient_id = fields.Many2one('clinic.patient', string='Patient')
    doctor_id = fields.Many2one('clinic.doctor', string='Doctor')
    date = fields.Date(string="Date")
    meeting_date = fields.Date(string="Meeting Date")

    @api.multi
    def print_booking_report(self):
        """
        This Function Get The Data For Booking Reports
        """
        booking_ids = self.env['clinic.booking'].search([])
        data = {}
        booking_list = []

        if self.state:
            for rec in booking_ids:
                if rec.state == self.state:
                    booking_list.append(rec.id)
            booking_ids = booking_ids.search([('id','in',booking_list)])
            booking_list = []

        if self.patient_id:
            for rec in booking_ids:
                if rec.patient_id == self.patient_id:
                    booking_list.append(rec.id)
            booking_ids = booking_ids.search([('id','in',booking_list)])
            booking_list = []  

        if self.doctor_id:
            for rec in booking_ids:
                if rec.doctor_id == self.doctor_id:
                    booking_list.append(rec.id)
            booking_ids = booking_ids.search([('id','in',booking_list)])
            booking_list = []

        if self.date:
            for rec in booking_ids:
                self_date = str(self.date)
                rec_date = str(rec.date)
                if self_date == rec_date:
                    booking_list.append(rec.id)
            booking_ids = booking_ids.search([('id','in',booking_list)])
            booking_list = []

        if self.meeting_date:
            for rec in booking_ids:
                self_meeting_date = str(self.meeting_date)
                rec_meeting_date = str(rec.meeting_date)
                if self_meeting_date == rec_meeting_date:
                    booking_list.append(rec.id)
            booking_ids = booking_ids.search([('id','in',booking_list)])
            booking_list = []

        for rec in booking_ids:
            booking_list.append(rec.id)
        data = {'booking_ids':booking_list}
        return self.env.ref('clinic.booking_custom_report_action').report_action(self, data=data)


class ClinicBookingReportDetails(models.AbstractModel):
    _name = "report.clinic.booking_custom_report_temp"

    @api.model
    def get_report_values(self, docids, data=None):
        booking_ids = self.env['clinic.booking'].search([('id','=',data['booking_ids'])])
        docids = docids
        # self.get_menus_skel(docids, data)
      
        return {
            'data': booking_ids
            }