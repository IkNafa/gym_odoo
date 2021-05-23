from odoo import http
from odoo.http import request
import werkzeug

class ResPartnerController(http.Controller):

    @http.route('/register', website=True, auth='public', methods=['GET'])
    def registerUser(self, **kw):
        return request.render('gym_base.register',{})

    @http.route('/user/create', type="http", auth="public", website=True)
    def create_user(self, **kw):
        return werkzeug.utils.redirect('/web')