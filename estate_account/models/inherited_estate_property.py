from odoo import models, exceptions

# Three Steps to inheriting and overloading a function in another module and model.

class InheritedEstateProperty(models.Model):
    _inherit = "estate.property"    # 1.) _inherit = _name of model

    def action_sold_button(self):   # 2.) def same_name_as_function_you're_overloading
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cancelled properties cannot be sold.")
            else:
                sales_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
                if not sales_journal:
                    raise exceptions.ValueError("No sales journal found. Please configure a Sales Journal.")

                invoice_vals = {
                    'partner_id': record.buyer_id.id,  # Buyer as the customer
                    'move_type': 'out_invoice',     # Customer Invoice
                    'journal_id': sales_journal.id, # The journal to use
                    'invoice_line_ids': [
                        # Line 1: 6% of the selling price
                        (0, 0, {
                            'name': "Commission (6% of Selling Price)",
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06,  # 6% commission
                        }),
                        # Line 2: Administrative fees
                        (0, 0, {
                            'name': "Administrative Fees",
                            'quantity': 1,
                            'price_unit': 100.00,  # Fixed fee
                        }),
                    ]
                }

                self.env['account.move'].create(invoice_vals)

        return super().action_sold_button()     # 3.) original/parent function is called when super().parent_function() is called