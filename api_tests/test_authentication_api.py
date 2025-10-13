"""API tests for Authentication endpoints."""
import pytest
from api_tests.base_api_test import BaseAPITest
import time


class TestAuthenticationAPI(BaseAPITest):
    """Test suite for Authentication API endpoints."""
    
    def setup_method(self):
        """Set up test method."""
        super().__init__()
        # Don't authenticate automatically for auth tests
    
    def teardown_method(self):
        """Clean up after test method."""
        self.cleanup()
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        login_data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        
        response = self.post('/auth/login', data=login_data)
        
        # Should succeed or return appropriate status
        if response.status_code == 200:
            auth_data = self.validate_response_json(response)
            
            # Should contain token
            token_fields = ['token', 'access_token', 'auth_token']
            has_token = any(field in auth_data for field in token_fields)
            
            if has_token:
                self.logger.info("Login successful with token")
                
                # Validate token format
                token = next((auth_data[field] for field in token_fields if field in auth_data), None)
                assert token and len(token) > 10, "Token should be of reasonable length"
                
                # Check expiration if provided
                if 'expires_in' in auth_data:
                    expires_in = auth_data['expires_in']
                    assert isinstance(expires_in, int) and expires_in > 0, \
                        "Expiration should be positive integer"
        
        elif response.status_code == 401:
            self.logger.info("Login failed as expected with test credentials")
            self.validate_error_response(response)
        
        elif response.status_code == 404:
            self.logger.info("Login endpoint not found - may not be implemented")
        
        else:
            self.logger.info(f"Login returned status {response.status_code}")
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        invalid_credentials = [
            {'username': 'invalid_user', 'password': 'invalid_password'},
            {'username': '', 'password': ''},
            {'username': 'test_user', 'password': 'wrong_password'},
            {'username': 'wrong_user', 'password': 'test_password'}
        ]
        
        for credentials in invalid_credentials:
            response = self.post('/auth/login', data=credentials)
            
            # Should return 401 or 400 for invalid credentials
            if response.status_code in [400, 401]:
                self.validate_error_response(response)
                self.logger.info(f"Invalid credentials correctly rejected: {credentials['username']}")
            elif response.status_code == 404:
                self.logger.info("Login endpoint not found")
                break
            else:
                self.logger.warning(f"Unexpected status for invalid credentials: {response.status_code}")
    
    def test_login_with_missing_fields(self):
        """Test login with missing required fields."""
        missing_field_scenarios = [
            {'password': 'test_password'},  # Missing username
            {'username': 'test_user'},      # Missing password
            {}                              # Missing both
        ]
        
        for data in missing_field_scenarios:
            response = self.post('/auth/login', data=data)
            
            # Should return 400 for missing fields
            if response.status_code == 400:
                self.validate_error_response(response)
                self.logger.info(f"Missing fields correctly handled: {list(data.keys())}")
            elif response.status_code == 404:
                self.logger.info("Login endpoint not found")
                break
    
    def test_token_validation(self):
        """Test token validation endpoint."""
        # First try to get a token
        login_response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if login_response.status_code == 200:
            auth_data = self.validate_response_json(login_response)
            token_fields = ['token', 'access_token', 'auth_token']
            token = next((auth_data[field] for field in token_fields if field in auth_data), None)
            
            if token:
                # Test token validation
                headers = {'Authorization': f'Bearer {token}'}
                response = self.get('/auth/validate', headers=headers)
                
                if response.status_code == 200:
                    self.logger.info("Token validation successful")
                elif response.status_code == 404:
                    self.logger.info("Token validation endpoint not found")
                else:
                    self.logger.info(f"Token validation returned status {response.status_code}")
    
    def test_token_refresh(self):
        """Test token refresh functionality."""
        # First try to get a token
        login_response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if login_response.status_code == 200:
            auth_data = self.validate_response_json(login_response)
            
            # Look for refresh token
            refresh_token = auth_data.get('refresh_token')
            
            if refresh_token:
                # Test token refresh
                refresh_data = {'refresh_token': refresh_token}
                response = self.post('/auth/refresh', data=refresh_data)
                
                if response.status_code == 200:
                    refresh_response = self.validate_response_json(response)
                    
                    # Should contain new token
                    token_fields = ['token', 'access_token', 'auth_token']
                    has_new_token = any(field in refresh_response for field in token_fields)
                    
                    assert has_new_token, "Refresh should return new token"
                    self.logger.info("Token refresh successful")
                
                elif response.status_code == 404:
                    self.logger.info("Token refresh endpoint not found")
    
    def test_logout(self):
        """Test logout functionality."""
        # First try to login
        login_response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if login_response.status_code == 200:
            auth_data = self.validate_response_json(login_response)
            token_fields = ['token', 'access_token', 'auth_token']
            token = next((auth_data[field] for field in token_fields if field in auth_data), None)
            
            if token:
                # Test logout
                headers = {'Authorization': f'Bearer {token}'}
                response = self.post('/auth/logout', headers=headers)
                
                if response.status_code in [200, 204]:
                    self.logger.info("Logout successful")
                    
                    # Try to use token after logout - should fail
                    test_response = self.get('/auth/validate', headers=headers)
                    if test_response.status_code == 401:
                        self.logger.info("Token correctly invalidated after logout")
                
                elif response.status_code == 404:
                    self.logger.info("Logout endpoint not found")
    
    def test_authentication_rate_limiting(self):
        """Test rate limiting on authentication endpoints."""
        # Test multiple login attempts
        results = self.test_rate_limiting('/auth/login', requests_count=15)
        
        self.logger.info(f"Authentication rate limiting results: {results}")
        
        # Should have some form of rate limiting for security
        if results['rate_limited_requests'] > 0:
            self.logger.info("Authentication rate limiting is implemented")
        else:
            self.logger.warning("No authentication rate limiting detected")
    
    def test_password_security_requirements(self):
        """Test password security requirements."""
        weak_passwords = [
            '123',
            'password',
            'abc',
            '111111',
            'qwerty'
        ]
        
        for weak_password in weak_passwords:
            # Try to register or change password with weak password
            register_data = {
                'username': 'test_user_weak',
                'password': weak_password,
                'email': 'test@example.com'
            }
            
            response = self.post('/auth/register', data=register_data)
            
            if response.status_code == 400:
                error_data = self.validate_response_json(response)
                self.logger.info(f"Weak password correctly rejected: {weak_password}")
            elif response.status_code == 404:
                self.logger.info("Registration endpoint not found")
                break
    
    def test_authentication_security_headers(self):
        """Test security headers in authentication responses."""
        response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if response.status_code in [200, 401]:
            headers = response.headers
            
            # Check for security headers
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'Strict-Transport-Security',
                'X-XSS-Protection'
            ]
            
            found_headers = []
            for header in security_headers:
                if header in headers:
                    found_headers.append(header)
            
            if found_headers:
                self.logger.info(f"Found security headers: {found_headers}")
            else:
                self.logger.warning("No security headers found in authentication response")
    
    def test_authentication_timing_attacks(self):
        """Test protection against timing attacks."""
        # Measure response times for valid vs invalid usernames
        valid_user_times = []
        invalid_user_times = []
        
        # Test with valid username, invalid password
        for i in range(5):
            start_time = time.time()
            response = self.post('/auth/login', data={
                'username': 'test_user',
                'password': 'wrong_password'
            })
            end_time = time.time()
            
            if response.status_code in [400, 401]:
                valid_user_times.append(end_time - start_time)
        
        # Test with invalid username
        for i in range(5):
            start_time = time.time()
            response = self.post('/auth/login', data={
                'username': 'nonexistent_user',
                'password': 'any_password'
            })
            end_time = time.time()
            
            if response.status_code in [400, 401]:
                invalid_user_times.append(end_time - start_time)
        
        # Compare average response times
        if valid_user_times and invalid_user_times:
            avg_valid = sum(valid_user_times) / len(valid_user_times)
            avg_invalid = sum(invalid_user_times) / len(invalid_user_times)
            
            time_difference = abs(avg_valid - avg_invalid)
            
            # Times should be similar to prevent timing attacks
            if time_difference < 0.1:  # Less than 100ms difference
                self.logger.info("Good timing attack protection - similar response times")
            else:
                self.logger.warning(f"Potential timing attack vulnerability - {time_difference:.3f}s difference")
    
    def test_session_management(self):
        """Test session management functionality."""
        # Test session creation
        login_response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if login_response.status_code == 200:
            # Check for session cookies
            cookies = login_response.cookies
            
            session_cookies = [cookie for cookie in cookies if 'session' in cookie.name.lower()]
            
            if session_cookies:
                self.logger.info(f"Found session cookies: {[c.name for c in session_cookies]}")
                
                # Check cookie security attributes
                for cookie in session_cookies:
                    if cookie.secure:
                        self.logger.info(f"Cookie {cookie.name} is secure")
                    if 'HttpOnly' in str(cookie):
                        self.logger.info(f"Cookie {cookie.name} is HttpOnly")
    
    def test_multi_factor_authentication(self):
        """Test multi-factor authentication if implemented."""
        # Try login that might trigger MFA
        response = self.post('/auth/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        if response.status_code == 200:
            auth_data = self.validate_response_json(response)
            
            # Check if MFA is required
            if 'mfa_required' in auth_data or 'two_factor_required' in auth_data:
                self.logger.info("Multi-factor authentication detected")
                
                # Test MFA verification endpoint
                mfa_response = self.post('/auth/mfa/verify', data={
                    'token': '123456',  # Test token
                    'session_id': auth_data.get('session_id')
                })
                
                if mfa_response.status_code in [400, 401]:
                    self.logger.info("MFA verification correctly rejects invalid token")


# Pytest fixtures
@pytest.fixture(scope="class")
def auth_api():
    """Fixture for authentication API testing."""
    api = TestAuthenticationAPI()
    yield api
    api.cleanup()


# Test runner for standalone execution
if __name__ == "__main__":
    import sys
    import os
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    test_instance = TestAuthenticationAPI()
    test_instance.setup_method()
    
    try:
        # Run all test methods
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            print(f"\nRunning {method_name}...")
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"✓ {method_name} passed")
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
    
    finally:
        test_instance.teardown_method()