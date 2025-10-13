"""Base API test class for Profitero API testing."""
import requests
import json
import time
from typing import Dict, Any, Optional
from utils.config_reader import config
import logging


class BaseAPITest:
    """Base class for API testing with common functionality."""
    
    def __init__(self):
        """Initialize base API test."""
        self.base_url = config.get_api_base_url()
        self.timeout = config.get('api_timeout', 30)
        self.max_retries = config.get('max_retries', 3)
        self.session = requests.Session()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Profitero-API-Test-Suite/1.0',
            'Accept': 'application/json'
        })
        
        # Authentication token (will be set during authentication)
        self.auth_token = None
    
    def authenticate(self, username: str = None, password: str = None, api_key: str = None) -> bool:
        """Authenticate with the API."""
        try:
            auth_url = f"{self.base_url}/auth/login"
            
            if api_key:
                # API key authentication
                self.session.headers.update({'X-API-Key': api_key})
                return True
            elif username and password:
                # Username/password authentication
                auth_data = {
                    'username': username,
                    'password': password
                }
                
                response = self.session.post(auth_url, json=auth_data, timeout=self.timeout)
                
                if response.status_code == 200:
                    auth_response = response.json()
                    self.auth_token = auth_response.get('token') or auth_response.get('access_token')
                    
                    if self.auth_token:
                        self.session.headers.update({
                            'Authorization': f'Bearer {self.auth_token}'
                        })
                        self.logger.info("Authentication successful")
                        return True
                
                self.logger.error(f"Authentication failed: {response.status_code}")
                return False
            else:
                self.logger.warning("No authentication credentials provided")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Authentication request failed: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    params: Dict = None, headers: Dict = None, 
                    expected_status: int = 200) -> requests.Response:
        """Make HTTP request with retry logic."""
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        # Merge additional headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, headers=request_headers, timeout=self.timeout)
                elif method.upper() == 'POST':
                    response = self.session.post(url, json=data, params=params, headers=request_headers, timeout=self.timeout)
                elif method.upper() == 'PUT':
                    response = self.session.put(url, json=data, params=params, headers=request_headers, timeout=self.timeout)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, params=params, headers=request_headers, timeout=self.timeout)
                elif method.upper() == 'PATCH':
                    response = self.session.patch(url, json=data, params=params, headers=request_headers, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Log request details
                self.logger.info(f"{method.upper()} {url} - Status: {response.status_code}")
                
                return response
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def get(self, endpoint: str, params: Dict = None, headers: Dict = None, 
            expected_status: int = 200) -> requests.Response:
        """Make GET request."""
        return self.make_request('GET', endpoint, params=params, headers=headers, expected_status=expected_status)
    
    def post(self, endpoint: str, data: Dict = None, params: Dict = None, 
             headers: Dict = None, expected_status: int = 201) -> requests.Response:
        """Make POST request."""
        return self.make_request('POST', endpoint, data=data, params=params, headers=headers, expected_status=expected_status)
    
    def put(self, endpoint: str, data: Dict = None, params: Dict = None, 
            headers: Dict = None, expected_status: int = 200) -> requests.Response:
        """Make PUT request."""
        return self.make_request('PUT', endpoint, data=data, params=params, headers=headers, expected_status=expected_status)
    
    def delete(self, endpoint: str, params: Dict = None, headers: Dict = None, 
               expected_status: int = 204) -> requests.Response:
        """Make DELETE request."""
        return self.make_request('DELETE', endpoint, params=params, headers=headers, expected_status=expected_status)
    
    def patch(self, endpoint: str, data: Dict = None, params: Dict = None, 
              headers: Dict = None, expected_status: int = 200) -> requests.Response:
        """Make PATCH request."""
        return self.make_request('PATCH', endpoint, data=data, params=params, headers=headers, expected_status=expected_status)
    
    def validate_response_status(self, response: requests.Response, expected_status: int):
        """Validate response status code."""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"
    
    def validate_response_json(self, response: requests.Response) -> Dict[str, Any]:
        """Validate and return JSON response."""
        try:
            return response.json()
        except json.JSONDecodeError:
            raise AssertionError(f"Response is not valid JSON: {response.text}")
    
    def validate_response_schema(self, response_data: Dict, required_fields: list):
        """Validate response schema has required fields."""
        for field in required_fields:
            assert field in response_data, f"Required field '{field}' not found in response"
    
    def validate_response_time(self, response: requests.Response, max_time: float = 5.0):
        """Validate response time is within acceptable limits."""
        response_time = response.elapsed.total_seconds()
        assert response_time <= max_time, \
            f"Response time {response_time:.2f}s exceeds maximum {max_time}s"
    
    def validate_pagination(self, response_data: Dict):
        """Validate pagination metadata."""
        pagination_fields = ['page', 'limit', 'total', 'pages']
        
        for field in pagination_fields:
            if field in response_data:
                value = response_data[field]
                assert isinstance(value, int) and value >= 0, \
                    f"Pagination field '{field}' should be non-negative integer, got {value}"
    
    def validate_error_response(self, response: requests.Response):
        """Validate error response format."""
        assert response.status_code >= 400, "Should be an error response"
        
        try:
            error_data = response.json()
            error_fields = ['error', 'message', 'detail', 'description']
            
            has_error_field = any(field in error_data for field in error_fields)
            assert has_error_field, "Error response should contain error information"
            
        except json.JSONDecodeError:
            # If not JSON, should at least have some text
            assert response.text, "Error response should contain error information"
    
    def test_endpoint_health(self, endpoint: str) -> bool:
        """Test if endpoint is healthy and responsive."""
        try:
            response = self.get(endpoint)
            return 200 <= response.status_code < 300
        except Exception:
            return False
    
    def test_rate_limiting(self, endpoint: str, requests_count: int = 10) -> Dict[str, Any]:
        """Test rate limiting on endpoint."""
        results = {
            'total_requests': requests_count,
            'successful_requests': 0,
            'rate_limited_requests': 0,
            'error_requests': 0,
            'response_times': []
        }
        
        for i in range(requests_count):
            try:
                start_time = time.time()
                response = self.get(endpoint)
                end_time = time.time()
                
                response_time = end_time - start_time
                results['response_times'].append(response_time)
                
                if response.status_code == 200:
                    results['successful_requests'] += 1
                elif response.status_code == 429:
                    results['rate_limited_requests'] += 1
                else:
                    results['error_requests'] += 1
                
                # Small delay between requests
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Rate limiting test request {i+1} failed: {e}")
                results['error_requests'] += 1
        
        results['average_response_time'] = sum(results['response_times']) / len(results['response_times']) if results['response_times'] else 0
        
        return results
    
    def test_concurrent_requests(self, endpoint: str, concurrent_count: int = 5) -> Dict[str, Any]:
        """Test concurrent requests to endpoint."""
        import threading
        import queue
        
        results_queue = queue.Queue()
        
        def make_concurrent_request():
            try:
                start_time = time.time()
                response = self.get(endpoint)
                end_time = time.time()
                
                results_queue.put({
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'success': 200 <= response.status_code < 300
                })
            except Exception as e:
                results_queue.put({
                    'error': str(e),
                    'success': False
                })
        
        # Create and start threads
        threads = []
        for i in range(concurrent_count):
            thread = threading.Thread(target=make_concurrent_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        results = {
            'total_requests': concurrent_count,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': []
        }
        
        while not results_queue.empty():
            result = results_queue.get()
            if result.get('success'):
                results['successful_requests'] += 1
                if 'response_time' in result:
                    results['response_times'].append(result['response_time'])
            else:
                results['failed_requests'] += 1
        
        results['average_response_time'] = sum(results['response_times']) / len(results['response_times']) if results['response_times'] else 0
        
        return results
    
    def cleanup(self):
        """Clean up resources."""
        if self.session:
            self.session.close()
            self.logger.info("API session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()