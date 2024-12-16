from pkg_resources import require

from odoo import api,models,fields,_
from odoo.exceptions import ValidationError


class NewUser(models.Model):
    _name = "auction.user"
    _description = "User information"

    name = fields.Char(string='Full Name', required=True)
    email = fields.Char(string='Email', required=True, unique=True)
    password = fields.Char(string='Password', required=True)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True)
    bid_id=fields.Many2one('bid.logs', string="Bid")

    _sql_constraints = [
        ('email_unique','unique(email)','The email must be unique.'),
    ]

    def _check_email_format(self):
        for record in self:
            if not record.email or '@' not in record.email:
                raise ValidationError(_("Please provide a valid email address"))

    def check_credentials(self,email,password):
        user = self.search([('email','=',email),('password','=',password)],limit=1)
        return user if user else None