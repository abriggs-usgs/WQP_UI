
from functools import wraps
import time

from flask import redirect, url_for, Blueprint, session, request

from .. import app, oauth

auth_blueprint = Blueprint('auth', __name__)  # pylint: disable=C0103


def authentication_required_when_configured(f):
    '''
    View decorator used to decorate any view that requires authorization when the usgs theme is used
    :param function f: view function
    :return: Decorated function
    :rtype: function
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''
        Function which redirects to the authorization endpoint if the access token has expired otherwise
        executes the function.
        '''
        if app.config['WATERAUTH_AUTHORIZE_URL'] and (session.get('access_token_expires_at', 0) < int(time.time())):
            return redirect('{0}?next={1}'.format(url_for('auth.login'), request.url))
        return f(*args, **kwargs)

    return decorated_function


@auth_blueprint.route('/login')
def login():
    '''
    Redirects to the authentication's login.
    '''
    redirect_uri = '{0}?next={1}'.format(url_for('auth.authorize', _external=True), request.args.get('next'))

    return oauth.waterauth.authorize_redirect(redirect_uri)


@auth_blueprint.route('/authorize')
def authorize():
    '''
    Retrieves the access token from the authorization service and sets its value in a cookie.
    :return:
    '''
    token = oauth.waterauth.authorize_access_token(verify=False)

    response = redirect(request.args.get('next'))
    response.set_cookie('access_token', token.get('access_token'), secure=True)
    session['access_token_expires_at'] = token.get('expires_at')

    return response
