from odoo import http
from odoo.http import request

class AuctionManagement(http.Controller):

    @http.route('/auction/profile1', type='http', auth='user', website=True)
    def user_profile(self, **kwargs):
        user = request.env.user  # Get the currently logged-in user
        if not user:
            return request.redirect('/web/login')  # Redirect to login if not authenticated

        return request.render('auction_management.user_profile_template', {
            'user': user
        })
