from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class AuctionPropertyController(http.Controller):

    @http.route('/auction/view/<int:auction_id>', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def view_auction(self, auction_id, **kwargs):
        auction = request.env['new.auction'].sudo().browse(auction_id)
        if not auction.exists():
            return request.render('website.404')  # If the auction doesn't exist, show 404 page.

        if http.request.httprequest.method == 'POST':
            try:
                # Fetch the logged-in auction user from the session
                auction_user_id = request.session.get('auction_user_id')
                if not auction_user_id:
                    return request.redirect(f'/auction/view/{auction_id}?error=Please log in to place a bid.')

                auction_user = request.env['auction.user'].sudo().browse(auction_user_id)
                if not auction_user.exists():
                    return request.redirect(f'/auction/view/{auction_id}?error=User not found.')

                # Fetch bid amount
                bid_amount = float(kwargs.get('bid_amount'))
                current_highest_bid = auction.highest_bid if auction.highest_bid else auction.initial_price

                # Validate the bid amount
                if bid_amount <= current_highest_bid:
                    return request.redirect(f'/auction/view/{auction_id}?error=Bid must be higher than the current highest bid.')

                # Log the bid
                request.env['bid.logs'].sudo().create({
                    'user_id': auction_user.id,  # Store the custom auction user
                    'auction_id': auction_id,
                    'bid_amount': bid_amount,
                })

                # Update the highest bid in the auction
                auction.sudo().write({'highest_bid': bid_amount})

                return request.redirect(f'/auction/view/{auction_id}?success_message=Your bid has been placed successfully.')

            except Exception as e:
                _logger.error(f"Error placing bid: {e}")
                return request.redirect(f'/auction/view/{auction_id}?error=Internal server error. Please try again later.')

        # Get the property associated with the auction
        property = auction.auction_property

        # Render the auction details page
        success_message = request.params.get('success_message', False)
        error_message = request.params.get('error', False)

        return request.render('auction_management.auction_details_page', {
            'auction': auction,
            'property': property,
            'success_message': success_message,
            'error_message': error_message,
        })

    @http.route('/auction/bidss', type='http', auth='public', methods=['POST'], website=True, csrf=False)
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
            request.env['bid.logs'].sudo().create({
                'user_id': auction_user.id,  # Store the custom auction user
                'auction_id': auction_id,
                'bid_amount': bid_amount,
            })

            # Update the highest bid in the auction
            auction.sudo().write({'highest_bid': bid_amount})

            return request.redirect(f'/auction/list?success_message=Your bid has been placed successfully.')

        except Exception as e:
            _logger.error(f"Error placing bid: {e}")
            return request.redirect(f'/auction/list?error=Internal server error. Please try again later.')


    @http.route('/property/view/<int:property_id>', auth='public', website=True)
    def view_property(self, property_id, **kwargs):
        property = request.env['new.property'].sudo().browse(property_id)
        if not property.exists():
            return request.render('website.404')  # If the property doesn't exist, show 404 page.

        # Render the property details page
        return request.render('auction_management.property_details_page', {
            'property': property,
        })
