# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Alquiler y Reservacion de Salones',
    'summary': 'Alquiler y Reservacion de Salones ',
    'category': 'Sales/CRM',
    'depends': ['crm'],
    'data': [
    	'security/crm_salon_security.xml',
        'security/ir.model.access.csv',
        'views/crm_salon_views.xml',

    ],
  
}
