from odoo import http
from odoo.http import request
import logging
from datetime import datetime
import websocket
import json

_logger = logging.getLogger(__name__)


class AuctionController(http.Controller):

    @http.route('/auction/list', type='http', auth='public', website=True)
    def auction_list(self):
        # Fetch auctions that are running and not ended yet
        auctions = request.env['new.auction'].sudo().search([
            ('status', '=', 'running'),
            ('end_date', '>=', datetime.now()),

        ])

        property = auctions.auction_property

        # Get success and error messages from URL parameters
        success_message = request.params.get('success_message', False)
        error_message = request.params.get('error', False)

        # Render the auction list page with the auctions and any messages
        return request.render('auction_management.auction_list_template', {
            'auctions': auctions,
            'success_message': success_message,
            'error_message': error_message,
            'property': property,
        })

    # @http.route('/auction/completed_auctions',type='http',auth='public', webiste=True)
    # def completed_auctions(self):
    #     finished_auctions = request.env['new.auction'].sudo().search([
    #         ('status', '=', 'finished'),
    #         ('end_date', '<', datetime.now())
    #     ])
    #
    #     success_message = request.params.get('success_message', False)
    #     error_message = request.params.get('error', False)
    #
    #     return request.render('auction_management.complete_auctions_template', {
    #         'finished_auctions': finished_auctions,
    #         'success_message': success_message,
    #         'error_message': error_message,
    #
    #     })

    @http.route('/auction/completed_auctions', type='http', auth='public', website=True)
    def finished_auction_list(self):
        # Fetch auctions that have ended
        finished_auctions = request.env['new.auction'].sudo().search([
            ('status', '=', 'finished'),
            ('end_date', '<', datetime.now())
        ])

        # Get success and error messages from URL parameters
        success_message = request.params.get('success_message', False)
        error_message = request.params.get('error', False)

        # Render the finished auction list page
        return request.render('auction_management.finished_auction_list_template', {
            'finished_auctions': finished_auctions,
            'success_message': success_message,
            'error_message': error_message,
        })
    
    @http.route('/auction/bid', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def place_bid(self, **kwargs):
        try:
            # Fetch the logged-in auction user from the session
            auction_user_id = request.session.get('auction_user_id')
            if not auction_user_id:
                return request.redirect('/auction/login?error=Please log in to place a bid.')

            auction_user = request.env['auction.user'].sudo().browse(auction_user_id)
            if not auction_user.exists():
                return request.redirect('/auction/login?error=User not found.')

            # Fetch auction details
            auction_id = int(kwargs.get('auction_id'))
            bid_amount = float(kwargs.get('bid_amount'))
            auction = request.env['new.auction'].sudo().browse(auction_id)

            if not auction.exists():
                return request.redirect(f'/auction/list?error=Auction not found.')

            # Validate the bid amount
            current_highest_bid = auction.highest_bid if auction.highest_bid else auction.initial_price
            if bid_amount <= current_highest_bid:
                return request.redirect(f'/auction/list?error=Bid must be higher than the current highest bid.')

            # Log the bid
            bid_logs = request.env['bid.logs'].sudo().create({
                'user_id': auction_user.id,  # Store the custom auction user
                'auction_id': auction_id,
                'bid_amount': bid_amount,
            })

            # Update the highest bid in the auction
            auction.sudo().write({'highest_bid': bid_amount})

            _logger.info(f"Broadcasting new bid update for auction_id: {auction_id}, highest_bid: {bid_amount}")

            # Connect to WebSocket server and send the bid update
            ws = websocket.create_connection("ws://localhost:3000")
            ws.send(json.dumps({
                "auction_id": auction.id,
                "highest_bid": bid_amount,
            }))
            ws.close()

            # Send confirmation email using the model function
            bid_logs.sudo().bid_confirmation_email(auction_user, auction, bid_amount)

            return request.redirect(f'/auction/list?success_message=Your bid has been placed successfully.')

        except Exception as e:
            _logger.error(f"Error placing bid: {e}")
            return request.redirect(f'/auction/list?error=Internal server error. Please try again later.')