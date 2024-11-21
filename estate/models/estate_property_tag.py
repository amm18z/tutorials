from odoo import fields, models

class EstatePropertyTag(models.Model):
	_name = "estate.property.tag"
	_description = "Tags for properties, buildings, and collections of buildings, and the land assocaited with each."
	_sql_constraints = [('unique_tag_name', 'UNIQUE(name)', 'Property tags must be unique.')]
	_order = 'name'
	
	name = fields.Char(string="Name",required=True)
	color = fields.Integer(string="Color")
	
	



