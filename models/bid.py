from odoo import models, api, fields
from odoo.exceptions import ValidationError
from datetime import date, datetime
import os

import logging

_logger = logging.getLogger(__name__)


class BidRules(models.Model):
    _name = "bid.rules"
    _description = "Bidding rules and description"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Bid Name", required=True)
    active = fields.Boolean(default=True)
    from_price = fields.Float()
    to_price = fields.Float()
    increment_by = fields.Float()

    minimum_increment = fields.Float(string="Increment amount")

    @api.model
    def create(self, vals):
        # Ensure from_price is less than to_price on record creation
        if vals.get('from_price', 0.0) >= vals.get('to_price', 0.0):
            raise ValidationError("Start price must be less than end price.")
        return super(BidRules, self).create(vals)

    def write(self, vals):
        # Ensure from_price is less than to_price on record update
        if 'from_price' in vals and 'to_price' in vals:
            if vals['from_price'] >= vals['to_price']:
                raise ValidationError("Start price must be less than end price.")
        elif 'from_price' in vals:
            if vals['from_price'] >= self.to_price:
                raise ValidationError("Start price must be less than end price.")
        elif 'to_price' in vals:
            if self.from_price >= vals['to_price']:
                raise ValidationError("Start price must be less than end price.")
        return super(BidRules, self).write(vals)


class BidLogs(models.Model):
    _name = "bid.logs"
    _description = "Captures all the bidding information"
    _order = "bid_amount desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('auction.user', string="Bidder", required=True)
    auction_id = fields.Many2one('new.auction', string="Auction")
    property_id = fields.Many2one('new.property', string="Property", related="auction_id.auction_property", store=True)
    bid_amount = fields.Float(string="Bid Amount", required=True)
    bid_time = fields.Datetime(string="Bid Time", default=lambda self: fields.Datetime.now())
    is_highest = fields.Boolean(string="Is Highest Bid", default=False)
    highest_bid = fields.Float(string="Highest Bid", related='auction_id.highest_bid', store=True)

    @api.model
    def create(self, vals):
        # Get the auction record before creating the bid
        auction = self.env['new.auction'].browse(vals.get('auction_id'))

        # Check if the bid amount is greater than the current highest bid
        if auction and vals.get('bid_amount') <= auction.highest_bid:
            raise ValidationError('Bid amount must be higher than the current highest bid.')

        # Create the bid
        bid = super(BidLogs, self).create(vals)

        # After creating the bid, update the auction's highest bid
        if bid.bid_amount > auction.highest_bid:
            auction.write({'highest_bid': bid.bid_amount})

        return bid

    def save_log_to_file(self, log):
        """Save log details to a designated file."""
        log_directory = "/home/user/odoo18/custom_addons/auction_management"  # Replace with your desired path
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_file_path = os.path.join(log_directory, f"auction_{log.auction_id.id}_logs.txt")

        with open(log_file_path, "a") as log_file:
            log_file.write(f"Time: {log.bid_time}, Bidder: {log.user_id.name}, "
                           f"Auction: {log.auction_id.auction_name}, "
                           f"Property: {log.property_id.name}, "
                           f"Bid: {log.bid_amount}\n")

        return log_file_path

    @api.model
    def bid_confirmation_email(self, auction_user, auction, bid_amount):
        try:
            # prepare email values
            email_values = {
                'subject': f'Bid confirmation for auction {auction.auction_name}',
                'email_to': auction_user.email,
                'body_html': f"""
                    <p>Hello {auction_user.name},</p>
                    <p>Thank you for your bid on the auction <strong>{auction.auction_name}</strong>.</p>
                    <p>Your bid amount: <strong>{bid_amount}</strong></p>
                    <p>Best of luck!</p>
                """,
                'email_from': self.env.user.email,
            }
            print(f"email:{self.env.user.email},{auction_user.email}")

            # Create and send the email
            mail = self.env['mail.mail'].create(email_values)
            mail.send()
            _logger.info(f"Bid confirmation email sent to {auction_user.email} for auction {auction.name}.")
        except Exception as e:
            _logger.error(f"Failed to send bid confirmation email: {e}")






