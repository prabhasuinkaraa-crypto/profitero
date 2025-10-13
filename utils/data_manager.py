"""Data management utilities for test framework."""
import json
import os
import csv
import random
from typing import Dict, List, Any, Optional
from faker import Faker
from utils.config_reader import config
import logging


class DataManager:
    """Manage test data for various test scenarios."""
    
    def __init__(self):
        """Initialize data manager."""
        self.test_data_path = config.get_test_data_path()
        self.faker = Faker()
        self.logger = logging.getLogger(__name__)
        
        # Ensure test data directory exists
        os.makedirs(self.test_data_path, exist_ok=True)
    
    def load_json_data(self, filename: str) -> Dict[str, Any]:
        """Load JSON test data from file."""
        filepath = os.path.join(self.test_data_path, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded test data from {filename}")
            return data
        except FileNotFoundError:
            self.logger.error(f"Test data file not found: {filename}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON data from {filename}: {e}")
            return {}
    
    def save_json_data(self, data: Dict[str, Any], filename: str):
        """Save data to JSON file."""
        filepath = os.path.join(self.test_data_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved test data to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving data to {filename}: {e}")
    
    def load_csv_data(self, filename: str) -> List[Dict[str, Any]]:
        """Load CSV test data from file."""
        filepath = os.path.join(self.test_data_path, filename)
        
        try:
            data = []
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            self.logger.info(f"Loaded {len(data)} rows from {filename}")
            return data
        except FileNotFoundError:
            self.logger.error(f"CSV file not found: {filename}")
            return []
        except Exception as e:
            self.logger.error(f"Error reading CSV file {filename}: {e}")
            return []
    
    def get_test_users(self, user_type: str = "valid") -> List[Dict[str, Any]]:
        """Get test user data."""
        users_data = self.load_json_data("test_users.json")
        
        if user_type == "valid":
            return users_data.get("valid_users", [])
        elif user_type == "invalid":
            return users_data.get("invalid_users", [])
        elif user_type == "special":
            return users_data.get("special_characters_users", [])
        else:
            return users_data.get("valid_users", [])
    
    def get_random_user(self, user_type: str = "valid") -> Dict[str, Any]:
        """Get a random test user."""
        users = self.get_test_users(user_type)
        return random.choice(users) if users else {}
    
    def get_contact_form_data(self, data_type: str = "valid") -> List[Dict[str, Any]]:
        """Get contact form test data."""
        contact_data = self.load_json_data("contact_form_data.json")
        
        data_key = f"{data_type}_contact_data"
        return contact_data.get(data_key, [])
    
    def get_random_contact_data(self, data_type: str = "valid") -> Dict[str, Any]:
        """Get random contact form data."""
        contact_data = self.get_contact_form_data(data_type)
        return random.choice(contact_data) if contact_data else {}
    
    def get_product_data(self, data_type: str = "sample") -> List[Dict[str, Any]]:
        """Get product test data."""
        products_data = self.load_json_data("test_products.json")
        
        if data_type == "sample":
            return products_data.get("sample_products", [])
        elif data_type == "invalid":
            return products_data.get("invalid_products", [])
        else:
            return products_data.get("sample_products", [])
    
    def get_api_test_data(self, category: str) -> Dict[str, Any]:
        """Get API test data by category."""
        api_data = self.load_json_data("api_test_data.json")
        return api_data.get(category, {})
    
    def generate_fake_user(self) -> Dict[str, Any]:
        """Generate fake user data using Faker."""
        return {
            "id": f"fake_{self.faker.uuid4()}",
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "password": self.faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "company": self.faker.company(),
            "phone": self.faker.phone_number(),
            "address": {
                "street": self.faker.street_address(),
                "city": self.faker.city(),
                "state": self.faker.state(),
                "country": self.faker.country(),
                "postal_code": self.faker.postcode()
            },
            "role": random.choice(["user", "admin", "manager"])
        }
    
    def generate_fake_contact_data(self) -> Dict[str, Any]:
        """Generate fake contact form data."""
        return {
            "id": f"fake_contact_{self.faker.uuid4()}",
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "email": self.faker.email(),
            "company": self.faker.company(),
            "phone": self.faker.phone_number(),
            "subject": self.faker.sentence(nb_words=6),
            "message": self.faker.text(max_nb_chars=500),
            "country": self.faker.country(),
            "industry": random.choice([
                "Technology", "Healthcare", "Finance", "Retail", "Manufacturing",
                "Education", "Government", "Non-profit", "Consulting", "Other"
            ]),
            "company_size": random.choice([
                "1-10 employees", "11-50 employees", "51-200 employees",
                "201-500 employees", "501-1000 employees", "1000+ employees"
            ])
        }
    
    def generate_fake_product(self) -> Dict[str, Any]:
        """Generate fake product data."""
        categories = ["analytics", "intelligence", "optimization", "media", "automation"]
        statuses = ["active", "beta", "deprecated", "coming_soon"]
        tiers = ["standard", "professional", "premium", "enterprise"]
        
        return {
            "id": f"fake_prod_{self.faker.uuid4()}",
            "name": f"{self.faker.catch_phrase()} {random.choice(['Platform', 'Suite', 'Tool', 'Solution'])}",
            "description": self.faker.text(max_nb_chars=200),
            "category": random.choice(categories),
            "features": [self.faker.sentence(nb_words=3) for _ in range(random.randint(3, 7))],
            "pricing": {
                "tier": random.choice(tiers),
                "price_range": f"${random.randint(500, 5000)}-${random.randint(5000, 20000)}/month"
            },
            "target_audience": self.faker.sentence(nb_words=5),
            "status": random.choice(statuses),
            "created_at": self.faker.date_time_this_year().isoformat(),
            "updated_at": self.faker.date_time_this_month().isoformat()
        }
    
    def create_test_dataset(self, data_type: str, count: int, filename: str = None):
        """Create a test dataset with specified number of records."""
        dataset = []
        
        for i in range(count):
            if data_type == "users":
                dataset.append(self.generate_fake_user())
            elif data_type == "contacts":
                dataset.append(self.generate_fake_contact_data())
            elif data_type == "products":
                dataset.append(self.generate_fake_product())
            else:
                self.logger.error(f"Unknown data type: {data_type}")
                return
        
        if filename:
            self.save_json_data({f"generated_{data_type}": dataset}, filename)
        
        return dataset
    
    def get_boundary_test_data(self, field_type: str) -> Dict[str, List[Any]]:
        """Get boundary test data for different field types."""
        boundary_data = {
            "string": {
                "valid": ["a", "test", "A" * 50, "Valid String"],
                "invalid": ["", "A" * 1000, None],
                "edge": ["A", "A" * 255]
            },
            "email": {
                "valid": ["test@example.com", "user.name@domain.co.uk", "test+tag@example.org"],
                "invalid": ["invalid-email", "@example.com", "test@", "test.example.com"],
                "edge": ["a@b.co", "test" + "x" * 60 + "@example.com"]
            },
            "phone": {
                "valid": ["+1-555-123-4567", "555-123-4567", "+44-20-1234-5678"],
                "invalid": ["123", "abc-def-ghij", "1234567890123456789012345"],
                "edge": ["1234567890", "+1-555-123-4567-ext-12345"]
            },
            "integer": {
                "valid": [0, 1, 100, 999999],
                "invalid": [-1, "invalid", None, 1.5],
                "edge": [0, 2147483647, -2147483648]
            },
            "password": {
                "valid": ["Password123!", "SecureP@ss1", "MyStr0ng!Pass"],
                "invalid": ["123", "password", "PASSWORD", "Pass123"],
                "edge": ["P@ss1", "A" * 128 + "1!"]
            }
        }
        
        return boundary_data.get(field_type, {})
    
    def get_security_test_data(self) -> Dict[str, List[str]]:
        """Get security test payloads."""
        return {
            "sql_injection": [
                "'; DROP TABLE users; --",
                "1' OR '1'='1",
                "admin'--",
                "' UNION SELECT * FROM users --",
                "1; DELETE FROM users WHERE 1=1 --"
            ],
            "xss": [
                "<script>alert('xss')</script>",
                "javascript:alert('xss')",
                "<img src=x onerror=alert('xss')>",
                "';alert('xss');//",
                "<svg onload=alert('xss')>"
            ],
            "command_injection": [
                "; ls -la",
                "| cat /etc/passwd",
                "&& whoami",
                "`id`",
                "$(whoami)"
            ],
            "path_traversal": [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "....//....//....//etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ],
            "ldap_injection": [
                "*)(&",
                "*)(uid=*",
                "*)(|(password=*))",
                "admin)(&(password=*)"
            ],
            "xml_injection": [
                "<?xml version=\"1.0\"?><!DOCTYPE test [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><test>&xxe;</test>",
                "<![CDATA[<script>alert('xss')</script>]]>"
            ]
        }
    
    def get_performance_test_data(self) -> Dict[str, Any]:
        """Get performance test configuration data."""
        return {
            "load_levels": {
                "light": {"users": 5, "duration": 60, "ramp_up": 10},
                "medium": {"users": 20, "duration": 300, "ramp_up": 30},
                "heavy": {"users": 50, "duration": 600, "ramp_up": 60},
                "stress": {"users": 100, "duration": 900, "ramp_up": 120}
            },
            "response_time_thresholds": {
                "excellent": 1.0,
                "good": 3.0,
                "acceptable": 5.0,
                "poor": 10.0
            },
            "success_rate_thresholds": {
                "excellent": 0.99,
                "good": 0.95,
                "acceptable": 0.90,
                "poor": 0.80
            }
        }
    
    def cleanup_test_data(self, pattern: str = "temp_*"):
        """Clean up temporary test data files."""
        import glob
        
        pattern_path = os.path.join(self.test_data_path, pattern)
        temp_files = glob.glob(pattern_path)
        
        cleaned_count = 0
        for file_path in temp_files:
            try:
                os.remove(file_path)
                cleaned_count += 1
            except Exception as e:
                self.logger.error(f"Error removing temp file {file_path}: {e}")
        
        self.logger.info(f"Cleaned up {cleaned_count} temporary test data files")
        return cleaned_count
    
    def validate_test_data(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate test data against a schema."""
        validation_errors = {
            "missing_fields": [],
            "invalid_types": [],
            "invalid_values": []
        }
        
        # Check required fields
        required_fields = schema.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                validation_errors["missing_fields"].append(field)
        
        # Check field types
        field_types = schema.get("field_types", {})
        for field, expected_type in field_types.items():
            if field in data:
                actual_type = type(data[field]).__name__
                if actual_type != expected_type:
                    validation_errors["invalid_types"].append(f"{field}: expected {expected_type}, got {actual_type}")
        
        # Check field values
        field_constraints = schema.get("field_constraints", {})
        for field, constraints in field_constraints.items():
            if field in data:
                value = data[field]
                
                # Check min/max length for strings
                if isinstance(value, str):
                    if "min_length" in constraints and len(value) < constraints["min_length"]:
                        validation_errors["invalid_values"].append(f"{field}: too short (min {constraints['min_length']})")
                    if "max_length" in constraints and len(value) > constraints["max_length"]:
                        validation_errors["invalid_values"].append(f"{field}: too long (max {constraints['max_length']})")
                
                # Check allowed values
                if "allowed_values" in constraints and value not in constraints["allowed_values"]:
                    validation_errors["invalid_values"].append(f"{field}: invalid value '{value}'")
        
        return validation_errors
    
    def export_test_results(self, results: Dict[str, Any], format: str = "json", filename: str = None):
        """Export test results to file."""
        if not filename:
            timestamp = self.faker.date_time().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.{format}"
        
        filepath = os.path.join(self.test_data_path, filename)
        
        try:
            if format.lower() == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            elif format.lower() == "csv":
                # Flatten results for CSV export
                flattened_results = []
                if isinstance(results, dict):
                    if "test_cases" in results:
                        flattened_results = results["test_cases"]
                    else:
                        flattened_results = [results]
                elif isinstance(results, list):
                    flattened_results = results
                
                if flattened_results:
                    with open(filepath, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=flattened_results[0].keys())
                        writer.writeheader()
                        writer.writerows(flattened_results)
            
            self.logger.info(f"Test results exported to {filename}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting test results: {e}")
            return None