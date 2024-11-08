from odoo import fields, models

class EstatePropertyTag(models.Model):
	_name = "estate.property.tag"
	_description = "Tags for properties, buildings, and collections of buildings, and the land assocaited with each."
	
	name = fields.Char(string="Name",required=True)
	



