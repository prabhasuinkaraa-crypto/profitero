"""Report generation utilities for test framework."""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Template, Environment, FileSystemLoader
import base64
from utils.config_reader import config
import logging


class ReportGenerator:
    """Generate comprehensive test reports."""
    
    def __init__(self):
        """Initialize report generator."""
        self.reports_path = config.get_reports_path()
        self.screenshots_path = config.get_screenshots_path()
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        os.makedirs(self.reports_path, exist_ok=True)
        os.makedirs(self.screenshots_path, exist_ok=True)
        
        # Set up Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(os.path.dirname(__file__)),
            autoescape=True
        )
    
    def generate_html_report(self, test_results: Dict[str, Any], 
                           template_name: str = "default_report_template.html") -> str:
        """Generate HTML test report."""
        try:
            # Create template if it doesn't exist
            template_path = os.path.join(os.path.dirname(__file__), template_name)
            if not os.path.exists(template_path):
                self._create_default_template(template_path)
            
            # Load template
            template = self.jinja_env.get_template(template_name)
            
            # Prepare report data
            report_data = self._prepare_report_data(test_results)
            
            # Render HTML
            html_content = template.render(**report_data)
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"test_report_{timestamp}.html"
            report_path = os.path.join(self.reports_path, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating HTML report: {e}")
            return ""
    
    def _create_default_template(self, template_path: str):
        """Create default HTML report template."""
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profitero Test Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background-color: #f8f9fa;
        }
        .summary-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .summary-card .value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
        }
        .passed { color: #28a745; }
        .failed { color: #dc3545; }
        .skipped { color: #ffc107; }
        .total { color: #007bff; }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .test-case {
            background: #f8f9fa;
            border-left: 4px solid #dee2e6;
            margin: 15px 0;
            padding: 15px;
            border-radius: 0 5px 5px 0;
        }
        .test-case.passed {
            border-left-color: #28a745;
            background-color: #f8fff9;
        }
        .test-case.failed {
            border-left-color: #dc3545;
            background-color: #fff8f8;
        }
        .test-case.skipped {
            border-left-color: #ffc107;
            background-color: #fffdf7;
        }
        .test-case h4 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .test-case .status {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .status.passed {
            background-color: #28a745;
            color: white;
        }
        .status.failed {
            background-color: #dc3545;
            color: white;
        }
        .status.skipped {
            background-color: #ffc107;
            color: #333;
        }
        .error-details {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 0.9em;
        }
        .screenshot {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 10px;
        }
        .performance-chart {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .footer {
            background-color: #343a40;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            font-size: 0.8em;
            border-radius: 12px;
            margin-right: 5px;
        }
        .badge-info { background-color: #17a2b8; color: white; }
        .badge-warning { background-color: #ffc107; color: #333; }
        .badge-success { background-color: #28a745; color: white; }
        .badge-danger { background-color: #dc3545; color: white; }
        
        @media (max-width: 768px) {
            .summary {
                grid-template-columns: 1fr;
            }
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Profitero Test Report</h1>
            <p>Generated on {{ report_date }} | Duration: {{ test_duration }}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <p class="value total">{{ summary.total_tests }}</p>
            </div>
            <div class="summary-card">
                <h3>Passed</h3>
                <p class="value passed">{{ summary.passed }}</p>
            </div>
            <div class="summary-card">
                <h3>Failed</h3>
                <p class="value failed">{{ summary.failed }}</p>
            </div>
            <div class="summary-card">
                <h3>Skipped</h3>
                <p class="value skipped">{{ summary.skipped }}</p>
            </div>
            <div class="summary-card">
                <h3>Success Rate</h3>
                <p class="value {{ 'passed' if summary.success_rate >= 0.9 else 'failed' if summary.success_rate < 0.7 else 'skipped' }}">
                    {{ "%.1f"|format(summary.success_rate * 100) }}%
                </p>
            </div>
        </div>
        
        <div class="content">
            {% if test_scenarios %}
            <div class="section">
                <h2>Test Scenarios</h2>
                {% for scenario in test_scenarios %}
                <div class="test-case {{ scenario.status.lower() }}">
                    <h4>
                        {{ scenario.name }}
                        <span class="status {{ scenario.status.lower() }}">{{ scenario.status }}</span>
                        {% if scenario.duration %}
                        <span class="badge badge-info">{{ "%.2f"|format(scenario.duration) }}s</span>
                        {% endif %}
                    </h4>
                    {% if scenario.tags %}
                    <p>
                        {% for tag in scenario.tags %}
                        <span class="badge badge-info">{{ tag }}</span>
                        {% endfor %}
                    </p>
                    {% endif %}
                    {% if scenario.error_message %}
                    <div class="error-details">
                        <strong>Error:</strong> {{ scenario.error_message }}
                    </div>
                    {% endif %}
                    {% if scenario.screenshot %}
                    <div>
                        <strong>Screenshot:</strong><br>
                        <img src="data:image/png;base64,{{ scenario.screenshot_data }}" class="screenshot" alt="Test Screenshot">
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            {% if performance_data %}
            <div class="section">
                <h2>Performance Metrics</h2>
                <div class="performance-chart">
                    <h3>Response Times</h3>
                    <p><strong>Average:</strong> {{ "%.2f"|format(performance_data.avg_response_time) }}s</p>
                    <p><strong>Min:</strong> {{ "%.2f"|format(performance_data.min_response_time) }}s</p>
                    <p><strong>Max:</strong> {{ "%.2f"|format(performance_data.max_response_time) }}s</p>
                </div>
            </div>
            {% endif %}
            
            {% if environment_info %}
            <div class="section">
                <h2>Environment Information</h2>
                <div class="test-case">
                    <p><strong>Browser:</strong> {{ environment_info.browser }}</p>
                    <p><strong>OS:</strong> {{ environment_info.os }}</p>
                    <p><strong>Base URL:</strong> {{ environment_info.base_url }}</p>
                    <p><strong>Test Environment:</strong> {{ environment_info.environment }}</p>
                </div>
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>&copy; 2025 Profitero Test Automation Framework</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content.strip())
    
    def _prepare_report_data(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for report generation."""
        # Calculate summary statistics
        total_tests = test_results.get('total_tests', 0)
        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)
        skipped = test_results.get('skipped', 0)
        
        success_rate = passed / total_tests if total_tests > 0 else 0
        
        # Process test scenarios
        scenarios = test_results.get('scenarios', [])
        processed_scenarios = []
        
        for scenario in scenarios:
            processed_scenario = {
                'name': scenario.get('name', 'Unknown'),
                'status': scenario.get('status', 'unknown'),
                'duration': scenario.get('duration', 0),
                'tags': scenario.get('tags', []),
                'error_message': scenario.get('error_message', ''),
                'screenshot': scenario.get('screenshot', ''),
                'screenshot_data': ''
            }
            
            # Load screenshot data if available
            if processed_scenario['screenshot']:
                screenshot_path = os.path.join(self.screenshots_path, f"{processed_scenario['screenshot']}.png")
                if os.path.exists(screenshot_path):
                    try:
                        with open(screenshot_path, 'rb') as f:
                            screenshot_data = base64.b64encode(f.read()).decode('utf-8')
                            processed_scenario['screenshot_data'] = screenshot_data
                    except Exception as e:
                        self.logger.warning(f"Could not load screenshot {screenshot_path}: {e}")
            
            processed_scenarios.append(processed_scenario)
        
        # Prepare report data
        report_data = {
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'test_duration': self._format_duration(test_results.get('test_duration', 0)),
            'summary': {
                'total_tests': total_tests,
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'success_rate': success_rate
            },
            'test_scenarios': processed_scenarios,
            'performance_data': self._process_performance_data(test_results.get('performance_data', {})),
            'environment_info': {
                'browser': config.get_browser(),
                'os': test_results.get('os', 'Unknown'),
                'base_url': config.get_base_url(),
                'environment': config.get('environment', 'test')
            }
        }
        
        return report_data
    
    def _process_performance_data(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process performance data for reporting."""
        if not performance_data:
            return {}
        
        response_times = performance_data.get('response_times', [])
        
        if response_times:
            return {
                'avg_response_time': sum(response_times) / len(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'total_requests': len(response_times)
            }
        
        return {}
    
    def _format_duration(self, duration_seconds: float) -> str:
        """Format duration in human-readable format."""
        if duration_seconds < 60:
            return f"{duration_seconds:.1f} seconds"
        elif duration_seconds < 3600:
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def generate_json_report(self, test_results: Dict[str, Any]) -> str:
        """Generate JSON test report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"test_report_{timestamp}.json"
            report_path = os.path.join(self.reports_path, report_filename)
            
            # Add metadata
            report_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'framework_version': '1.0.0',
                    'report_format': 'json'
                },
                'test_results': test_results
            }
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"JSON report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating JSON report: {e}")
            return ""
    
    def generate_csv_report(self, test_results: Dict[str, Any]) -> str:
        """Generate CSV test report."""
        try:
            import csv
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"test_report_{timestamp}.csv"
            report_path = os.path.join(self.reports_path, report_filename)
            
            scenarios = test_results.get('scenarios', [])
            
            if scenarios:
                with open(report_path, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['name', 'status', 'duration', 'tags', 'error_message']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for scenario in scenarios:
                        row = {
                            'name': scenario.get('name', ''),
                            'status': scenario.get('status', ''),
                            'duration': scenario.get('duration', 0),
                            'tags': ', '.join(scenario.get('tags', [])),
                            'error_message': scenario.get('error_message', '')
                        }
                        writer.writerow(row)
            
            self.logger.info(f"CSV report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating CSV report: {e}")
            return ""
    
    def generate_junit_xml_report(self, test_results: Dict[str, Any]) -> str:
        """Generate JUnit XML test report."""
        try:
            from xml.etree.ElementTree import Element, SubElement, tostring
            from xml.dom import minidom
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"junit_report_{timestamp}.xml"
            report_path = os.path.join(self.reports_path, report_filename)
            
            # Create root element
            testsuites = Element('testsuites')
            testsuites.set('name', 'Profitero Test Suite')
            testsuites.set('tests', str(test_results.get('total_tests', 0)))
            testsuites.set('failures', str(test_results.get('failed', 0)))
            testsuites.set('skipped', str(test_results.get('skipped', 0)))
            testsuites.set('time', str(test_results.get('test_duration', 0)))
            
            # Create testsuite element
            testsuite = SubElement(testsuites, 'testsuite')
            testsuite.set('name', 'Profitero Tests')
            testsuite.set('tests', str(test_results.get('total_tests', 0)))
            testsuite.set('failures', str(test_results.get('failed', 0)))
            testsuite.set('skipped', str(test_results.get('skipped', 0)))
            testsuite.set('time', str(test_results.get('test_duration', 0)))
            
            # Add test cases
            scenarios = test_results.get('scenarios', [])
            for scenario in scenarios:
                testcase = SubElement(testsuite, 'testcase')
                testcase.set('name', scenario.get('name', 'Unknown'))
                testcase.set('classname', 'ProfiteroTests')
                testcase.set('time', str(scenario.get('duration', 0)))
                
                status = scenario.get('status', 'unknown').lower()
                if status == 'failed':
                    failure = SubElement(testcase, 'failure')
                    failure.set('message', scenario.get('error_message', 'Test failed'))
                    failure.text = scenario.get('error_message', 'Test failed')
                elif status == 'skipped':
                    skipped = SubElement(testcase, 'skipped')
                    skipped.set('message', 'Test skipped')
            
            # Write XML file
            xml_str = minidom.parseString(tostring(testsuites)).toprettyxml(indent="  ")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            self.logger.info(f"JUnit XML report generated: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating JUnit XML report: {e}")
            return ""
    
    def generate_all_reports(self, test_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate all report formats."""
        reports = {}
        
        try:
            reports['html'] = self.generate_html_report(test_results)
            reports['json'] = self.generate_json_report(test_results)
            reports['csv'] = self.generate_csv_report(test_results)
            reports['junit_xml'] = self.generate_junit_xml_report(test_results)
            
            self.logger.info("All report formats generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {e}")
        
        return reports
    
    def create_dashboard_data(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create data for test dashboard."""
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': test_results.get('total_tests', 0),
                'passed': test_results.get('passed', 0),
                'failed': test_results.get('failed', 0),
                'skipped': test_results.get('skipped', 0),
                'success_rate': test_results.get('passed', 0) / max(test_results.get('total_tests', 1), 1)
            },
            'trends': {
                'test_count_trend': [test_results.get('total_tests', 0)],
                'success_rate_trend': [test_results.get('passed', 0) / max(test_results.get('total_tests', 1), 1)]
            },
            'performance': self._process_performance_data(test_results.get('performance_data', {})),
            'test_categories': self._categorize_tests(test_results.get('scenarios', []))
        }
        
        return dashboard_data
    
    def _categorize_tests(self, scenarios: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize tests by tags."""
        categories = {}
        
        for scenario in scenarios:
            tags = scenario.get('tags', [])
            for tag in tags:
                if tag in categories:
                    categories[tag] += 1
                else:
                    categories[tag] = 1
        
        return categories
    
    def cleanup_old_reports(self, days_to_keep: int = 30):
        """Clean up old report files."""
        import glob
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
        
        report_patterns = [
            "test_report_*.html",
            "test_report_*.json",
            "test_report_*.csv",
            "junit_report_*.xml"
        ]
        
        cleaned_count = 0
        
        for pattern in report_patterns:
            pattern_path = os.path.join(self.reports_path, pattern)
            old_files = glob.glob(pattern_path)
            
            for file_path in old_files:
                try:
                    file_time = os.path.getctime(file_path)
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        cleaned_count += 1
                except Exception as e:
                    self.logger.error(f"Error removing old report {file_path}: {e}")
        
        self.logger.info(f"Cleaned up {cleaned_count} old report files")
        return cleaned_count