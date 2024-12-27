from odoo import fields,api,models

class NewProperty(models.Model):
    _name="new.property"
    _description="New Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char(string="Name", help="Property Name", required=True)
    auction_id=fields.Many2one("new.auction", string="auction", ondelete="cascade")
    type=fields.Many2one('asset.category', string="Type", required=False)
    image_ids=fields.One2many('property.image', 'property_id')
    loan_amount=fields.Float(string='Loan Amount', required=True, default=None)
    interest_rate=fields.Float(string='Interest', required=True)
    year=fields.Integer(string='Years', default=1)
    month=fields.Integer(string='Months')
    total_interest=fields.Float(string="Total Interst", compute="compute_total_interest", readonly=True, store=True)
    penalty=fields.Float(string='Penalty', required=True)
    bidding_fees=fields.Float(string='Bidding Fees', require=True)
    price=fields.Float(string="Price", required=False, compute="compute_toal_price", readonly=True, store=True)
    note=fields.Html()
    description=fields.Html()
    address=fields.Char(string="Address", required=False)
    city=fields.Char(string="City", required=False)
    pincode=fields.Char(string="Pincode", required=False)
    district=fields.Char(string="District", required=False)
    state=fields.Char(string="State", required=False)
    document=fields.Binary(string="Document",required=False)
    property=fields.Many2one('bid.logs', string="Property", ondelete="cascade")

    @api.onchange('interest_rate', 'year', 'month')
    def calculate_total_interest(self):
        for rec in self:
            principal=rec.loan_amount
            rate=rec.interest_rate
            time=rec.year+(rec.month/12)
            interest=principal*rate*time
            rec.total_interest=interest

    @api.onchange('loan_amount', 'total_interest', 'bidding_fees', 'penalty')
    def toal_price(self):
        for rec in self:
            total=rec.loan_amount+rec.total_interest+rec.bidding_fees+rec.penalty
            rec.price=total

    @api.depends('interest_rate', 'year', 'month')
    def compute_total_interest(self):
        for rec in self:
            principal=rec.loan_amount
            rate=rec.interest_rate
            time=rec.year+(rec.month/12)
            interest=principal*rate*time
            rec.total_interest=interest

    @api.depends('loan_amount', 'total_interest', 'bidding_fees', 'penalty')
    def compute_toal_price(self):
        for rec in self:
            total=rec.loan_amount+rec.total_interest+rec.bidding_fees+rec.penalty
            rec.price=total


class PropertyImage(models.Model):
    _name = 'property.image'
    _description = 'Property Images'

    property_id = fields.Many2one('new.property', string="Property", ondelete="cascade")
    image = fields.Binary(string="Images")


