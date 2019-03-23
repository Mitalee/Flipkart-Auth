from __future__ import absolute_import

from flask import current_app as app

import json
import requests
from urllib.parse import urlencode

import string
import random

#from . import settings


class AuthClient(requests.Session):

    def __init__(self, app_id, app_secret, redirect_uri, environment, state_token=None, access_token=None, refresh_token=None):
        
        """Constructor for Authapp        
        :param redirect_uri: Redirect URI, handles callback from provider
        :param environment: App Environment, accepted values: 'sandbox','production','prod'
        :param state_token: CSRF token, generated if not provided, defaults to None
        :param access_token: Access Token for refresh or revoke functionality, defaults to None
        :param refresh_token: Refresh Token for refresh or revoke functionality, defaults to None
        :param id_token: ID Token for OpenID flow, defaults to None
        """

        super(AuthClient, self).__init__()

        self.app_id = app_id
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.environment = environment
        self.state_token = state_token


        #endpoints
        self.auth_endpoint = app.config['URL_AUTH']
        self.token_endpoint = app.config['URL_TOKEN']
        self.redirect_uri = app.config['REDIRECT_URI']

        # self.redirect_uri= "http://localhost:8001"
        # self.auth_endpoint = 'https://api.flipkart.net/oauth-service/oauth/authorize'
        # self.token_endpoint = 'https://api.flipkart.net/oauth-service/oauth/token?'

        # response values
        self.access_token = access_token
        self.expires_in = None
        self.refresh_token = refresh_token


        
    def get_authorization_url(self, state_token=None):
        """Generates authorization url using scopes specified where user is redirected to
        
        :param scopes: Scopes for OAuth/OpenId flow
        :type scopes: list of enum, `intuitlib.enums.Scopes`
        :param state_token: CSRF token, defaults to None
        :return: Authorization url
        """

        state = state_token or self.state_token 
        if state is None:
            state = generate_token()
        self.state_token = state

        url_params = {
            'client_id': self.app_id,
            'response_type': 'code',
            'scope': 'Seller_Api',
            'redirect_uri': self.redirect_uri,
            'state': self.state_token 
        }

        return ''.join([self.auth_endpoint, urlencode(url_params)])

    def get_access_token(self, auth_code):
        """Gets access_token and refresh_token using authorization code
        
        :param auth_code: Authorization code received from redirect_uri
        """
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Authorization': get_auth_header(self.app_id, self.app_secret)
        # }

        body = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        # send_request('POST', self.token_endpoint, headers, self, body=urlencode(body), session=self)   

        headers = {
          #'Authorization': '11a408bb3b648b6a2a62191028a2858a18997:734c4c025c6b163dd5ae7c021c9459d6', 
            'Accept': 'application/json', 
            'Content-Type': 'application/json;charset=utf-8'
        }

        url_token = ''.join(self.token_endpoint, urlencode(body))
        print('URL_TOKEN IS: ', url_token)
        #r = requests.get(url, auth=HTTPBasicAuth('6b378b5a2761427a06650656548123a14b56','27ba19c6d2fc10346c68f4381b704c0c2'))
        r = requests.get(url_token, auth=(app.config['APP_ID'],app.config['APP_SECRET']))
        return (r)

    # def refresh(self, refresh_token=None):
    #     """Gets fresh access_token and refresh_token 
        
    #     :param refresh_token: Refresh Token
    #     :raises ValueError: if Refresh Token value not specified
    #     :raises `intuitlib.exceptions.AuthappError`: if response status != 200
    #     """

    #     token = refresh_token or self.refresh_token
    #     if token is None:
    #         raise ValueError('Refresh token not specified')

    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Authorization': get_auth_header(self.app_id, self.app_secret)
    #     }

    #     body = {
    #         'grant_type': 'refresh_token',
    #         'refresh_token': token
    #     }

    #     send_request('POST', self.token_endpoint, headers, self, body=urlencode(body), session=self)

            
    # def get_user_info(self, access_token=None):
    #     """Gets User Info based on OpenID scopes specified
        
    #     :param access_token: Access token
    #     :raises ValueError: if Refresh Token or Access Token value not specified
    #     :raises `intuitlib.exceptions.AuthappError`: if response status != 200
    #     :return: Requests object
    #     """

    #     token = access_token or self.access_token
    #     if token is None:
    #         raise ValueError('Acceess token not specified')

    #     headers = {
    #         'Authorization': 'Bearer {0}'.format(token)
    #     }

    #     return send_request('GET', self.user_info_url, headers, self, session=self)


def generate_token(length=30, allowed_chars=''.join([string.ascii_letters, string.digits])):
    """Generates random CSRF token
    
    :param length: Length of CSRF token, defaults to 30
    :param allowed_chars: Characters to use, defaults to 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    :return: Token string
    """

    return ''.join(random.choice(allowed_chars) for i in range(length))