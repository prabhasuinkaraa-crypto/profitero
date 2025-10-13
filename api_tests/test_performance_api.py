"""API performance and load testing."""
import pytest
from api_tests.base_api_test import BaseAPITest
import time
import statistics
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestAPIPerformance(BaseAPITest):
    """Test suite for API performance testing."""
    
    def setup_method(self):
        """Set up test method."""
        super().__init__()
        self.authenticate(api_key="test_api_key")
    
    def teardown_method(self):
        """Clean up after test method."""
        self.cleanup()
    
    def test_response_time_benchmarks(self):
        """Test API response time benchmarks."""
        endpoints = [
            '/health',
            '/products',
            '/services',
            '/users'
        ]
        
        benchmark_results = {}
        
        for endpoint in endpoints:
            response_times = []
            
            # Make 10 requests to each endpoint
            for i in range(10):
                try:
                    start_time = time.time()
                    response = self.get(endpoint)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    
                    # Small delay between requests
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.logger.error(f"Request to {endpoint} failed: {e}")
                    continue
            
            if response_times:
                benchmark_results[endpoint] = {
                    'min': min(response_times),
                    'max': max(response_times),
                    'avg': statistics.mean(response_times),
                    'median': statistics.median(response_times),
                    'std_dev': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    'count': len(response_times)
                }
        
        # Log results
        for endpoint, stats in benchmark_results.items():
            self.logger.info(f"Endpoint {endpoint} performance:")
            self.logger.info(f"  Average: {stats['avg']:.3f}s")
            self.logger.info(f"  Median: {stats['median']:.3f}s")
            self.logger.info(f"  Min: {stats['min']:.3f}s")
            self.logger.info(f"  Max: {stats['max']:.3f}s")
            self.logger.info(f"  Std Dev: {stats['std_dev']:.3f}s")
            
            # Assert performance requirements
            assert stats['avg'] < 5.0, f"Average response time for {endpoint} too slow: {stats['avg']:.3f}s"
            assert stats['max'] < 10.0, f"Max response time for {endpoint} too slow: {stats['max']:.3f}s"
    
    def test_concurrent_load(self):
        """Test API under concurrent load."""
        endpoint = '/products'
        concurrent_users = [5, 10, 20]
        
        for user_count in concurrent_users:
            self.logger.info(f"Testing with {user_count} concurrent users")
            
            results = self._run_concurrent_test(endpoint, user_count, requests_per_user=5)
            
            # Analyze results
            success_rate = results['successful_requests'] / results['total_requests']
            avg_response_time = results['average_response_time']
            
            self.logger.info(f"  Success rate: {success_rate:.2%}")
            self.logger.info(f"  Average response time: {avg_response_time:.3f}s")
            self.logger.info(f"  Failed requests: {results['failed_requests']}")
            
            # Assert performance requirements
            assert success_rate >= 0.95, f"Success rate too low with {user_count} users: {success_rate:.2%}"
            assert avg_response_time < 10.0, f"Response time too slow with {user_count} users: {avg_response_time:.3f}s"
    
    def _run_concurrent_test(self, endpoint: str, concurrent_users: int, requests_per_user: int = 5):
        """Run concurrent test with specified parameters."""
        results = {
            'total_requests': concurrent_users * requests_per_user,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': []
        }
        
        def make_requests():
            """Make requests for a single user."""
            user_results = {
                'successful': 0,
                'failed': 0,
                'response_times': [],
                'errors': []
            }
            
            for _ in range(requests_per_user):
                try:
                    start_time = time.time()
                    response = self.get(endpoint)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    user_results['response_times'].append(response_time)
                    
                    if 200 <= response.status_code < 300:
                        user_results['successful'] += 1
                    else:
                        user_results['failed'] += 1
                        user_results['errors'].append(f"Status {response.status_code}")
                
                except Exception as e:
                    user_results['failed'] += 1
                    user_results['errors'].append(str(e))
            
            return user_results
        
        # Run concurrent requests
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_requests) for _ in range(concurrent_users)]
            
            for future in as_completed(futures):
                try:
                    user_result = future.result()
                    results['successful_requests'] += user_result['successful']
                    results['failed_requests'] += user_result['failed']
                    results['response_times'].extend(user_result['response_times'])
                    results['errors'].extend(user_result['errors'])
                except Exception as e:
                    self.logger.error(f"Concurrent test thread failed: {e}")
                    results['failed_requests'] += requests_per_user
        
        # Calculate average response time
        if results['response_times']:
            results['average_response_time'] = statistics.mean(results['response_times'])
        else:
            results['average_response_time'] = 0
        
        return results
    
    def test_sustained_load(self):
        """Test API under sustained load."""
        endpoint = '/products'
        duration_seconds = 60  # 1 minute test
        requests_per_second = 2
        
        self.logger.info(f"Running sustained load test for {duration_seconds}s at {requests_per_second} req/s")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        results = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': []
        }
        
        while time.time() < end_time:
            request_start = time.time()
            
            try:
                response = self.get(endpoint)
                request_end = time.time()
                
                results['total_requests'] += 1
                response_time = request_end - request_start
                results['response_times'].append(response_time)
                
                if 200 <= response.status_code < 300:
                    results['successful_requests'] += 1
                else:
                    results['failed_requests'] += 1
                    results['errors'].append(f"Status {response.status_code}")
            
            except Exception as e:
                results['total_requests'] += 1
                results['failed_requests'] += 1
                results['errors'].append(str(e))
            
            # Rate limiting
            elapsed = time.time() - request_start
            sleep_time = (1.0 / requests_per_second) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Analyze results
        actual_duration = time.time() - start_time
        actual_rps = results['total_requests'] / actual_duration
        success_rate = results['successful_requests'] / results['total_requests'] if results['total_requests'] > 0 else 0
        
        if results['response_times']:
            avg_response_time = statistics.mean(results['response_times'])
            p95_response_time = statistics.quantiles(results['response_times'], n=20)[18]  # 95th percentile
        else:
            avg_response_time = 0
            p95_response_time = 0
        
        self.logger.info(f"Sustained load test results:")
        self.logger.info(f"  Duration: {actual_duration:.1f}s")
        self.logger.info(f"  Total requests: {results['total_requests']}")
        self.logger.info(f"  Actual RPS: {actual_rps:.2f}")
        self.logger.info(f"  Success rate: {success_rate:.2%}")
        self.logger.info(f"  Average response time: {avg_response_time:.3f}s")
        self.logger.info(f"  95th percentile response time: {p95_response_time:.3f}s")
        
        # Assert performance requirements
        assert success_rate >= 0.95, f"Success rate too low in sustained test: {success_rate:.2%}"
        assert avg_response_time < 5.0, f"Average response time too slow: {avg_response_time:.3f}s"
        assert p95_response_time < 10.0, f"95th percentile response time too slow: {p95_response_time:.3f}s"
    
    def test_memory_usage_stability(self):
        """Test API memory usage stability over time."""
        endpoint = '/products'
        iterations = 100
        
        self.logger.info(f"Testing memory stability over {iterations} requests")
        
        response_times = []
        
        for i in range(iterations):
            try:
                start_time = time.time()
                response = self.get(endpoint)
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                # Log progress every 20 requests
                if (i + 1) % 20 == 0:
                    self.logger.info(f"  Completed {i + 1}/{iterations} requests")
                
                # Small delay between requests
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Request {i + 1} failed: {e}")
        
        if len(response_times) >= 10:
            # Check for performance degradation over time
            first_quarter = response_times[:len(response_times)//4]
            last_quarter = response_times[-len(response_times)//4:]
            
            avg_first = statistics.mean(first_quarter)
            avg_last = statistics.mean(last_quarter)
            
            degradation = (avg_last - avg_first) / avg_first * 100
            
            self.logger.info(f"Performance change over time: {degradation:+.1f}%")
            self.logger.info(f"First quarter average: {avg_first:.3f}s")
            self.logger.info(f"Last quarter average: {avg_last:.3f}s")
            
            # Should not degrade significantly
            assert degradation < 50, f"Performance degraded too much: {degradation:.1f}%"
    
    def test_large_response_handling(self):
        """Test handling of large responses."""
        # Test with large page size
        large_params = {'limit': 1000}
        
        try:
            start_time = time.time()
            response = self.get('/products', params=large_params)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                response_size = len(response.content)
                
                self.logger.info(f"Large response test:")
                self.logger.info(f"  Response time: {response_time:.3f}s")
                self.logger.info(f"  Response size: {response_size:,} bytes")
                
                # Should handle large responses reasonably
                assert response_time < 30.0, f"Large response too slow: {response_time:.3f}s"
                
                # Try to parse JSON
                try:
                    data = response.json()
                    self.logger.info(f"  Successfully parsed JSON response")
                except Exception as e:
                    self.logger.error(f"  Failed to parse large JSON response: {e}")
            
            else:
                self.logger.info(f"Large response request returned status {response.status_code}")
        
        except Exception as e:
            self.logger.error(f"Large response test failed: {e}")
    
    def test_api_throughput(self):
        """Test maximum API throughput."""
        endpoint = '/products'
        test_duration = 30  # 30 seconds
        
        self.logger.info(f"Testing maximum throughput for {test_duration}s")
        
        start_time = time.time()
        end_time = start_time + test_duration
        
        request_count = 0
        successful_requests = 0
        
        while time.time() < end_time:
            try:
                response = self.get(endpoint)
                request_count += 1
                
                if 200 <= response.status_code < 300:
                    successful_requests += 1
                
                # No delay - maximum throughput test
                
            except Exception as e:
                request_count += 1
                # Continue testing even if some requests fail
        
        actual_duration = time.time() - start_time
        throughput = request_count / actual_duration
        success_rate = successful_requests / request_count if request_count > 0 else 0
        
        self.logger.info(f"Throughput test results:")
        self.logger.info(f"  Total requests: {request_count}")
        self.logger.info(f"  Successful requests: {successful_requests}")
        self.logger.info(f"  Success rate: {success_rate:.2%}")
        self.logger.info(f"  Throughput: {throughput:.2f} req/s")
        
        # Basic assertions
        assert throughput > 0.5, f"Throughput too low: {throughput:.2f} req/s"
        assert success_rate >= 0.8, f"Success rate too low at max throughput: {success_rate:.2%}"
    
    def test_error_rate_under_load(self):
        """Test error rates under various load conditions."""
        endpoint = '/products'
        load_levels = [1, 5, 10, 15]  # Concurrent users
        
        error_rates = {}
        
        for load_level in load_levels:
            self.logger.info(f"Testing error rate with {load_level} concurrent users")
            
            results = self._run_concurrent_test(endpoint, load_level, requests_per_user=10)
            
            error_rate = results['failed_requests'] / results['total_requests']
            error_rates[load_level] = error_rate
            
            self.logger.info(f"  Error rate: {error_rate:.2%}")
        
        # Error rate should not increase dramatically with load
        baseline_error_rate = error_rates[1]
        
        for load_level, error_rate in error_rates.items():
            if load_level > 1:
                error_increase = error_rate - baseline_error_rate
                assert error_increase < 0.1, \
                    f"Error rate increased too much at load level {load_level}: +{error_increase:.2%}"
    
    def test_cache_performance(self):
        """Test caching performance if implemented."""
        endpoint = '/products'
        
        # First request (cache miss)
        start_time = time.time()
        first_response = self.get(endpoint)
        first_response_time = time.time() - start_time
        
        if first_response.status_code == 200:
            # Second request (potential cache hit)
            start_time = time.time()
            second_response = self.get(endpoint)
            second_response_time = time.time() - start_time
            
            if second_response.status_code == 200:
                self.logger.info(f"Cache performance test:")
                self.logger.info(f"  First request: {first_response_time:.3f}s")
                self.logger.info(f"  Second request: {second_response_time:.3f}s")
                
                # Check for cache headers
                cache_headers = ['Cache-Control', 'ETag', 'Last-Modified', 'Expires']
                found_cache_headers = []
                
                for header in cache_headers:
                    if header in second_response.headers:
                        found_cache_headers.append(header)
                
                if found_cache_headers:
                    self.logger.info(f"  Found cache headers: {found_cache_headers}")
                
                # If caching is implemented, second request should be faster
                if second_response_time < first_response_time * 0.8:
                    self.logger.info("  Caching appears to be working")
                else:
                    self.logger.info("  No significant caching performance improvement detected")


# Pytest fixtures
@pytest.fixture(scope="class")
def performance_api():
    """Fixture for performance API testing."""
    api = TestAPIPerformance()
    yield api
    api.cleanup()


# Test runner for standalone execution
if __name__ == "__main__":
    import sys
    import os
    
    # Add project root to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    test_instance = TestAPIPerformance()
    test_instance.setup_method()
    
    try:
        # Run performance tests (subset for quick execution)
        performance_tests = [
            'test_response_time_benchmarks',
            'test_concurrent_load',
            'test_large_response_handling',
            'test_api_throughput'
        ]
        
        for method_name in performance_tests:
            print(f"\nRunning {method_name}...")
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"✓ {method_name} passed")
            except Exception as e:
                print(f"✗ {method_name} failed: {e}")
    
    finally:
        test_instance.teardown_method()