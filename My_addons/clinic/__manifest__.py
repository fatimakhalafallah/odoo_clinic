 # -*- coding: utf-8 -*-
{
    'name' : 'clinic',
    'versiqon' : '1.1',
    'summary': 'clinic erp system',
    'sequence': 10,
    'description': """
        manage patient, 
        doctors and
        Patient dormitory data
     """,
    'category': 'Health',
    'author': 'Fatima',
    'website': '',
    'images' : [],
    'depends' : ['base'],
    'data': [
    'security/ir.model.access.csv',
    'views/clinic_patient_view.xml',
    'views/clinic_doctor_view.xml',
    'views/clinic_booking_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'active': True,
}