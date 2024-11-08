from odoo import fields, models

class EstatePropertyType(models.Model):
	_name = "estate.property.type"
	_description = "Categories of properties, buildings, and collections of buildings, and the land assocaited with each."
	
	name = fields.Char(string="Name",required=True)
	



