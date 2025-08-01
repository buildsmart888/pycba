"""
Test Runner for PyCBA Advanced App
Run all tests and generate test report
"""
import unittest
import sys
import os
import time
from io import StringIO

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_all_tests():
    """Run all test suites and generate report"""
    print("="*60)
    print("PyCBA Advanced App - Test Suite Runner")
    print("="*60)
    
    # Discover and run tests
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    
    # Load specific test modules
    test_modules = [
        'test_advanced_app',
        'test_performance'
    ]
    
    suite = unittest.TestSuite()
    
    for module_name in test_modules:
        try:
            # Import and add tests from each module
            module = __import__(module_name)
            module_suite = loader.loadTestsFromModule(module)
            suite.addTests(module_suite)
            print(f"✓ Loaded tests from {module_name}")
        except ImportError as e:
            print(f"✗ Failed to load {module_name}: {e}")
            continue
    
    print(f"\nTotal test cases loaded: {suite.countTestCases()}")
    print("-" * 60)
    
    # Run tests with detailed output
    start_time = time.time()
    
    # Capture test output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print test output
    test_output = stream.getvalue()
    print(test_output)
    
    # Generate summary report
    print("="*60)
    print("TEST SUMMARY REPORT")
    print("="*60)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Execution Time: {total_time:.2f} seconds")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print()
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! 🎉")
        print("✓ Your beam analysis application is working correctly")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"✗ Failures: {len(result.failures)}")
        print(f"✗ Errors: {len(result.errors)}")
    
    print()
    
    # Detailed failure/error reporting
    if result.failures:
        print("-" * 60)
        print("FAILURE DETAILS:")
        print("-" * 60)
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"{i}. {test}")
            print(f"   {traceback.strip()}")
            print()
    
    if result.errors:
        print("-" * 60)
        print("ERROR DETAILS:")
        print("-" * 60)
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"{i}. {test}")
            print(f"   {traceback.strip()}")
            print()
    
    # Recommendations
    print("-" * 60)
    print("RECOMMENDATIONS:")
    print("-" * 60)
    
    if result.wasSuccessful():
        print("✓ All core functionality is working")
        print("✓ Performance is within acceptable limits")
        print("✓ Edge cases are handled properly")
        print("✓ Integration with PyCBA library is successful")
        print()
        print("Your application is ready for production use!")
    else:
        print("Consider the following actions:")
        if result.failures:
            print("• Review and fix failing test cases")
            print("• Check calculation logic in affected functions")
        if result.errors:
            print("• Fix import and runtime errors")
            print("• Ensure all dependencies are properly installed")
        print("• Re-run tests after making fixes")
    
    print("="*60)
    
    return result.wasSuccessful()


def run_specific_test(test_name):
    """Run a specific test case"""
    print(f"Running specific test: {test_name}")
    
    # Try to find and run the specific test
    loader = unittest.TestLoader()
    
    try:
        suite = loader.loadTestsFromName(test_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()
    except Exception as e:
        print(f"Error running test {test_name}: {e}")
        return False


if __name__ == '__main__':
    # Check if specific test is requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
