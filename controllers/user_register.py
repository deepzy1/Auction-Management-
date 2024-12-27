from odoo import http, fields
from odoo.http import request
from datetime import datetime

class AuctionUserController(http.Controller):

    # Route to display the registration form
    @http.route('/auction/register', type='http', auth='public', website=True)
    def auction_register(self, **kwargs):
        return request.render('auction_management.register_template', {})

    # Handle form submission for registration (no OTP needed)
    @http.route('/auction/register/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def auction_register_submit(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        phone = kwargs.get('phone')

        # Ensure password matches the confirmation password
        if kwargs.get('password') != kwargs.get('confirm_password'):
            return request.render('auction_management.register_template', {'error': 'Passwords do not match.'})

        # Check if email already exists
        if request.env['auction.user'].sudo().search([('email', '=', email)]):
            return request.render('auction_management.register_template', {'error': 'Email already exists.'})

        # Create the user without OTP
        request.env['auction.user'].sudo().create({
            'name': name,
            'email': email,
            'password': password,
            'phone': phone
        })

        # Redirect to login page after registration
        return request.redirect('/auction/login')

        # Home/Profile Page (Logged-In User)

    @http.route('/auction/profile', type='http', auth='public', website=True)
    def auction_home(self, **kwargs):
        # Get logged-in user ID from session
        auction_user_id = request.session.get('auction_user_id')
        if not auction_user_id:
            return request.redirect('/auction/login')

        # Fetch the logged-in user's details
        user = request.env['auction.user'].sudo().browse(auction_user_id)
        if not user.exists():
            return request.redirect('/auction/login')

        # Render user profile/home page
        return request.render('auction_management.user_profile_template', {'user': user})

