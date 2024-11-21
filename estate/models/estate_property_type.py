from odoo import fields, models, api

class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "Categories of properties, buildings, and collections of buildings, and the land assocaited with each."
	_sql_constraints = [('unique_type_name', 'UNIQUE(name)', 'Property types must be unique.')]
	_order = 'sequence, name'

	name = fields.Char(string="Name",required=True)
	property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties') #because a One2many is a virtual relationship, there MUST be a Many2one field defined in the comodel (the inverse field 'property_type_id' in this example)
	sequence = fields.Integer(string='Sequence', default=1, help="Used to order stages. Lower is better.")

	offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
	offer_count = fields.Integer(compute="_compute_offer_count", string="Number Of Offers")

	@api.depends('offer_ids')
	def _compute_offer_count(self):
		for record in self:
			record.offer_count = len(record.offer_ids)

	

