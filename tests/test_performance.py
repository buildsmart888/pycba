"""
Performance and Integration Tests for Continuous Beam Analysis
"""
import unittest
import time
import numpy as np
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pycba.analysis import BeamAnalysis


class TestPerformance(unittest.TestCase):
    """Performance tests for beam analysis"""
    
    def test_analysis_performance_small_beam(self):
        """Test analysis performance for small beam (2 spans)"""
        span_lengths = [5.0, 5.0]
        E = 200e6
        I = 0.0001
        R = [-1, -1, -1, 0, -1, -1]
        LM = [
            [1, 1, -1.44, 0.0, 0.0],
            [2, 1, -1.44, 0.0, 0.0]
        ]
        
        start_time = time.time()
        analysis = BeamAnalysis(span_lengths, E * I, R, LM)
        analysis.analyze()
        end_time = time.time()
        
        analysis_time = end_time - start_time
        # Should complete within 1 second for small beam
        self.assertLess(analysis_time, 1.0)
        print(f"Small beam analysis time: {analysis_time:.3f} seconds")
    
    def test_analysis_performance_large_beam(self):
        """Test analysis performance for large beam (10 spans)"""
        span_lengths = [5.0] * 10  # 10 spans of 5m each
        E = 200e6
        I = 0.0001
        
        # Set up support conditions for 10 spans (11 supports)
        R = [-1, -1]  # First support (fixed)
        for i in range(1, 10):  # Middle supports (pinned)
            R.extend([-1, 0])
        R.extend([-1, -1])  # Last support (fixed)
        
        # Set up loads for all spans
        LM = []
        for i in range(10):
            LM.append([i+1, 1, -1.44, 0.0, 0.0])
        
        start_time = time.time()
        analysis = BeamAnalysis(span_lengths, E * I, R, LM)
        analysis.analyze()
        end_time = time.time()
        
        analysis_time = end_time - start_time
        # Should complete within 5 seconds for large beam
        self.assertLess(analysis_time, 5.0)
        print(f"Large beam analysis time: {analysis_time:.3f} seconds")
    
    def test_multiple_analysis_runs(self):
        """Test performance of multiple consecutive analyses"""
        span_lengths = [5.0, 5.0, 5.0]
        E = 200e6
        I = 0.0001
        R = [-1, -1, -1, 0, -1, 0, -1, -1]
        
        num_runs = 10
        total_start_time = time.time()
        
        for i in range(num_runs):
            load_variation = 1.0 + (i * 0.1)  # Vary load from 1.0 to 1.9
            LM = [
                [1, 1, -load_variation, 0.0, 0.0],
                [2, 1, -load_variation, 0.0, 0.0],
                [3, 1, -load_variation, 0.0, 0.0]
            ]
            
            analysis = BeamAnalysis(span_lengths, E * I, R, LM)
            analysis.analyze()
        
        total_end_time = time.time()
        total_time = total_end_time - total_start_time
        avg_time = total_time / num_runs
        
        print(f"Average analysis time over {num_runs} runs: {avg_time:.3f} seconds")
        # Average should be reasonable
        self.assertLess(avg_time, 1.0)


class TestComplexScenarios(unittest.TestCase):
    """Test complex real-world scenarios"""
    
    def test_bridge_like_structure(self):
        """Test analysis of a bridge-like continuous beam"""
        # 5-span bridge: 25m + 30m + 35m + 30m + 25m
        span_lengths = [25.0, 30.0, 35.0, 30.0, 25.0]
        E = 200e9  # 200 GPa (concrete)
        I = 0.1    # 0.1 m⁴ (large beam)
        
        # Support conditions: Fixed at ends, pinned at intermediate
        R = [-1, -1]  # End 1 (fixed)
        for i in range(1, 5):  # Intermediate supports (pinned)
            R.extend([-1, 0])
        R.extend([-1, -1])  # End 2 (fixed)
        
        # Loading: Dead load + Live load + Vehicle load
        dead_load = 15.0  # kN/m
        live_load = 12.0  # kN/m
        
        LM = []
        for i in range(5):
            # Distributed loads
            LM.append([i+1, 1, -(dead_load + live_load), 0.0, 0.0])
            
            # Add concentrated load at mid-span (vehicle)
            if i == 2:  # Middle span gets extra vehicle load
                LM.append([i+1, 2, -200.0, 0.5, 0.0])  # 200 kN at mid-span
        
        # Perform analysis
        analysis = BeamAnalysis(span_lengths, E * I, R, LM)
        analysis.analyze()
        
        # Verify results
        results = analysis.beam_results.results
        self.assertIsNotNone(results)
        self.assertGreater(len(results.x), 0)
        
        # Check that maximum moment is reasonable for this size structure
        moments = np.array(results.M)
        max_moment = np.max(np.abs(moments))
        self.assertGreater(max_moment, 1000)  # Should be significant
        self.assertLess(max_moment, 50000)    # But not unreasonable
        
        print(f"Bridge analysis - Max moment: {max_moment:.0f} kN-m")
    
    def test_asymmetric_loading(self):
        """Test beam with asymmetric loading pattern"""
        span_lengths = [6.0, 6.0, 6.0, 6.0]
        E = 200e6
        I = 0.0001
        
        # Support conditions
        R = [-1, -1, -1, 0, -1, 0, -1, 0, -1, -1]
        
        # Asymmetric loading: decreasing load from left to right
        loads = [5.0, 3.0, 2.0, 1.0]  # kN/m
        LM = []
        for i, load in enumerate(loads):
            LM.append([i+1, 1, -load, 0.0, 0.0])
        
        analysis = BeamAnalysis(span_lengths, E * I, R, LM)
        analysis.analyze()
        
        results = analysis.beam_results.results
        
        # Check that analysis completed successfully
        self.assertIsNotNone(results)
        
        # Verify asymmetric response
        moments = np.array(results.M)
        
        # Find moment at quarter points of each span
        total_length = sum(span_lengths)
        x_points = np.array(results.x)
        
        quarter_moments = []
        for i in range(4):
            span_start = sum(span_lengths[:i])
            quarter_point = span_start + span_lengths[i] * 0.25
            idx = np.argmin(np.abs(x_points - quarter_point))
            quarter_moments.append(abs(moments[idx]))
        
        # First span should have larger moments than last span
        self.assertGreater(quarter_moments[0], quarter_moments[3])
        
        print(f"Asymmetric loading - Quarter span moments: {quarter_moments}")
    
    def test_temperature_effects(self):
        """Test beam with temperature loading (simplified)"""
        span_lengths = [8.0, 8.0]
        E = 200e6
        I = 0.0001
        
        R = [-1, -1, -1, 0, -1, -1]
        
        # Simulate temperature effect as imposed moments
        temp_moment = 50.0  # kN-m (simplified temperature effect)
        
        LM = [
            [1, 1, -2.0, 0.0, 0.0],  # Dead load
            [2, 1, -2.0, 0.0, 0.0],  # Dead load
            [1, 4, temp_moment, 0.0, 0.0],    # Temperature moment at start
            [2, 4, -temp_moment, 1.0, 0.0],   # Reverse moment at end
        ]
        
        analysis = BeamAnalysis(span_lengths, E * I, R, LM)
        analysis.analyze()
        
        results = analysis.beam_results.results
        self.assertIsNotNone(results)
        
        # Temperature effects should create additional moments
        moments = np.array(results.M)
        max_moment = np.max(np.abs(moments))
        
        # Should be more than just gravity loads would produce
        self.assertGreater(max_moment, 10.0)
        
        print(f"Temperature effects - Max moment: {max_moment:.1f} kN-m")


class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling"""
    
    def test_invalid_span_lengths(self):
        """Test handling of invalid span lengths"""
        # Test negative span length
        with self.assertRaises(Exception):
            BeamAnalysis([-5.0, 5.0], 1000, [-1, -1, -1, 0], [])
    
    def test_mismatched_supports(self):
        """Test handling of mismatched support conditions"""
        span_lengths = [5.0, 5.0]
        E_I = 1000
        
        # Wrong number of support conditions (should be 6 for 2 spans)
        R_wrong = [-1, -1, -1, 0]  # Only 4 instead of 6
        LM = [[1, 1, -1.0, 0.0, 0.0]]
        
        # This should raise an exception or handle gracefully
        try:
            analysis = BeamAnalysis(span_lengths, E_I, R_wrong, LM)
            analysis.analyze()
        except Exception as e:
            # Expected to fail with wrong support configuration
            print(f"Expected error with wrong supports: {e}")
    
    def test_extreme_loads(self):
        """Test handling of extreme load values"""
        span_lengths = [5.0]
        E_I = [1000]  # Must be list for BeamAnalysis
        R = [[-1, -1, -1, -1]]  # Support matrix format
        
        # Extremely large load
        LM = [[1, 1, -1e6, 0.0, 0.0]]  # 1 million kN/m
        
        try:
            analysis = BeamAnalysis(span_lengths, E_I, R, LM)
            analysis.analyze()
            
            results = analysis.beam_results.results
            
            # Should complete but results will be large
            moments = np.array(results.M)
            self.assertTrue(np.all(np.isfinite(moments)))  # Check for NaN/Inf
            
        except Exception as e:
            # Expected for extreme values that may cause numerical issues
            self.assertIsInstance(e, (ValueError, TypeError, np.linalg.LinAlgError))
            print(f"Expected error with extreme loads: {e}")


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
