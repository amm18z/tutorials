from odoo import fields, models

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "A building or buildings and the land belonging to it or them."

	name = fields.Char(string='name', required=True)
	description = fields.Text(string='description')
	postcode = fields.Char(string='[postcode')
	date_availability = fields.Date(string='date availability')
	expeceted_price = fields.Float(string='expeceted price', required=True)
	selling_price = fields.Float(string='selling price')
	bedrooms = fields.Integer(string='bedrooms')
	living_area = fields.Integer(string='living area')
	facades = fields.Integer(string='facades')
	garage = fields.Boolean(string='garage')
	garden = fields.Boolean(string='garden')
	garden_area = fields.Integer(string='garden area')
	garden_orientation = fields.Selection(string='orientation', selection = [('north','North'),('south','South'),('east','East'),('west','West')])