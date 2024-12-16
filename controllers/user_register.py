from odoo import http
from odoo.http import request


class AuctionUserController(http.Controller):

    # Registration Page
    @http.route('/auction/register', type='http', auth='public', website=True)
    def auction_register(self, **kwargs):
        return request.render('auction_management.register_template', {})

    # Handle Registration Submission
    @http.route('/auction/register/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def auction_register_submit(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        phone = kwargs.get('phone')
        address = kwargs.get('address')

        # Check if the email already exists
        existing_user = request.env['auction.user'].sudo().search([('email', '=', email)], limit=1)
        if existing_user:
            return request.render('auction_management.register_template', {'error': 'Email already exists.'})

        # Create a new user
        request.env['auction.user'].sudo().create({
            'name': name,
            'email': email,
            'password': password,
            'phone': phone,
            'address': address,
        })
        return request.redirect('/auction/login')

    # Login Page
    @http.route('/auction/login', type='http', auth='public', website=True)
    def auction_login(self, **kwargs):
        return request.render('auction_management.login_template', {})

    # Handle Login Submission
    @http.route('/auction/login/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def auction_login_submit(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        # Check user credentials
        user = request.env['auction.user'].sudo().search([('email', '=', email), ('password', '=', password)], limit=1)
        if user:
            # Store user ID in session
            request.session['auction_user_id'] = user.id
            return request.redirect('/home')
        else:
            return request.render('auction_management.login_template', {'error': 'Invalid email or password.'})

    # Logout Route
    @http.route('/auction/logout', type='http', auth="public", website=True, csrf=False)
    def logout_user(self):
        # Clear the session key for the auction user
        if 'auction_user_id' in request.session:
            request.session.pop('auction_user_id', None)

        return request.redirect('/home')

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
