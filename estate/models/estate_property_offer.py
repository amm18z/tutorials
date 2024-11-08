from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties, buildings, and collections of buildings, and the land associated with each."

    price = fields.Float(string="Price")
    status = fields.Selection(string="State",copy=False,selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one("res.partner", string="Buyer",required=True)
    property_id = fields.Many2one("estate.property",string="Property",required=True)

    

	



