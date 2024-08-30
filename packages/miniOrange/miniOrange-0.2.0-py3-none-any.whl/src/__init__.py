import webbrowser

import requests
import jwt
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from typing import Callable , Optional
import requests
from urllib.parse import urlparse , parse_qs


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
        webbrowser.open( auth_url )
        return auth_url

    def handle_authorization_response(self , uri: str , callback: Callable[[str] , None]):
        if not self.client_id or not self.client_secret:
            callback( "Client ID or Client Secret not set" )
            return

        parsed_uri = urlparse( uri )
        if parsed_uri.path.startswith( f"{self.base_url}/lander" ):
            query_params = parse_qs( parsed_uri.query )
            code = query_params.get( "code" , [None] )[0]
            if code:
                self.request_token( code , callback )

    def request_token(self , code: str , callback: Callable[[str] , None]):
        if not self.client_id or not self.client_secret or not self.redirect_url:
            callback( "Client ID, Client Secret, or Redirect URL not set" )
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
            raise ValueError( "Public key not set" )

        try:
            decoded_payload = jwt.decode(
                id_token ,
                self.public_key ,
                algorithms=['RS256'] ,
                audience=self.client_id
            )
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise ValueError( "ID token has expired" )
        except jwt.InvalidTokenError as e:
            raise ValueError( f"Invalid ID token: {e}" )


class AuthLibrary:
    def __init__(self , token_url , client_id , client_secret , userinfo_url):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.userinfo_url = userinfo_url

    def authenticate_user(self , username , password):
        """Authenticate user and handle tokens."""
        data = {
            'grant_type': 'password' ,
            'client_id': self.client_id ,
            'client_secret': self.client_secret ,
            'username': username ,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            res = requests.post( self.token_url , data=data , headers=headers )
            res.raise_for_status()

            token_data = res.json()
            access_token = token_data.get( 'access_token' )

            if access_token:
                userinfo_headers = {
                    'Authorization': f'Bearer {access_token}' ,
                    'Accept': 'application/json'
                }
                userinfo_res = requests.get( self.userinfo_url , headers=userinfo_headers )
                userinfo_res.raise_for_status()

                userinfo = userinfo_res.json()
                return userinfo

            else:
                return {"error": "Access token not found."}

        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.RequestException as err:
            return {"error": f"Request exception occurred: {err}"}

    def login(self , username , password):
        """Authenticate and return user info or error message."""
        userinfo = self.authenticate_user( username , password )

        if 'error' not in userinfo:
            return {"status": "success" , "user_info": userinfo}
        else:
            return {"status": "error" , "message": userinfo.get( 'error' , "An error occurred." )}
