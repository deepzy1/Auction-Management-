from odoo import http
from odoo.http import request
import random
import time
import json


class AuctionLoginController(http.Controller):

    @http.route('/auction/login', type='http', auth='public', website=True)
    def auction_login(self, **kwargs):
        return request.render('auction_management.login_template', {})

    @http.route('/auction/login/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def auction_login_submit(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        user = request.env['auction.user'].sudo().search([('email', '=', email), ('password', '=', password)], limit=1)
        if user:
            request.session['auction_user_id'] = user.id
            for x in request.session:
                print(f"re:{x}")
            return request.redirect('home')
        else:
            return request.render('auction_management.login_template', {'error': 'Invalid email or password.'})

    @http.route('/auction/logout', type='http', auth="public", methods=['GET'], csrf=False)
    def logout_user(self):
        # Clear specific session key for auction user
        if 'auction_user_id' in request.session:
            print(f"Logging out user: {request.session['auction_user_id']}")
            request.session.pop('auction_user_id', None)  # Clear auction user session

        # Debug: Print remaining session keys
        for key in request.session:
            print(f"Remaining session key after logout: {key}")

        return request.redirect('/auction/login')  # Redirect to login page

    @http.route('/auction/register/send_otp', type='json', auth='public', csrf=False)
    def send_otp(self):
        """Send OTP to the user's email."""
        data = request.httprequest.get_json()
        print(f"data_is:{data}")
        email = data.get('email')
        if not email:
            return {'success': False, 'error': 'Email is required.'}

        # Call the model method to generate and send the OTP
        success = request.env['user.register.otp'].sudo().generate_otp(email)
        print(f"success_is:{success}")
        if success:
            return {'success': True, 'message': 'OTP sent to your email.'}
        else:
            return {'success': False, 'error': 'Failed to send OTP. Please try again later.'}

    @http.route('/auction/register/verify_otp', type='json', auth='public', csrf=False)
    def verify_otp(self):
        """Verify OTP entered by the user."""
        data = request.httprequest.get_json()
        otp = data.get('otp')
        email = data.get('email')

        if not otp or not email:
            return {'success': False, 'error': 'OTP and email are required.'}

        # Find the OTP record for the given email
        otp_record = request.env['user.register.otp'].sudo().search([('email', '=', email)], limit=1)

        if not otp_record:
            return {'success': False, 'error': 'No OTP found for this email.'}

        # Check if the OTP has expired
        if otp_record.expire_time < fields.Datetime.now():
            return {'success': False, 'error': 'OTP has expired. Please request a new one.'}

        # Check if the OTP is correct
        if otp_record.otp == otp:
            # Mark OTP as verified
            otp_record.write({'otp_verified': True})

            return {'success': True, 'message': 'OTP verified successfully.'}
        else:
            return {'success': False, 'error': 'Invalid OTP. Please try again.'}

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



