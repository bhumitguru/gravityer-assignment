from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_percentage = fields.Float(string="Discount (%)", default=0.0)
    discounted_price = fields.Float(string="Discounted Price", compute="_compute_discounted_price", store=True)


    @api.depends('list_price', 'discount_percentage')
    def _compute_discounted_price(self):
        """
    Computes the discounted price for each product based on the list price and discount percentage.
    If a discount percentage is specified (greater than 0), it calculates the discount amount
    and subtracts it from the list price to get the discounted price.
    Otherwise, it sets the discounted price to the list price.

    This method ensures that the 'discounted_price' field is always up-to-date when either 
    'list_price' or 'discount_percentage' changes.
    """
        for product in self:
            if product.discount_percentage > 0:
                discount_amount = (product.discount_percentage / 100) * product.list_price
                product.discounted_price = product.list_price - discount_amount
            else:
                product.discounted_price = product.list_price
