from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id', 'product_uom_qty', 'order_id.pricelist_id')
    def _onchange_product_id_pricelist(self):
        for line in self:
            if line.order_id.pricelist_id:
                # Check if the selected pricelist uses tiered pricing
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', line.order_id.pricelist_id.id),
                    ('compute_price', '=', 'tiered'),
                    ('price_list_product_id', '=', line.product_id.id)
                ], limit=1)

                if pricelist_item:
                    # Find the correct tier based on quantity
                    for tire in pricelist_item.price_tire_ids:
                        if tire.tire_quantity_from <= line.product_uom_qty <= tire.tire_quantity_to:
                            line.price_unit = tire.list_price
                            break
