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

import time

import datetime

from datetime import datetime, date, time 




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
    dias_generacion = fields.Selection([('1', '1'),('2','2'),('3','3'),
        ('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),
        ('10','10'),('11','11'),('12','12')],string='Meses Generacion Oportunidad')



CrmTipoVenta()


class CrmTipoContacto(models.Model):
    _name = 'crm.tipo.contacto'

    name = fields.Char(string='Tipo Contacto')
    # genera_oportunidad = fields.Boolean('Genera Oportunidad?')
    # dias_generacion = fields.Integer('Dias Generacion Oportunidad')



CrmTipoContacto()


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
    usa_oportunidad = fields.Boolean('Usa oportunidad')


    @api.onchange('tipo_venta')
    def _onchange_tipo_venta(self):
        # hoy = date.today()
        if self.tipo_venta.genera_oportunidad == True:
            self.usa_oportunidad = True
        else:
            self.usa_oportunidad = False

            

    @api.model
    def genera_oprotunidad(self):
        # import pdb
        # pdb.set_trace()
        to_sync_items = self.search([('stage_id', 'in', (1,4))])
        values = {}
        for to_sync_item in to_sync_items:
            if to_sync_item.tipo_venta.genera_oportunidad == True:
                # fecha_evento = to_sync_item.date_begin
                fecha_evento_str = to_sync_item.date_begin.strftime('%Y-%m-%d')
                fecha_evento = datetime.strptime(fecha_evento_str,'%Y-%m-%d')
                anio = fecha_evento.year
                mes = fecha_evento.month
                mes_new = mes + int(to_sync_item.tipo_venta.dias_generacion)
                if mes_new > 12:
                    mes_new_cociente = mes_new // 12
                    mes_new_resto = mes_new % 12
                    if mes_new_resto == 0:
                        current_date=fecha_evento.replace(year=fecha_evento.year+mes_new_cociente, month=12)
                    else:
                        current_date=fecha_evento.replace(year=fecha_evento.year+mes_new_cociente, month=mes_new_resto)
                else:
                    current_date=fecha_evento.replace(month=mes_new)
                if current_date.strftime('%Y-%m-%d') == date.today().strftime('%Y-%m-%d'):
                    values['name'] = to_sync_item.name
                    values['partner_id'] = to_sync_item.partner_id.id
                    values['partner_cumple_ids'] = to_sync_item.partner_cumple_ids.id
                    values['vendedor_id'] = to_sync_item.vendedor_id.id
                    values['tipo_venta'] = to_sync_item.tipo_venta.id
                    values['salon_id'] = to_sync_item.salon_id.id
                    # values['date_begin'] = to_sync_item.date_begin
                    # values['date_end'] = to_sync_item.date_end
                    self.create(values)

                # fecha_evento_day = 

            # partner = to_sync_item.partner_id

            # params = {
            #     'partner_gid': partner.partner_gid,
            # }

            # if partner.vat and partner._is_vat_syncable(partner.vat):
            #     params['vat'] = partner.vat
            #     result, error = partner._rpc_remote_api('update', params)
            #     if error:
            #         _logger.error('Send Partner to sync failed: %s' % str(error))

            # to_sync_item.write({'synched': True})
    



    # def _onchange_partner_id_values(self, partner_id):
    #     """ returns the new values when partner_id has changed """
    #     if partner_id:
    #         partner = self.env['res.partner'].browse(partner_id)

    #         partner_name = partner.parent_id.name
    #         if not partner_name and partner.is_company:
    #             partner_name = partner.name

    #         return {
    #             'partner_name': partner_name,
    #             'contact_name': partner.name if not partner.is_company else False,
    #             'title': partner.title.id,
    #             'street': partner.street,
    #             'street2': partner.street2,
    #             'city': partner.city,
    #             'state_id': partner.state_id.id,
    #             'country_id': partner.country_id.id,
    #             'email_from': partner.email,
    #             'phone': partner.phone,
    #             'mobile': partner.mobile,
    #             'zip': partner.zip,
    #             'function': partner.function,
    #             'website': partner.website,
    #         }
    #     return {}



    # @api.model
    # def create(self, vals):
    #     import pdb
    #     pdb.set_trace()

    #     return super(Lead, self).create(vals)






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
    tipo_contacto = fields.Many2one('crm.tipo.contacto','Tipo Contacto')

    @api.onchange('fecha_nacimiento')
    def _onchange_fecha_nacimiento(self):
        hoy = date.today()
        if self.fecha_nacimiento:
            if hoy < self.fecha_nacimiento:
                self.edad = 0
                raise UserError(_('Erro en la Fecha de Nacimiento'))

            else:
                edad = date.today().year - self.fecha_nacimiento.year
            self.edad = edad

     


    # fecha_nacimiento

    # @api.model
    # def create(self, vals):
    #     import pdb
    #     pdb.set_trace()
    #     partner_cumple_ids = vals.get('partner_cumple_ids', '')
        # if partner_cumple_ids:
        #     vals['parent_id'] = self._get_tags_create_vals(tag_name, vals.get('country_id'))
        # return super(Partner, self).create(vals)
    

# class MassMailing(models.Model):
#     _inherit = "crm.lead"

#     salon_id = fields.Many2one('crm.salon','Salon')
#     mobile = fields.Char('Movil')
