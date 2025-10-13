"""API tests for Products endpoints."""
import pytest
from api_tests.base_api_test import BaseAPITest
import json


class TestProductsAPI(BaseAPITest):
    """Test suite for Products API endpoints."""
    
    def setup_method(self):
        """Set up test method."""
        super().__init__()
        # Authenticate if credentials are available
        self.authenticate(api_key="test_api_key")
    
    def teardown_method(self):
        """Clean up after test method."""
        self.cleanup()
    
    def test_get_all_products(self):
        """Test getting all products."""
        response = self.get('/products')
        
        # Validate response
        self.validate_response_status(response, 200)
        self.validate_response_time(response, 5.0)
        
        # Validate JSON response
        products_data = self.validate_response_json(response)
        
        # Validate response structure
        if isinstance(products_data, list):
            products = products_data
        elif isinstance(products_data, dict):
            products = products_data.get('products', products_data.get('data', []))
        else:
            pytest.fail("Invalid products response structure")
        
        # Validate product structure
        if len(products) > 0:
            product = products[0]
            required_fields = ['id', 'name', 'description']
            self.validate_response_schema(product, required_fields)
    
    def test_get_products_with_pagination(self):
        """Test getting products with pagination."""
        params = {'page': 1, 'limit': 10}
        response = self.get('/products', params=params)
        
        self.validate_response_status(response, 200)
        products_data = self.validate_response_json(response)
        
        # Validate pagination
        self.validate_pagination(products_data)
    
    def test_get_products_with_filters(self):
        """Test getting products with filters."""
        filter_params = [
            {'category': 'analytics'},
            {'status': 'active'},
            {'name': 'digital'}
        ]
        
        for params in filter_params:
            response = self.get('/products', params=params)
            
            # Should either return filtered results or handle gracefully
            assert response.status_code in [200, 400, 404], \
                f"Unexpected status code for filter {params}: {response.status_code}"
            
            if response.status_code == 200:
                products_data = self.validate_response_json(response)
                self.logger.info(f"Filter {params} returned data successfully")
    
    def test_get_single_product(self):
        """Test getting a single product by ID."""
        # First get all products to find a valid ID
        response = self.get('/products')
        
        if response.status_code == 200:
            products_data = self.validate_response_json(response)
            
            if isinstance(products_data, list) and len(products_data) > 0:
                product_id = products_data[0].get('id')
            elif isinstance(products_data, dict):
                products = products_data.get('products', products_data.get('data', []))
                if len(products) > 0:
                    product_id = products[0].get('id')
                else:
                    product_id = None
            else:
                product_id = None
            
            if product_id:
                # Test getting single product
                single_response = self.get(f'/products/{product_id}')
                
                if single_response.status_code == 200:
                    product_data = self.validate_response_json(single_response)
                    assert product_data.get('id') == product_id, "Product ID should match"
                    
                    required_fields = ['id', 'name', 'description']
                    self.validate_response_schema(product_data, required_fields)
    
    def test_get_nonexistent_product(self):
        """Test getting a non-existent product."""
        response = self.get('/products/nonexistent-id')
        
        # Should return 404 for non-existent product
        assert response.status_code in [404, 400], \
            f"Expected 404 or 400 for non-existent product, got {response.status_code}"
        
        if response.status_code >= 400:
            self.validate_error_response(response)
    
    def test_products_api_performance(self):
        """Test products API performance."""
        # Test response time
        response = self.get('/products')
        self.validate_response_time(response, 3.0)  # Should respond within 3 seconds
        
        # Test with large page size
        params = {'limit': 100}
        response = self.get('/products', params=params)
        
        if response.status_code == 200:
            self.validate_response_time(response, 10.0)  # Allow more time for large response
    
    def test_products_api_rate_limiting(self):
        """Test rate limiting on products API."""
        results = self.test_rate_limiting('/products', requests_count=20)
        
        self.logger.info(f"Rate limiting test results: {results}")
        
        # Should have some successful requests
        assert results['successful_requests'] > 0, "Should have at least some successful requests"
        
        # If rate limiting is implemented, should see some 429 responses
        if results['rate_limited_requests'] > 0:
            self.logger.info(f"Rate limiting detected: {results['rate_limited_requests']} requests limited")
    
    def test_products_api_concurrent_requests(self):
        """Test concurrent requests to products API."""
        results = self.test_concurrent_requests('/products', concurrent_count=10)
        
        self.logger.info(f"Concurrent requests test results: {results}")
        
        # Most requests should succeed
        success_rate = results['successful_requests'] / results['total_requests']
        assert success_rate >= 0.8, f"Success rate too low: {success_rate:.2%}"
    
    def test_products_api_error_handling(self):
        """Test error handling in products API."""
        error_scenarios = [
            {'endpoint': '/products', 'params': {'limit': 'invalid'}, 'expected_status': 400},
            {'endpoint': '/products', 'params': {'page': -1}, 'expected_status': 400},
            {'endpoint': '/products/invalid-format-id', 'params': {}, 'expected_status': 400},
        ]
        
        for scenario in error_scenarios:
            response = self.get(scenario['endpoint'], params=scenario['params'])
            
            # Should return appropriate error status
            assert response.status_code >= 400, \
                f"Expected error status for {scenario}, got {response.status_code}"
            
            # Validate error response format
            self.validate_error_response(response)
    
    def test_products_api_data_consistency(self):
        """Test data consistency in products API."""
        # Make multiple requests and compare results
        responses = []
        
        for i in range(3):
            response = self.get('/products')
            if response.status_code == 200:
                responses.append(self.validate_response_json(response))
        
        if len(responses) > 1:
            # Compare first response with others
            first_response = responses[0]
            
            for i, response in enumerate(responses[1:], 2):
                # Basic consistency check - structure should be the same
                assert type(response) == type(first_response), \
                    f"Response {i} has different type than first response"
                
                if isinstance(response, dict) and isinstance(first_response, dict):
                    # Check that both have same top-level keys
                    assert set(response.keys()) == set(first_response.keys()), \
                        f"Response {i} has different keys than first response"
    
    def test_products_api_security(self):
        """Test security aspects of products API."""
        # Test without authentication
        unauthenticated_session = BaseAPITest()
        
        response = unauthenticated_session.get('/products')
        
        # Depending on API design, should either work (public endpoint) or require auth
        if response.status_code == 401:
            self.logger.info("Products API requires authentication")
            self.validate_error_response(response)
        elif response.status_code == 200:
            self.logger.info("Products API is publicly accessible")
        
        unauthenticated_session.cleanup()
        
        # Test SQL injection attempt
        malicious_params = {'id': "1' OR '1'='1"}
        response = self.get('/products', params=malicious_params)
        
        # Should not return unexpected results
        assert response.status_code in [200, 400, 404], \
            "SQL injection attempt should be handled safely"
    
    def test_products_api_headers(self):
        """Test API response headers."""
        response = self.get('/products')
        
        if response.status_code == 200:
            headers = response.headers
            
            # Check for security headers
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'Content-Type'
            ]
            
            for header in security_headers:
                if header in headers:
                    self.logger.info(f"Found security header: {header}")
            
            # Content-Type should be JSON
            content_type = headers.get('Content-Type', '')
            assert 'application/json' in content_type, \
                f"Expected JSON content type, got {content_type}"
    
    def test_products_api_versioning(self):
        """Test API versioning support."""
        version_tests = [
            {'path': '/v1/products', 'header': None},
            {'path': '/v2/products', 'header': None},
            {'path': '/products', 'header': {'API-Version': 'v1'}},
            {'path': '/products', 'header': {'API-Version': 'v2'}},
        ]
        
        for test in version_tests:
            response = self.get(test['path'], headers=test['header'])
            
            if response.status_code == 200:
                self.logger.info(f"API version test successful: {test}")
            elif response.status_code == 404:
                self.logger.info(f"API version not found: {test}")
            else:
                self.logger.info(f"API version test status {response.status_code}: {test}")


# Pytest fixtures and configuration
@pytest.fixture(scope="class")
def products_api():
    """Fixture for products API testing."""
    api = TestProductsAPI()
    yield api
    api.cleanup()


# Test runner for standalone execution
if __name__ == "__main__":
    import sys
    import os
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    test_instance = TestProductsAPI()
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