import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from typing import Callable
import requests
from urllib.parse import urlparse, parse_qs

import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
class MiniOrange:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.base_url = None
        self.redirect_url = None
        self.public_key = None

    def set_client_id(self, client_id: str):
        self.client_id = client_id

    def set_client_secret(self, client_secret: str):
        self.client_secret = client_secret

    def set_base_url(self, base_url: str):
        self.base_url = base_url

    def set_redirect_url(self, redirect_url: str):
        self.redirect_url = redirect_url

    def set_public_key(self, public_key_pem: str):
        self.public_key = self.load_public_key(public_key_pem)

    @staticmethod
    def load_public_key(pem_data: str):
        try:
            public_key = load_pem_public_key( pem_data.encode() , backend=default_backend() )
            return public_key
        except ValueError as e:
            raise ValueError( f"Error loading public key: {e}" )

    def start_authorization(self):
        if not all([self.client_id, self.base_url, self.redirect_url]):
            raise ValueError("Client ID, Base URL, or Redirect URL is not set")

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

    def handle_authorization_response(self, uri: str, callback: Callable[[str], None]) -> str:
        if not self.client_id or not self.client_secret:
            return "Client ID or Client Secret not set"

        parsed_uri = urlparse(uri)
        logging.debug(f"Parsed URI: {parsed_uri}")

        if parsed_uri.path == "/callback":
            query_params = parse_qs(parsed_uri.query)
            code = query_params.get("code", [None])[0]
            logging.debug(f"Authorization code: {code}")
            if code:
                return self.request_token(code, callback)
            else:
                return "Authorization code not found"
        else:
            return "Invalid callback URL"

    def request_token(self, code: str, callback: Callable[[str], None]) -> str:
        if not self.client_id or not self.client_secret or not self.redirect_url:
            return "Client ID, Client Secret, or Redirect URL not set"

        post_url = f"{self.base_url}/moas/rest/oauth/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_url,
            "code": code
        }
        logging.debug(f"Requesting token from URL: {post_url} with params: {params}")
        try:
            response = requests.post(post_url, data=params)
            response.raise_for_status()
            data = response.json()
            logging.debug(f"Token response: {data}")
            id_token = data.get("id_token")
            if id_token:
                logging.debug(f"ID token received: {id_token}")
                return id_token
            else:
                return "ID token not found in response"
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            return f"Request error: {e}"

    def decode_jwt(self , id_token: str):
        if not self.public_key:
            raise ValueError( "Public key not set" )

        if not id_token:
            raise ValueError( "ID token is None or empty" )

        try:
            decoded_payload = jwt.decode(
                id_token ,
                self.public_key ,
                algorithms=['RS256'] ,
                audience=self.client_id
            )
            return decoded_payload
        except ExpiredSignatureError:
            logging.error( "ID token has expired" )
            raise ValueError( "ID token has expired" )
        except InvalidTokenError as e:
            logging.error( f"Invalid ID token: {e}" )
            raise ValueError( f"Invalid ID token: {e}" )
        except Exception as e:
            logging.error( f"Unexpected error decoding JWT: {e}" )
            raise ValueError( f"Unexpected error decoding JWT: {e}" )
class AuthLibrary:
    def __init__(self, token_url, client_id, client_secret, userinfo_url):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.userinfo_url = userinfo_url

    def authenticate_user(self, username, password):
        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            res = requests.post(self.token_url, data=data, headers=headers)
            res.raise_for_status()

            token_data = res.json()
            access_token = token_data.get('access_token')

            if access_token:
                userinfo_headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/json'
                }
                userinfo_res = requests.get(self.userinfo_url, headers=userinfo_headers)
                userinfo_res.raise_for_status()

                userinfo = userinfo_res.json()
                return userinfo

            else:
                return {"error": "Access token not found."}

        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.RequestException as err:
            return {"error": f"Request exception occurred: {err}"}

    def login(self, username, password):
        userinfo = self.authenticate_user(username, password)

        if 'error' not in userinfo:
            return {"status": "success", "user_info": userinfo}
        else:
            return {"status": "error", "message": userinfo.get('error', "An error occurred.")}
