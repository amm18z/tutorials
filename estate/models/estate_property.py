from odoo import api, fields, models, exceptions

class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "A building or buildings and the land belonging to it or them."
	_sql_constraints = [('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price should be strictly positive.'),
						('check_selling_price_positive', 'CHECK(selling_price > 0)', 'The selling price should strictly positive.')]
	_order = 'id desc' # Where is "id" coming from? it's not a field on the model... field automatically created when estate_property relation is created? by whom? psql? or the ORM layer?


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
	state = fields.Selection(string='Status', selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], copy=False, default='new', readonly=True)
	active = fields.Boolean(default=True)

	best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

	property_type_id = fields.Many2one("estate.property.type", string="Property Type")
	buyer_id = fields.Many2one("res.partner", string = "Buyer", copy=False)
	salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)

	tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")

	offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offer')

	total_area = fields.Integer(compute="_compute_total_area")

	@api.depends("living_area", "garden_area")	# Lets the ORM layer know the fields upon which on the computed field depends, so that 
	def _compute_total_area(self):				# the computed field can be recomputed if/when its dependencies change in value
		for record in self:
			record.total_area = record.living_area + record.garden_area

	''' 'self' is a collection.
		The object self is a recordset, i.e. an ordered collection of records. 
		It supports the standard Python operations on collections, e.g. len(self) and iter(self), plus extra set operations such as recs1 | recs2.
		Iterating over self gives the records one by one, where each record is itself a collection of size 1. 
		You can access/assign fields on single records by using the dot notation, e.g. record.name. '''

	

	# For relational fields it's possible to use paths through a field as a dependency
	@api.depends("offer_ids.price")
	def _compute_best_price(self):
		temp_best_price = 0.0
		for record in self:
			if len(record.mapped('offer_ids.price')) > 0:
				record.best_price = max(record.mapped('offer_ids.price')) # mapped() documentation: https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#map
			else:
				record.best_price = 0


	@api.onchange("garden")
	def _onchange_garden(self):
		if self.garden == True:
			self.garden_area = 10
			self.garden_orientation = 'north'
		else:
			self.garden_area = 0
			self.garden_orientation = ''

	def action_sold_button(self):		# having a <button/> and adding <... type='object' ...> to it means odoo will look for and find function of the same name: this one 
		for record in self:
			if record.state == 'cancelled':
				raise exceptions.UserError("Cancelled properties cannot be sold.")
			else:
				record.state = 'sold'
		return True							# Chapter 9: Finally, a public method should always return something so that it can be called through XML-RPC. When in doubt, just return True.

	def action_cancel_button(self):
		for record in self:
			if record.state == 'sold':
				raise exceptions.UserError("Sold properties cannot be cancelled.")
			else:
				record.state = 'cancelled'
		return True							# Chapter 9: Finally, a public method should always return something so that it can be called through XML-RPC. When in doubt, just return True.
	
	@api.constrains('selling_price', 'expected_price', 'offer_ids')
	def _check_selling_price(self):
		acceptedOfferExists = False
		for record in self:
			if len(record.offer_ids) > 0:
				for offer in record.offer_ids:
					if offer.state == 'accepted':

						record.state = 'offer_accepted'		# inserting this behavior into _check_selling_price for convenience because tutorial never explicitly told me to do it, maybe it's own function is more ideal

						acceptedOfferExists = True
						break
				
				if acceptedOfferExists == True:
					if record.selling_price < record.expected_price * .90:
						raise exceptions.ValidationError("The selling price must be at least 90% of the expected price")

	@api.ondelete(at_uninstall=False)	# using ondelete decorator instead of overriding unlink because overriding unlink messes with uninstallation
	def _unlink_if_state_new_or_cancelled(self):
		for record in self:
			if record.state != 'new' and record.state != 'cancelled':
				raise exceptions.UserError("You cannot delete a property that is not in the 'New' or 'Cancelled' state.")
				# no need to return super() because this method (thanks to @api.ondelete) is just a hook that adds logic right BEFORE unlink() is executed on a record

