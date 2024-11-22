from odoo import api, fields, models, exceptions

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
                                
    @api.model  # Declare this method as a "model method" (works at the model level, not tied to specific records).
    def create(self, vals):  # self: used to interact with the actual records in the database (read, update, delete, etc.). Refers to the records (recordset) in memory. If no records exist (e.g., in create()) self represents the model. # Override the create method to add custom logic when a new offer is created.
                             # vals: carries input data for the new record(s) being created or updated. Only represents the data at the moment the method is called. It is not tied to any actual records in the database yet. Temporary and specific to the create() or write() call.
        # Check if the `property_id` is present in the input dictionary `vals`.
        if 'property_id' in vals:
            # Use self.env to access the 'estate.property' model and get the property record associated with the given property_id.
            property_id = self.env['estate.property'].browse(vals['property_id'])

            # Filter existing offers on the property to find if any have a price higher than the new offer's price.
            higher_offers = property_id.offer_ids.filtered(lambda offer: offer.price > vals.get('price', 0))

            # If there are any higher offers already, raise a UserError to prevent the new offer from being created.
            if higher_offers:
                raise exceptions.UserError("You cannot create an offer with a lower amount than an existing offer.")

            # If the offer is valid, update the state of the property to 'Offer Received'.
            property_id.state = 'offer_received'

        # Call the parent (super) create method to actually insert the new offer into the database.
        # This ensures that the record is created after our custom logic is applied.
        return super().create(vals)