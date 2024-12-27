from odoo import http
from odoo.http import request


class AuctionManagement(http.Controller):

    @http.route('/profile', type='http', auth='user', website=True)
    def user_profile(self, **kwargs):
        # Get the logged-in user's ID from the session
        auction_user_id = request.session.get('auction_user_id')

        # If no user is logged in, redirect to the login page
        if not auction_user_id:
            return request.redirect('/auction/login')

        # Fetch the logged-in user's data
        user = request.env['auction.user'].sudo().browse(auction_user_id)

        # Check if the user exists in the database
        if not user.exists():
            return request.redirect('/auction/login')

        # Render the user profile page
        return request.render('auction_management.user_profile', {
            'user': user
        })