# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from psycopg2 import sql, extras
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError
from odoo.addons.phone_validation.tools import phone_validation
from collections import OrderedDict




class CrmSalon(models.Model):
    """ Industry Tags of Acquisition Rules """
    _name = 'crm.salon'
    _rec_name='nombre_salon'

    name = fields.Char(string='Codigo',)
    nombre_salon = fields.Char('Nombre')
    state = fields.Selection([
        ('draft', 'Libre'),
        ('abonado', 'Abonado'),
        ('done', 'Reservado'),
    ], string="Estado Reservacion",default='draft')
    date_begin = fields.Datetime('Fecha Inicio', readonly=False)
    date_end = fields.Datetime('Fecha Fin', readonly=False)
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)
    capacidad = fields.Integer(string='Capacidad')


CrmSalon()


class CrmVendedor(models.Model):
    _name = 'crm.vendedor'

    name = fields.Char(string='Nombre Vendedor')
    correo = fields.Char('Correo')
    # state = fields.Selection([
    #     ('draft', 'Libre'),
    #     ('abonado', 'Abonado'),
    #     ('done', 'Reservado'),
    # ], string="Estado Reservacion",default='draft')
    # date_begin = fields.Datetime('Fecha Inicio', readonly=False)
    # date_end = fields.Datetime('Fecha Fin', readonly=False)
    # company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)
    # capacidad = fields.Integer(string='Capacidad')


CrmVendedor()


class CrmTipoVenta(models.Model):
    _name = 'crm.tipo.venta'

    name = fields.Char(string='Tipo Venta')
    genera_oportunidad = fields.Boolean('Genera Oportunidad?')
    dias_generacion = fields.Integer('Dias Generacion Oportunidad')



CrmTipoVenta()


    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', 'Tag name already exists!'),
    # ]

class Lead(models.Model):
    _inherit = "crm.lead"

    salon_id = fields.Many2one('crm.salon','Salon')
    mobile = fields.Char('Movil')
    partner_cumple_ids = fields.Many2one('res.partner','Cumpleañero')
    # media = fields.Char('Media')
    date_begin = fields.Datetime('Fecha Inicio', readonly=False)
    date_end = fields.Datetime('Fecha Fin', readonly=False)
    vendedor_id = fields.Many2one('crm.vendedor','Vendedor')
    tipo_venta = fields.Many2one('crm.tipo.venta','Tipo Venta')


    # @api.multi
    def view_reservations(self):
        # self.ensure_one()
        return {
            'name': 'Reservaciones',
            'type': 'ir.actions.act_window',
            'view_type': 'calendar',
            'view_mode': 'calendar',
            'res_model': 'crm.lead',
            'nodestroy' : True,
            'target' : 'current',
            # 'context' : context, 
            # 'res_id': self.id,
            # 'target': 'new',
        }


Lead()


class Partner(models.Model):

    _inherit = 'res.partner'

    edad = fields.Integer('Edad')
    fecha_nacimiento = fields.Date('Fecha de Nacimiento')
    
