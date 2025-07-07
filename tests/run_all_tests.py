#!/usr/bin/env python3
"""
Comprehensive Test Runner for HR Agent Bot
Runs all test suites and provides detailed reporting
"""

import unittest
import sys
import os
import time
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.test_unit import *
from tests.test_integration import *
from tests.test_e2e import *


def run_test_suite(test_class, suite_name):
    """Run a specific test suite and return results."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {suite_name}")
    print(f"{'='*60}")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    
    # Run tests
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    end_time = time.time()
    
    # Calculate statistics
    total_tests = result.testsRun
    failed_tests = len(result.failures)
    errored_tests = len(result.errors)
    skipped_tests = total_tests - failed_tests - errored_tests
    
    # Print summary
    print(f"\n📊 {suite_name} Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {skipped_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Errors: {errored_tests}")
    print(f"  Duration: {end_time - start_time:.2f} seconds")
    
    return {
        "suite_name": suite_name,
        "total_tests": total_tests,
        "passed": skipped_tests,
        "failed": failed_tests,
        "errors": errored_tests,
        "duration": end_time - start_time,
        "failures": result.failures,
        "errors": result.errors
    }


def run_all_tests():
    """Run all test suites and generate comprehensive report."""
    print("🤖 HR Agent Bot - Comprehensive Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define test suites
    test_suites = [
        (TestTools, "Unit Tests - Tools"),
        (TestEscalation, "Unit Tests - Escalation"),
        (TestFeedbackCollector, "Unit Tests - Feedback Collection"),
        (TestDocumentParser, "Unit Tests - Document Parser"),
        (TestAgentIntegration, "Integration Tests - Agent"),
        (TestEscalationIntegration, "Integration Tests - Escalation"),
        (TestFeedbackIntegration, "Integration Tests - Feedback"),
        (TestKnowledgeBaseIntegration, "Integration Tests - Knowledge Base"),
        (TestToolIntegration, "Integration Tests - Tools"),
        (TestCompleteUserWorkflows, "End-to-End Tests - User Workflows"),
        (TestEdgeCases, "End-to-End Tests - Edge Cases"),
        (TestPerformanceScenarios, "End-to-End Tests - Performance")
    ]
    
    # Run all test suites
    results = []
    total_start_time = time.time()
    
    for test_class, suite_name in test_suites:
        try:
            result = run_test_suite(test_class, suite_name)
            results.append(result)
        except Exception as e:
            print(f"❌ Failed to run {suite_name}: {e}")
            results.append({
                "suite_name": suite_name,
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "duration": 0,
                "failures": [],
                "errors": [(suite_name, str(e))]
            })
    
    total_end_time = time.time()
    
    # Generate comprehensive report
    print(f"\n{'='*60}")
    print("📋 COMPREHENSIVE TEST REPORT")
    print(f"{'='*60}")
    
    # Overall statistics
    total_tests = sum(r["total_tests"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    total_duration = sum(r["duration"] for r in results)
    
    print(f"Overall Statistics:")
    print(f"  Total Test Suites: {len(test_suites)}")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    print(f"  Errors: {total_errors}")
    print(f"  Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "  Success Rate: 0%")
    print(f"  Total Duration: {total_duration:.2f} seconds")
    
    # Detailed results by suite
    print(f"\nDetailed Results by Suite:")
    print(f"{'Suite Name':<40} {'Tests':<8} {'Passed':<8} {'Failed':<8} {'Errors':<8} {'Duration':<10}")
    print("-" * 90)
    
    for result in results:
        print(f"{result['suite_name']:<40} {result['total_tests']:<8} {result['passed']:<8} {result['failed']:<8} {result['errors']:<8} {result['duration']:<10.2f}s")
    
    # Summary of failures and errors
    all_failures = []
    all_errors = []
    
    for result in results:
        all_failures.extend(result["failures"])
        all_errors.extend(result["errors"])
    
    if all_failures:
        print(f"\n❌ Failures ({len(all_failures)}):")
        for test, traceback in all_failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if all_errors:
        print(f"\n💥 Errors ({len(all_errors)}):")
        for test, traceback in all_errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    # Generate test report file
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "overall_stats": {
            "total_suites": len(test_suites),
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "errors": total_errors,
            "success_rate": (total_passed/total_tests*100) if total_tests > 0 else 0,
            "total_duration": total_duration
        },
        "suite_results": results,
        "failures": all_failures,
        "errors": all_errors
    }
    
    # Save report to file
    report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed test report saved to: {report_filename}")
    
    # Final verdict
    if total_failed == 0 and total_errors == 0:
        print(f"\n✅ ALL TESTS PASSED! 🎉")
        return 0
    else:
        print(f"\n❌ {total_failed + total_errors} TESTS FAILED")
        return 1


def run_specific_test_category(category):
    """Run tests for a specific category."""
    categories = {
        "unit": [
            (TestTools, "Unit Tests - Tools"),
            (TestEscalation, "Unit Tests - Escalation"),
            (TestFeedbackCollector, "Unit Tests - Feedback Collection"),
            (TestDocumentParser, "Unit Tests - Document Parser")
        ],
        "integration": [
            (TestAgentIntegration, "Integration Tests - Agent"),
            (TestEscalationIntegration, "Integration Tests - Escalation"),
            (TestFeedbackIntegration, "Integration Tests - Feedback"),
            (TestKnowledgeBaseIntegration, "Integration Tests - Knowledge Base"),
            (TestToolIntegration, "Integration Tests - Tools")
        ],
        "e2e": [
            (TestCompleteUserWorkflows, "End-to-End Tests - User Workflows"),
            (TestEdgeCases, "End-to-End Tests - Edge Cases"),
            (TestPerformanceScenarios, "End-to-End Tests - Performance")
        ]
    }
    
    if category not in categories:
        print(f"❌ Unknown category: {category}")
        print(f"Available categories: {', '.join(categories.keys())}")
        return 1
    
    print(f"🧪 Running {category.upper()} tests only...")
    
    results = []
    for test_class, suite_name in categories[category]:
        result = run_test_suite(test_class, suite_name)
        results.append(result)
    
    # Print summary for category
    total_tests = sum(r["total_tests"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    
    print(f"\n📊 {category.upper()} Tests Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    print(f"  Errors: {total_errors}")
    print(f"  Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "  Success Rate: 0%")
    
    return 0 if total_failed == 0 and total_errors == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        category = sys.argv[1].lower()
        exit_code = run_specific_test_category(category)
    else:
        exit_code = run_all_tests()
    
    sys.exit(exit_code) 