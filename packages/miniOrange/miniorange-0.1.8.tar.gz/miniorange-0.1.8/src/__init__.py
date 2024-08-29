import webbrowser

import requests
import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from typing import Callable
from urllib.parse import urlparse, parse_qs


class MiniOrange:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.base_url = None
        self.redirect_url = None
        self.public_key = None

    def set_client_id(self , client_id: str):
        self.client_id = client_id

    def set_client_secret(self , client_secret: str):
        self.client_secret = client_secret

    def set_base_url(self , base_url: str):
        self.base_url = base_url

    def set_redirect_url(self , redirect_url: str):
        self.redirect_url = redirect_url

    def set_public_key(self , public_key_pem: str):
        self.public_key = self.load_public_key( public_key_pem )

    @staticmethod
    def load_public_key(pem_data: str):
        try:
            public_key = load_pem_public_key( pem_data.encode() , backend=default_backend() )
            return public_key
        except ValueError as e:
            raise ValueError( f"Error loading public key: {e}" )

    def start_authorization(self):
        if not all( [self.client_id , self.base_url , self.redirect_url] ):
            raise ValueError( "Client ID, Base URL, or Redirect URL is not set" )

        auth_url = (
            f"{self.base_url}/moas/idp/openidsso?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_url}&"
            f"scope=openid&"
            f"response_type=code&"
            f"state=yAwL-57K10sIIpGeVO7nR7ZAnzdsj01uGothExyVpmo"
        )
        # webbrowser.open(auth_url)
        return auth_url

    def handle_authorization_response(self , uri: str , callback: Callable[[str] , None]):
        if not self.client_id or not self.client_secret:
            callback( "Client ID and/or Client Secret not set." )
            return

        parsed_uri = urlparse( uri )
        if parsed_uri.path.startswith( f"{self.base_url}/lander" ):
            query_params = parse_qs( parsed_uri.query )
            code = query_params.get( "code" , [None] )[0]
            if code:
                self.request_token( code , callback )

    def request_token(self , code: str , callback: Callable[[str] , None]):
        if not self.client_id or not self.client_secret or not self.redirect_url:
            callback( "Client ID, Client Secret, or Redirect URL not set." )
            return

        post_url = f"{self.base_url}/moas/rest/oauth/token"
        params = {
            "grant_type": "authorization_code" ,
            "client_id": self.client_id ,
            "client_secret": self.client_secret ,
            "redirect_uri": self.redirect_url ,
            "code": code
        }
        try:
            response = requests.post( post_url , data=params )
            response.raise_for_status()
            data = response.json()
            id_token = data.get( "id_token" )
            if id_token:
                callback( id_token )
            else:
                callback( "ID token not found in response" )
        except requests.RequestException as e:
            callback( f"Request error: {e}" )

    def decode_jwt(self , id_token: str):
        if not self.public_key:
            raise ValueError( "Public key not set." )

        try:
            decoded_payload = jwt.decode(
                id_token ,
                self.public_key ,
                algorithms=['RS256'] ,
                audience=self.client_id
            )
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise ValueError( "ID token has expired." )
        except jwt.InvalidTokenError as e:
            raise ValueError( f"Invalid ID token: {e}" )

    @staticmethod
    def fetch_user_info(url: str , token: str , callback: Callable[[str] , None]):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get( url , headers=headers )
            response.raise_for_status()
            callback( response.text )
        except requests.RequestException as e:
            callback( f"Request error: {e}" )

