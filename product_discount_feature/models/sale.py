from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id','product_uom_qty')
    def _onchange_product_id_set_discount(self):
        """Override unit price based on product discount if available."""
        if self.product_id:
            # Get the discounted price from the product
            discounted_price = self.product_id.discounted_price
            # Update the price_unit with the discounted price
            self.price_unit = discounted_price

    def update_price_unit(self, vals, is_create=False):
        # Check if any of the specified fields are in vals
        if any(field in vals for field in ['product_uom_qty', 'product_id', 'price_unit', 'tax_id', 'discount']):
            # During creation, we don't have existing lines to loop through
            lines = self if not is_create else [vals]

            for line in lines:
                # Determine product_id from vals or use the current line's product_id
                product_id = vals.get('product_id', line['product_id'] if is_create else line.product_id.id)
                
                # Fetch the product record
                product = self.env['product.product'].browse(product_id)
                
                # Update price_unit with product's discounted price
                vals['price_unit'] = product.discounted_price  # Ensure 'discounted_price' exists on product

    def create(self, vals):
        print(vals, "============== Create ===============")
        self.update_price_unit(vals, is_create=True)
        return super(SaleOrderLine, self).create(vals)

    def write(self, vals):
        print(vals, "================= Write ================")
        self.update_price_unit(vals)
        return super(SaleOrderLine, self).write(vals)


# Here, the _onchange_product_id_set_discount method changes the amount in the sale order line.
# However, when we hit the save button, the sale order line is recomputed by Odoo's base method,
# causing the amount to be recalculated. As a result, we cannot use the discount amount value in the unit price.
#  To address this, I have added a write method that applies the value during the save process.without make changes in default method 