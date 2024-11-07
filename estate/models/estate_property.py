from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "A building or buildings and the land belonging to it or them."


	name = fields.Char(string='Title', required=True)
	description = fields.Text(string='Description')
	postcode = fields.Char(string='Postcode')
	date_availability = fields.Date(string='Available From', copy=False, default=fields.Date.add(fields.Date.today(),months=3)) #took me forever to figure out it's just months=3 for the 2nd argument GRRR!!
	expected_price = fields.Float(string='Expected Price', required=True)
	selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
	bedrooms = fields.Integer(string='Bedrooms', default=2)
	living_area = fields.Integer(string='Living Area (sqm)')
	facades = fields.Integer(string='Facades')
	garage = fields.Boolean(string='Garage')
	garden = fields.Boolean(string='Garden')
	garden_area = fields.Integer(string='Garden Area (sqm)')
	garden_orientation = fields.Selection(string='Garden Orientation', selection = [('north','North'),('south','South'),('east','East'),('west','West')])
	state = fields.Selection(string='Status', selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, default='new')
	active = fields.Boolean(default=True)
	
