from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties, buildings, and collections of buildings, and the land associated with each."
    _sql_constraints = [('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price must be strictly positive')]
    _order = 'price desc'

    price = fields.Float(string="Price")
    state = fields.Selection(string="Status",copy=False,selection=[('accepted','Accepted'),('refused','Refused')],readonly=True)
    partner_id = fields.Many2one("res.partner", string="Buyer",required=True)
    property_id = fields.Many2one("estate.property",string="Property",required=True)

    validity = fields.Integer(compute='_inverse_date_deadline', inverse='_compute_date_deadline', string='Validity', default='7', store=True)


    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string="Deadline", store=True, default=fields.Date.add(fields.Date.today(),days=7))

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends('create_date', 'date_deadline', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date != False:
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date),days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
            
    @api.depends('create_date', 'validity', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date != False:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer_button(self):
        for record in self:
            record.state = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            return True

    def action_refuse_offer_button(self):
        for record in self:
            record.state = 'refused'
            return True