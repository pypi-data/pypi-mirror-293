import unittest
from unittest.mock import patch , Mock
from src import MiniOrange,AuthLibrary


class TestMiniOrange( unittest.TestCase ):

    def setUp(self):
        self.mo = MiniOrange()
        self.mo.set_client_id( "gOFOPctXqqAZzvU" )
        self.mo.set_client_secret( "2sgYyB8EOX-HpVi8TpHklUAXUVQ" )
        self.mo.set_base_url( "https://vk.xecurify.com" )
        self.mo.set_redirect_url( "http://127.0.0.1:5000/callback" )
        self.mo.set_public_key( """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzIKQ+V528e3nGaOL72XA
avmL2HAXwdG5+0Cg2X+ezPfSn2U+DxbYOKFyHXfdCj4ocgF1MKk1ECUDhMlZ6vsl
m7ZPuq9Nus6cYeBxSFdKXaC+vI0hpghkGwAl7a6YT4HAbZ3qs+T7My5gaeuXI1j+
8KBOXK8VRDormzQlI0Q+qbfqUSMCNBMsknxFWfgxvvXSBqEOV2Yq0hbp+JSrsB1S
9DefmvNmxUKLDQ65MmInZ7HqfE+ocWt6H0ba9zISCgjSEs4m0fY6fr99EhuQ9vKX
GcxQfvu2qAOHz0te4yQ67xoUGWzMCmZG3TUTfYz+kFVCSJSrmSnTzkppffio7ooA
owIDAQAB
-----END PUBLIC KEY-----""" )

    @patch( 'src.requests.post' )
    def test_request_token_with_code_success(self , mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_token": "mock_token"}
        mock_post.return_value = mock_response

        def callback(result):
            self.assertEqual( result , "mock_token" )

        self.mo.request_token( "mock_code" , callback )

    @patch( 'src.requests.post' )
    def test_request_token_with_code_failure(self , mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        def callback(result):
            self.assertEqual( result , "ID token not found in response" )

        self.mo.request_token( "mock_code" , callback )

    def test_start_authorization_missing_parameters(self):
        mo = MiniOrange()
        with patch( 'src.webbrowser.open' ) as mock_open:
            with self.assertRaises( ValueError ) as context:
                mo.start_authorization()
            self.assertEqual( str( context.exception ) , "Client ID, Base URL, or Redirect URL is not set" )

    @patch( 'src.webbrowser.open' )
    def test_start_authorization_success(self , mock_open):
        self.mo.start_authorization()
        expected_url = (
            'https://vk.xecurify.com/moas/idp/openidsso?'
            'client_id=gOFOPctXqqAZzvU&'
            'redirect_uri=http://127.0.0.1:5000/callback&'
            'scope=openid&'
            'response_type=code&'
            'state=yAwL-57K10sIIpGeVO7nR7ZAnzdsj01uGothExyVpmo'
        )
        mock_open.assert_called_once_with( expected_url )

    def test_handle_authorization_response_no_code(self):
        def callback(result):
            self.assertEqual( result , "No authorization code found." )

        self.mo.handle_authorization_response( "https://example.com/lander" , callback )


class TestAuthLibrary( unittest.TestCase ):

    def setUp(self):
        self.auth_lib = AuthLibrary(
            token_url='https://example.com/token' ,
            client_id='test_client_id' ,
            client_secret='test_client_secret' ,
            userinfo_url='https://example.com/userinfo'
        )

    @patch( 'requests.post' )
    def test_authenticate_user_success(self , mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_response

        mock_get = Mock()
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'firstname': 'John' ,
            'lastname': 'Doe' ,
            'username': 'johndoe'
        }
        with patch( 'requests.get' , mock_get ):
            userinfo = self.auth_lib.authenticate_user( 'johndoe' , 'password' )

        mock_post.assert_called_once_with(
            'https://example.com/token' ,
            data={
                'grant_type': 'password' ,
                'client_id': 'test_client_id' ,
                'client_secret': 'test_client_secret' ,
                'username': 'johndoe' ,
                'password': 'password'
            } ,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        mock_get.assert_called_once_with(
            'https://example.com/userinfo' ,
            headers={
                'Authorization': 'Bearer test_access_token' ,
                'Accept': 'application/json'
            }
        )

        self.assertEqual( userinfo , {
            'firstname': 'John' ,
            'lastname': 'Doe' ,
            'username': 'johndoe'
        } )

    @patch( 'requests.post' )
    def test_authenticate_user_failure(self , mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Invalid credentials'}
        mock_post.return_value = mock_response

        userinfo = self.auth_lib.authenticate_user( 'johndoe' , 'wrongpassword' )

        self.assertEqual( userinfo ,
                          {'error': 'HTTP error occurred: 400 Client Error: None for url: https://example.com/token'} )

    @patch( 'requests.post' )
    @patch( 'requests.get' )
    def test_login_success(self , mock_get , mock_post):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            'firstname': 'John' ,
            'lastname': 'Doe' ,
            'username': 'johndoe'
        }
        mock_get.return_value = mock_get_response

        result = self.auth_lib.login( 'johndoe' , 'password' )

        self.assertEqual( result , {
            'status': 'success' ,
            'user_info': {
                'firstname': 'John' ,
                'lastname': 'Doe' ,
                'username': 'johndoe'
            }
        } )

    @patch( 'requests.post' )
    def test_login_failure(self , mock_post):
        mock_post_response = Mock()
        mock_post_response.status_code = 400
        mock_post_response.json.return_value = {'error': 'Invalid credentials'}
        mock_post.return_value = mock_post_response

        result = self.auth_lib.login( 'johndoe' , 'wrongpassword' )

        self.assertEqual( result , {
            'status': 'error' ,
            'message': 'HTTP error occurred: 400 Client Error: None for url: https://example.com/token'
        } )


if __name__ == "__main__":
    unittest.main()
