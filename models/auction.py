from odoo import api, fields, models
from datetime import date, datetime

from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class NewAuction(models.Model):
    _name = "new.auction"
    _description = "New Auction"
    _rec_name = "auction_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    auction_name = fields.Char(string="Auction Name", required=True, help="Enter auction name",tracking=True)
    auction_property = fields.Many2one("new.property", string="Property",tracking=True)
    initial_price = fields.Float(string="Initial Price", related="auction_property.price", store=True)
    reserve_price = fields.Float(string="Reserve Price",tracking=True)
    start_date = fields.Datetime(string="Start DateTime",tracking=True)
    end_date = fields.Datetime(string="End DateTime",tracking=True)
    extend_by = fields.Datetime(string="Extend By")
    bid_ids = fields.One2many('bid.logs', 'auction_id', string="Bid", ondelete="cascade",tracking=True)
    highest_bid = fields.Float(string="Highest_bid", compute="_compute_highest_bid",
                               default=lambda self: self.initial_price,tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('running', 'Running'),
        ('extended', 'Extended'), ('closed', 'Closed'), ('finished', 'Finished')
    ], default='draft',tracking=True)

    remaining_time = fields.Char(string="Remaining Time", compute="_compute_remaining_time", store=False)

    @api.depends('start_date', 'end_date')
    def _compute_remaining_time(self):
        for rec in self:
            if rec.status == 'running':
                remaining_seconds = (rec.end_date - fields.Datetime.now()).total_seconds()
                if remaining_seconds > 0:
                    hours = int(remaining_seconds // 3600)
                    minutes = int((remaining_seconds % 3600) // 60)
                    seconds = int(remaining_seconds % 60)
                    rec.remaining_time = f"{hours}h {minutes}m {seconds}s"
                else:
                    rec.remaining_time = "Auction Ended"
            else:
                rec.remaining_time = "Auction Not Running"

    @api.depends("bid_ids.bid_amount")
    def _compute_highest_bid(self):
        for rec in self:
            if rec.bid_ids:
                rec.highest_bid = max(rec.bid_ids.mapped('bid_amount'))
            else:
                rec.highest_bid = rec.initial_price

    def action_confirm(self):
        for rec in self:
            rec.status = 'confirmed'

    def action_run(self):
        for rec in self:
            rec.status = 'running'

    @api.model
    def auto_update_status(self):
        """ Update status to 'running' if the current datetime matches start_date """
        auction_to_start = self.search([('start_date', '<=', fields.Datetime.now()), ('status', '=', 'confirmed')])
        for auction in auction_to_start:
            auction.status = 'running'
        auction_to_end = self.search([('end_date', '<=', fields.Datetime.now()), ('status', '=', 'running')])
        for auction in auction_to_end:
            auction.status = 'finished'

            # Send email to the highest bidder
            if auction.bid_ids:
                # Get the highest bidder
                highest_bid = max(auction.bid_ids, key=lambda x: x.bid_amount)
                highest_bidder = highest_bid.user_id
                highest_bid_amount = highest_bid.bid_amount

                # Send email if the highest bidder exists and has an email
                if highest_bidder.email:
                    subject = f"Congratulations! You've won the auction {auction.auction_name}"
                    body = f"""
                        <p>Dear {highest_bidder.name},</p>
                        <p>Congratulations! You have won the auction for <strong>{auction.auction_name}</strong>.</p>
                        <p>Your winning bid was <strong>{highest_bid_amount}</strong>.</p>
                        <p>Thank you for participating!</p>
                    """

                    # Create and send the email
                    mail = self.env['mail.mail'].create({
                        'subject': subject,
                        'body_html': body,
                        'email_to': highest_bidder.email,
                    })
                    mail.send()

    def action_extend(self):
        for rec in self:
            rec.status = 'extended'

    def action_close(self):
        for rec in self:
            rec.status = 'closed'
            # Send email to the highest bidder
            if rec.bid_ids:
                # Get the highest bidder
                highest_bid = max(rec.bid_ids, key=lambda x: x.bid_amount)
                highest_bidder = highest_bid.user_id
                highest_bid_amount = highest_bid.bid_amount

                # Send email if the highest bidder exists and has an email
                if highest_bidder.email:
                    subject = f"Congratulations! You've won the auction {rec.auction_name}"
                    body = f"""
                        <p>Dear {highest_bidder.name},</p>
                        <p>Congratulations! You have won the auction for <strong>{rec.auction_name}</strong>.</p>
                        <p>Your winning bid was <strong>{highest_bid_amount}</strong>.</p>
                        <p>Thank you for participating!</p>
                    """

                    # Create and send the email
                    mail = self.env['mail.mail'].create({
                        'subject': subject,
                        'body_html': body,
                        'email_to': highest_bidder.email,
                    })
                    mail.send()

    @api.model
    def get_auction_data_for_frontend(self):
        auctions = self.search([])  # Get all auctions or specific auctions
        data = []
        for auction in auctions:
            data.append({
                'auction_name': auction.auction_name,
                'end_date': auction.end_date and auction.end_date.isoformat()  # Ensure it's in ISO format (UTC)
            })
        return data

