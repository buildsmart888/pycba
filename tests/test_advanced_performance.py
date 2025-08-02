"""
Enhanced Performance Tests for Advanced App Functions
วันที่สร้าง: 2 สิงหาคม 2568
ทดสอบ: Performance, Memory usage, Large datasets, Concurrent operations
"""

import pytest
import time
import numpy as np
import psutil
import sys
import os
from unittest.mock import Mock
import threading

# Add the project root to Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Import functions to test
from advanced_app import (
    create_beam_diagram,
    create_shear_diagram,
    create_moment_diagram,
    create_deflection_diagram
)

class TestAdvancedAppPerformance:
    """Performance tests for advanced app functions"""
    
    def test_beam_diagram_performance_small(self):
        """Test beam diagram performance with small dataset"""
        span_lengths = [5.0, 6.0]
        reactions = [2500, 3000, 2500]
        
        start_time = time.time()
        
        for i in range(10):  # Run multiple times
            fig = create_beam_diagram(
                span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions
            )
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 10
        
        # Should complete within 0.1 seconds per diagram
        assert avg_time < 0.1, f"Beam diagram too slow: {avg_time:.3f}s"
        print(f"Average beam diagram time: {avg_time:.4f} seconds")
    
    def test_beam_diagram_performance_large(self):
        """Test beam diagram performance with large beam"""
        span_lengths = [5.0] * 20  # 20 spans
        reactions = [1000] * 21    # 21 supports
        
        start_time = time.time()
        
        fig = create_beam_diagram(
            span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within 2 seconds even for large beam
        assert execution_time < 2.0, f"Large beam diagram too slow: {execution_time:.3f}s"
        print(f"Large beam diagram time: {execution_time:.4f} seconds")
    
    def test_shear_diagram_performance_large_dataset(self):
        """Test shear diagram performance with large dataset"""
        n_points = 10000
        x_points = np.linspace(0, 100, n_points)
        shear = 1000 * np.sin(x_points * np.pi / 50) + np.random.normal(0, 100, n_points)
        
        start_time = time.time()
        
        fig = create_shear_diagram(x_points, shear)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should handle 10k points within 1 second
        assert execution_time < 1.0, f"Shear diagram too slow for large dataset: {execution_time:.3f}s"
        print(f"Large shear diagram time: {execution_time:.4f} seconds")
    
    def test_moment_diagram_performance_large_dataset(self):
        """Test moment diagram performance with large dataset"""
        n_points = 10000
        x_points = np.linspace(0, 50, n_points)
        moment = 5000 * x_points * (50 - x_points) / 625 + np.random.normal(0, 200, n_points)
        
        start_time = time.time()
        
        fig = create_moment_diagram(x_points, moment)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should handle 10k points within 1 second
        assert execution_time < 1.0, f"Moment diagram too slow for large dataset: {execution_time:.3f}s"
        print(f"Large moment diagram time: {execution_time:.4f} seconds")
    
    def test_deflection_diagram_performance_large_dataset(self):
        """Test deflection diagram performance with large dataset"""
        n_points = 10000
        x_points = np.linspace(0, 30, n_points)
        deflection = 10 * np.sin(x_points * np.pi / 30) + np.random.normal(0, 1, n_points)
        
        start_time = time.time()
        
        fig = create_deflection_diagram(x_points, deflection)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should handle 10k points within 1 second
        assert execution_time < 1.0, f"Deflection diagram too slow for large dataset: {execution_time:.3f}s"
        print(f"Large deflection diagram time: {execution_time:.4f} seconds")


class TestMemoryUsage:
    """Test memory usage and resource management"""
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def test_memory_usage_multiple_diagrams(self):
        """Test memory usage when creating multiple diagrams"""
        initial_memory = self.get_memory_usage()
        
        # Create many diagrams
        for i in range(100):
            span_lengths = [5.0, 6.0, 4.0]
            x_points = np.linspace(0, 15, 1000)
            shear = np.random.normal(0, 1000, 1000)
            moment = np.random.normal(0, 5000, 1000)
            deflection = np.random.normal(0, 10, 1000)
            reactions = [3000, 5000, 4500, 2500]
            
            fig1 = create_beam_diagram(span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions)
            fig2 = create_shear_diagram(x_points, shear)
            fig3 = create_moment_diagram(x_points, moment)
            fig4 = create_deflection_diagram(x_points, deflection)
            
            # Clear references to help garbage collection
            del fig1, fig2, fig3, fig4
        
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Excessive memory usage: {memory_increase:.1f} MB"
        print(f"Memory usage increase: {memory_increase:.1f} MB")
    
    def test_memory_cleanup_large_arrays(self):
        """Test memory cleanup with large arrays"""
        initial_memory = self.get_memory_usage()
        
        # Create and process large arrays
        large_arrays = []
        for i in range(10):
            n_points = 50000
            x_points = np.linspace(0, 100, n_points)
            data = np.random.normal(0, 1000, n_points)
            
            fig = create_shear_diagram(x_points, data)
            large_arrays.append((x_points, data, fig))
        
        # Clear all references
        del large_arrays
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Check memory after cleanup
        time.sleep(1)  # Give time for cleanup
        final_memory = self.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Memory should not increase excessively after cleanup
        assert memory_increase < 200, f"Memory not properly cleaned up: {memory_increase:.1f} MB"
        print(f"Memory after cleanup: {memory_increase:.1f} MB increase")


class TestStressScenarios:
    """Test stress scenarios and edge cases"""
    
    def test_concurrent_diagram_creation(self):
        """Test concurrent diagram creation"""
        results = []
        errors = []
        
        def create_diagrams():
            try:
                span_lengths = [5.0, 6.0]
                x_points = np.linspace(0, 11, 1000)
                shear = np.random.normal(0, 1000, 1000)
                reactions = [2500, 3000, 2500]
                
                fig = create_beam_diagram(span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions)
                fig2 = create_shear_diagram(x_points, shear)
                
                results.append(True)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads
        threads = []
        num_threads = 5
        
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=create_diagrams)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All threads should complete successfully
        assert len(results) == num_threads, f"Only {len(results)} out of {num_threads} threads completed"
        assert len(errors) == 0, f"Errors occurred: {errors}"
        
        # Should complete within reasonable time
        assert total_time < 10.0, f"Concurrent execution too slow: {total_time:.2f}s"
        
        print(f"Concurrent execution completed in {total_time:.2f} seconds")
    
    def test_extreme_data_values(self):
        """Test handling of extreme data values"""
        extreme_cases = [
            # Very large values
            (np.array([0, 10]), np.array([1e6, 1e6])),
            # Very small values
            (np.array([0, 10]), np.array([1e-6, 1e-6])),
            # Mixed extreme values
            (np.array([0, 5, 10]), np.array([-1e6, 0, 1e6])),
            # Many zeros
            (np.array([0, 5, 10, 15, 20]), np.array([0, 0, 0, 0, 0]))
        ]
        
        for x_points, data in extreme_cases:
            try:
                fig = create_shear_diagram(x_points, data)
                assert fig is not None, "Should create figure even with extreme values"
                
                fig2 = create_moment_diagram(x_points, data)
                assert fig2 is not None, "Should create moment diagram with extreme values"
                
            except Exception as e:
                pytest.fail(f"Failed to handle extreme values {data}: {e}")
    
    def test_rapid_sequential_creation(self):
        """Test rapid sequential diagram creation"""
        span_lengths = [5.0, 6.0, 4.0]
        reactions = [3000, 5000, 4500, 2500]
        
        start_time = time.time()
        
        # Rapidly create many diagrams
        for i in range(100):
            fig = create_beam_diagram(
                span_lengths, 1200 + i, 800 + i, [1.2, 1.6], 0, 0, reactions
            )
            
            # Verify figure is created
            assert fig is not None, f"Failed to create diagram {i}"
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / 100
        
        # Average creation time should be reasonable
        assert avg_time < 0.05, f"Average creation time too slow: {avg_time:.4f}s"
        
        print(f"Rapid creation: {avg_time:.4f}s average per diagram")


class TestScalability:
    """Test scalability with increasing problem sizes"""
    
    def test_scalability_span_count(self):
        """Test scalability with increasing number of spans"""
        span_counts = [1, 2, 5, 10, 20]
        times = []
        
        for num_spans in span_counts:
            span_lengths = [5.0] * num_spans
            reactions = [2000] * (num_spans + 1)
            
            start_time = time.time()
            
            fig = create_beam_diagram(
                span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            times.append(execution_time)
            
            print(f"Spans: {num_spans:2d}, Time: {execution_time:.4f}s")
        
        # Check that time doesn't grow exponentially
        for i in range(1, len(times)):
            time_ratio = times[i] / times[i-1]
            span_ratio = span_counts[i] / span_counts[i-1]
            
            # Time should not grow faster than O(n²)
            assert time_ratio <= span_ratio ** 2, f"Poor scalability: time ratio {time_ratio:.2f} vs span ratio {span_ratio:.2f}"
    
    def test_scalability_data_points(self):
        """Test scalability with increasing number of data points"""
        point_counts = [100, 500, 1000, 5000, 10000]
        times = []
        
        for num_points in point_counts:
            x_points = np.linspace(0, 50, num_points)
            shear = np.random.normal(0, 1000, num_points)
            
            start_time = time.time()
            
            fig = create_shear_diagram(x_points, shear)
            
            end_time = time.time()
            execution_time = end_time - start_time
            times.append(execution_time)
            
            print(f"Points: {num_points:5d}, Time: {execution_time:.4f}s")
        
        # Time should grow roughly linearly with data points
        for i in range(1, len(times)):
            time_ratio = times[i] / times[i-1]
            point_ratio = point_counts[i] / point_counts[i-1]
            
            # Allow some overhead but should be roughly linear
            assert time_ratio <= point_ratio * 2, f"Poor scalability: time ratio {time_ratio:.2f} vs point ratio {point_ratio:.2f}"


def run_performance_benchmark():
    """Run comprehensive performance benchmark"""
    print("🚀 RUNNING PERFORMANCE BENCHMARK")
    print("=" * 50)
    
    # Basic performance test
    print("\n📊 Basic Performance Tests...")
    
    test_runner = TestAdvancedAppPerformance()
    test_runner.test_beam_diagram_performance_small()
    test_runner.test_beam_diagram_performance_large()
    
    # Memory tests
    print("\n💾 Memory Usage Tests...")
    
    memory_tester = TestMemoryUsage()
    memory_tester.test_memory_usage_multiple_diagrams()
    
    # Stress tests
    print("\n🔥 Stress Tests...")
    
    stress_tester = TestStressScenarios()
    stress_tester.test_concurrent_diagram_creation()
    stress_tester.test_extreme_data_values()
    
    # Scalability tests
    print("\n📈 Scalability Tests...")
    
    scalability_tester = TestScalability()
    scalability_tester.test_scalability_span_count()
    
    print("\n✅ Performance benchmark completed!")


if __name__ == "__main__":
    run_performance_benchmark()
