from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import random
import logging

_logger = logging.getLogger(__name__)



class NewUser(models.Model):
    _name = "auction.user"
    _description = "User information"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True)
    email = fields.Char(string='Email', required=True, unique=True)
    password = fields.Char(string='Password', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True)
    bid_id = fields.Many2one('bid.logs', string="Bid")

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'The email must be unique.'),
    ]

    def _check_email_format(self):
        for record in self:
            if not record.email or '@' not in record.email:
                raise ValidationError(_("Please provide a valid email address"))

    def check_credentials(self, email, password):
        user = self.search([('email', '=', email), ('password', '=', password)], limit=1)





class UserRegisterOtp(models.Model):
    _name = "user.register.otp"
    _description = "User OTP for Registration"

    email = fields.Char(string="Email", required=True)
    otp = fields.Char(string='OTP')  # Temporary field for storing OTP
    expire_time = fields.Datetime(string="Expire Time", required=True)
    otp_verified = fields.Boolean(string='OTP Verified', default=False)

    @api.model
    def generate_otp(self, email):
        try:
            otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP

            # Set OTP expiration time (5 minutes)
            expire_time = fields.Datetime.now() + timedelta(minutes=5)

            # Create or update the OTP record for the email
            existing_otp = self.search([('email', '=', email)], limit=1)
            if existing_otp:
                existing_otp.write({'otp': otp, 'expire_time': expire_time})
            else:
                self.create({'otp': otp, 'expire_time': expire_time, 'email': email})

            # Send OTP via email
            mail_values = {
                'subject': 'Your OTP for Auction Registration',
                'email_to': email,
                'body_html': f"""
                    <p>Hello,</p>
                    <p>Your OTP for registration is: <strong>{otp}</strong></p>
                    <p>This OTP is valid for 5 minutes.</p>
                """,
                'email_from': 'no-reply@example.com',  # Set this to a valid sender email address
            }

            # Create and send the email
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

            _logger.info(f"OTP sent to {email}")
            return True

        except Exception as e:
            _logger.error(f"Error generating OTP for {email}: {e}")
            return False



class PasswordResetOtp(models.Model):
    _name = "password.reset.otp"
    _description = "OTP for Password Reset"

    email = fields.Char(string="Email")
    otp = fields.Char(string='OTP')  # Temporary field for storing OTP
    expire_time = fields.Datetime(string="Expire Time", required=True)
    otp_verified = fields.Boolean(string='OTP Verified', default=False)

    @api.model
    def generate_password_reset_otp(self, email):
        try:
            otp = random.randint(100000, 999999)

            expire_time = datetime.now() + timedelta(minutes=5)

            # Create or update the OTP record for the email
            existing_otp = self.search([('email', '=', email)], limit=1)
            if existing_otp:
                existing_otp.write({'otp': otp, 'expire_time': expire_time})
            else:
                self.create({'otp': otp, 'expire_time': expire_time, 'email': email})

            # Send OTP via email
            self.env['mail.mail'].create({
                'subject': 'Your OTP for Password Reset',
                'email_to': email,
                'body_html': f"""
                    <p>Hello,</p>
                    <p>Your OTP for password reset is: <strong>{otp}</strong></p>
                    <p>This OTP is valid for 5 minutes.</p>
                """,
                'email_from': self.env.user.email,
            }).send()

            return True

        except Exception as e:
            _logger.error(f"Error generating OTP for password reset for {email}: {e}")
            return False
