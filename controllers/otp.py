import random
from odoo import http
from odoo.http import request
from twilio.rest import Client  # For sending SMS via Twilio

class AuctionUserController(http.Controller):

    def generate_otp(self):
        """Generates a random 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def send_email_otp(self, email, otp):
        """Send OTP via email using Odoo's built-in email system"""
        template = request.env.ref('auction_management.email_otp_template')
        if template:
            template.sudo().send_mail(1, email_values={'email_to': email, 'otp': otp})

    def send_sms_otp(self, phone_number, otp):
        """Send OTP via SMS using Twilio API"""
        # Twilio setup (You need to replace these with your own credentials)
        account_sid = 'your_twilio_account_sid'
        auth_token = 'your_twilio_auth_token'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f'Your OTP for Auction Registration is {otp}',
            from_='+your_twilio_phone_number',  # Twilio number
            to=phone_number
        )
        return message.sid

    # Registration Page
    @http.route('/auction/register', type='http', auth='public', website=True)
    def auction_register(self, **kwargs):
        return request.render('auction_management.register_template', {})

    # Handle Registration Submission (Step 1: Send OTPs)
    @http.route('/auction/register/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def auction_register_submit(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        phone = kwargs.get('phone')
        address = kwargs.get('address')

        # Check if email already exists
        existing_user = request.env['auction.user'].sudo().search([('email', '=', email)], limit=1)
        if existing_user:
            return request.render('auction_management.register_template', {'error': 'Email already exists.'})

        # Generate OTPs
        email_otp = self.generate_otp()
        phone_otp = self.generate_otp()

        # Save OTPs temporarily in session for verification
        request.session['email_otp'] = email_otp
        request.session['phone_otp'] = phone_otp
        request.session['user_data'] = {
            'name': name,
            'email': email,
            'password': password,
            'phone': phone,
            'address': address,
        }

        # Send OTP to email and phone
        self.send_email_otp(email, email_otp)
        self.send_sms_otp(phone, phone_otp)

        return request.render('auction_management.otp_verification_template', {})

    # OTP Verification Page
    @http.route('/auction/verify_otp', type='http', auth='public', website=True)
    def verify_otp(self, **kwargs):
        return request.render('auction_management.otp_verification_template', {})

    # Handle OTP Verification
    @http.route('/auction/verify_otp/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def verify_otp_submit(self, **kwargs):
        email_otp = kwargs.get('email_otp')
        phone_otp = kwargs.get('phone_otp')

        # Fetch OTPs from session
        session_email_otp = request.session.get('email_otp')
        session_phone_otp = request.session.get('phone_otp')

        if email_otp == session_email_otp and phone_otp == session_phone_otp:
            # If OTPs are correct, create the user and register them
            user_data = request.session.get('user_data')
            request.env['auction.user'].sudo().create({
                'name': user_data['name'],
                'email': user_data['email'],
                'password': user_data['password'],
                'phone': user_data['phone'],
                'address': user_data['address'],
            })

            # Clear the session data
            request.session.pop('email_otp', None)
            request.session.pop('phone_otp', None)
            request.session.pop('user_data', None)

            return request.redirect('/auction/login')

        else:
            return request.render('auction_management.otp_verification_template', {'error': 'Invalid OTPs.'})
