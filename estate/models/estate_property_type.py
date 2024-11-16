from odoo import fields, models

class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "Categories of properties, buildings, and collections of buildings, and the land assocaited with each."
	_sql_constraints = [('unique_type_name', 'UNIQUE(name)', 'Property types must be unique.')]

	name = fields.Char(string="Name",required=True)
	



