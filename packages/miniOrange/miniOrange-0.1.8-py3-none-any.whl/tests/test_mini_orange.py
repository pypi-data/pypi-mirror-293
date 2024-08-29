import unittest
from unittest.mock import patch, Mock
from src import MiniOrange  # Adjust import as necessary

class TestMiniOrange(unittest.TestCase):

    def setUp(self):
        """Set up the MiniOrange instance for testing."""
        self.mo = MiniOrange()
        self.mo.set_client_id("gOFOPctXqqAZzvU")
        self.mo.set_client_secret("2sgYyB8EOX-HpVi8TpHklUAXUVQ")
        self.mo.set_base_url("https://vk.xecurify.com")
        self.mo.set_redirect_url("http://127.0.0.1:5000/callback")
        self.mo.set_public_key("""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzIKQ+V528e3nGaOL72XA
avmL2HAXwdG5+0Cg2X+ezPfSn2U+DxbYOKFyHXfdCj4ocgF1MKk1ECUDhMlZ6vsl
m7ZPuq9Nus6cYeBxSFdKXaC+vI0hpghkGwAl7a6YT4HAbZ3qs+T7My5gaeuXI1j+
8KBOXK8VRDormzQlI0Q+qbfqUSMCNBMsknxFWfgxvvXSBqEOV2Yq0hbp+JSrsB1S
9DefmvNmxUKLDQ65MmInZ7HqfE+ocWt6H0ba9zISCgjSEs4m0fY6fr99EhuQ9vKX
GcxQfvu2qAOHz0te4yQ67xoUGWzMCmZG3TUTfYz+kFVCSJSrmSnTzkppffio7ooA
owIDAQAB
-----END PUBLIC KEY-----""")

    @patch('src.requests.post')
    def test_request_token_success(self, mock_post):
        """Test successful token request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_token": "mock_token"}
        mock_post.return_value = mock_response

        def callback(result):
            self.assertEqual(result, "mock_token")

        self.mo.request_token("mock_code", callback)

    @patch('src.requests.post')
    def test_request_token_failure(self, mock_post):
        """Test token request failure."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        def callback(result):
            self.assertEqual(result, "ID token not found in response")

        self.mo.request_token("mock_code", callback)

    @patch('src.requests.get')
    def test_fetch_user_info_success(self, mock_get):
        """Test successful user info fetch."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"email": "test@example.com"}'
        mock_get.return_value = mock_response

        def callback(result):
            self.assertEqual(result, '{"email": "test@example.com"}')

        self.mo.fetch_user_info("https://example.com/userinfo", "mock_token", callback)

    @patch('src.requests.get')
    def test_fetch_user_info_failure(self, mock_get):
        """Test failure in fetching user info."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        def callback(result):
            self.assertTrue(result.startswith("Request error"))

        self.mo.fetch_user_info("https://example.com/userinfo", "mock_token", callback)

    def test_start_authorization_missing_parameters(self):
        """Test start authorization when parameters are missing."""
        mo = MiniOrange()
        with patch('src.webbrowser.open') as mock_open:
            with self.assertRaises(ValueError) as context:
                mo.start_authorization()
            self.assertEqual(str(context.exception), "Client ID, Base URL, or Redirect URL is not set")

    @patch('src.webbrowser.open')
    def test_start_authorization_success(self, mock_open):
        """Test start authorization with complete parameters."""
        self.mo.start_authorization()
        expected_url = (
            'https://vk.xecurify.com/moas/idp/openidsso?'
            'client_id=gOFOPctXqqAZzvU&'
            'redirect_uri=http://127.0.0.1:5000/callback&'
            'scope=openid&'
            'response_type=code&'
            'state=yAwL-57K10sIIpGeVO7nR7ZAnzdsj01uGothExyVpmo'
        )
        mock_open.assert_called_once_with(expected_url)

    def test_handle_authorization_response_no_code(self):
        """Test handling of authorization response when no code is present."""
        def callback(result):
            self.assertEqual(result, "No authorization code found.")

        self.mo.handle_authorization_response("https://example.com/lander", callback)

if __name__ == "__main__":
    unittest.main()
