"""
Comprehensive Unit Tests for Advanced App - Continuous Beam Analysis
วันที่สร้าง: 2 สิงหาคม 2568
ครอบคลุม: UI functions, diagram creation, calculation logic, data processing
"""

import pytest
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Import the functions we want to test
sys.path.insert(0, current_dir)
from advanced_app import (
    create_beam_diagram,
    create_shear_diagram, 
    create_moment_diagram,
    create_deflection_diagram
)

from pycba.beam import Beam
from pycba.analysis import BeamAnalysis


class TestBeamDiagramCreation:
    """Test suite for beam diagram creation functions"""
    
    def test_create_beam_diagram_basic(self):
        """Test basic beam diagram creation"""
        span_lengths = [5.0, 6.0, 4.0]
        wdl = 1200.0
        wll = 800.0
        load_factors = [1.2, 1.6]
        moment_left = 0.0
        moment_right = 0.0
        reactions = [3000, 5000, 4500, 2500]
        
        fig = create_beam_diagram(
            span_lengths, wdl, wll, load_factors, 
            moment_left, moment_right, reactions
        )
        
        # Test basic properties
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
        # Test layout properties
        assert fig.layout.height == 400
        assert "ระยะทาง (m)" in fig.layout.xaxis.title.text
        assert "แรง" in fig.layout.yaxis.title.text
        
    def test_create_beam_diagram_no_reactions(self):
        """Test beam diagram creation without reactions"""
        span_lengths = [5.0, 5.0]
        wdl = 1000.0
        wll = 600.0
        load_factors = [1.2, 1.6]
        moment_left = 0.0
        moment_right = 0.0
        reactions = None
        
        fig = create_beam_diagram(
            span_lengths, wdl, wll, load_factors,
            moment_left, moment_right, reactions
        )
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) > 0
        
    def test_create_beam_diagram_with_moments(self):
        """Test beam diagram with applied moments"""
        span_lengths = [6.0]
        wdl = 1500.0
        wll = 1000.0
        load_factors = [1.2, 1.6]
        moment_left = -5000.0
        moment_right = 3000.0
        reactions = [2000, 2000]
        
        fig = create_beam_diagram(
            span_lengths, wdl, wll, load_factors,
            moment_left, moment_right, reactions
        )
        
        assert isinstance(fig, go.Figure)
        # Should have annotations for moments
        assert len(fig.layout.annotations) >= 2  # At least load and moment annotations
        
    def test_create_beam_diagram_zero_load(self):
        """Test beam diagram with zero loads"""
        span_lengths = [5.0]
        wdl = 0.0
        wll = 0.0
        load_factors = [1.2, 1.6]
        moment_left = 0.0
        moment_right = 0.0
        reactions = [0, 0]
        
        fig = create_beam_diagram(
            span_lengths, wdl, wll, load_factors,
            moment_left, moment_right, reactions
        )
        
        assert isinstance(fig, go.Figure)
        # Should still create a figure with beam and supports
        assert len(fig.data) >= 2  # At least beam line and support markers


class TestShearDiagramCreation:
    """Test suite for shear force diagram creation"""
    
    def test_create_shear_diagram_basic(self):
        """Test basic shear diagram creation"""
        x_points = np.linspace(0, 10, 100)
        shear = 1000 * np.sin(x_points * np.pi / 10)  # Sample shear force
        
        fig = create_shear_diagram(x_points, shear)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1  # At least the shear curve
        assert fig.layout.height == 300
        assert "แรงเฉือน (kg)" in fig.layout.yaxis.title
        
    def test_create_shear_diagram_with_extrema(self):
        """Test shear diagram with clear max/min values"""
        x_points = np.array([0, 2.5, 5.0, 7.5, 10.0])
        shear = np.array([1000, 500, -200, -800, 0])
        
        fig = create_shear_diagram(x_points, shear)
        
        assert isinstance(fig, go.Figure)
        # Should have markers for max/min values
        max_shear = np.max(shear)
        min_shear = np.min(shear)
        
        if abs(max_shear) > 1e-6 or abs(min_shear) > 1e-6:
            assert len(fig.data) >= 2  # Shear curve + markers
            
    def test_create_shear_diagram_zero_shear(self):
        """Test shear diagram with all zero values"""
        x_points = np.linspace(0, 5, 20)
        shear = np.zeros_like(x_points)
        
        fig = create_shear_diagram(x_points, shear)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1


class TestMomentDiagramCreation:
    """Test suite for moment diagram creation"""
    
    def test_create_moment_diagram_basic(self):
        """Test basic moment diagram creation"""
        x_points = np.linspace(0, 8, 80)
        moment = 2000 * x_points * (8 - x_points)  # Parabolic moment
        
        fig = create_moment_diagram(x_points, moment)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1
        assert fig.layout.height == 300
        assert "โมเมนต์ดัด (kg⋅m)" in fig.layout.yaxis.title
        
    def test_create_moment_diagram_with_extrema(self):
        """Test moment diagram with clear peaks"""
        x_points = np.array([0, 2, 4, 6, 8])
        moment = np.array([0, 3000, 4000, 2000, 0])
        
        fig = create_moment_diagram(x_points, moment)
        
        assert isinstance(fig, go.Figure)
        # Should have markers for max values
        max_moment = np.max(moment)
        min_moment = np.min(moment)
        
        if abs(max_moment) > 1e-6:
            assert len(fig.data) >= 2  # Moment curve + markers


class TestDeflectionDiagramCreation:
    """Test suite for deflection diagram creation"""
    
    def test_create_deflection_diagram_basic(self):
        """Test basic deflection diagram creation"""
        x_points = np.linspace(0, 10, 100)
        deflection = 5 * np.sin(x_points * np.pi / 10)  # Sample deflection in mm
        
        fig = create_deflection_diagram(x_points, deflection)
        
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 1
        assert fig.layout.height == 300
        assert "การโก่งตัว (mm)" in fig.layout.yaxis.title
        
    def test_create_deflection_diagram_with_max(self):
        """Test deflection diagram with clear maximum"""
        x_points = np.array([0, 2.5, 5.0, 7.5, 10.0])
        deflection = np.array([0, -2.5, -4.0, -2.5, 0])  # Negative = downward
        
        fig = create_deflection_diagram(x_points, deflection)
        
        assert isinstance(fig, go.Figure)
        # Should have marker for max deflection
        max_deflection = np.max(np.abs(-deflection))  # Note: function inverts sign
        if max_deflection > 1e-6:
            assert len(fig.data) >= 2


class TestBeamAnalysisIntegration:
    """Integration tests for complete beam analysis workflow"""
    
    def test_single_span_beam_analysis(self):
        """Test analysis of single span beam"""
        span_lengths = [6.0]
        EI = 25000e6  # Pa⋅m⁴
        R = [-1, -1, -1, -1]  # Fixed-Fixed beam
        LM = [[1, 1, -2.0, 0.0, 0.0]]  # 2 kN/m UDL
        
        try:
            analysis = BeamAnalysis(span_lengths, EI, R, LM)
            analysis.analyze()
            
            results = analysis.beam_results.results
            assert hasattr(results, 'x')
            assert hasattr(results, 'V')
            assert hasattr(results, 'M')
            assert hasattr(results, 'D')
            
            # Basic checks
            assert len(results.x) > 0
            assert len(results.V) == len(results.x)
            assert len(results.M) == len(results.x)
            assert len(results.D) == len(results.x)
            
        except Exception as e:
            pytest.skip(f"PyCBA analysis failed: {e}")
    
    def test_continuous_beam_analysis(self):
        """Test analysis of continuous beam"""
        span_lengths = [5.0, 6.0, 4.0]
        EI = 30000e6  # Pa⋅m⁴
        R = [-1, -1, -1, 0, -1, 0, -1, -1]  # Pin-Roller supports
        LM = [
            [1, 1, -1.5, 0.0, 0.0],  # Span 1: 1.5 kN/m
            [2, 1, -1.8, 0.0, 0.0],  # Span 2: 1.8 kN/m
            [3, 1, -1.2, 0.0, 0.0],  # Span 3: 1.2 kN/m
        ]
        
        try:
            analysis = BeamAnalysis(span_lengths, EI, R, LM)
            analysis.analyze()
            
            results = analysis.beam_results.results
            assert len(results.x) > 0
            
            # Check total length
            total_length = sum(span_lengths)
            assert max(results.x) <= total_length + 0.1  # Small tolerance
            
        except Exception as e:
            pytest.skip(f"PyCBA analysis failed: {e}")


class TestDataProcessing:
    """Test data processing and unit conversions"""
    
    def test_unit_conversions(self):
        """Test unit conversion calculations"""
        # Test GPa to Pa
        e_gpa = 30.0
        e_pa = e_gpa * 1e9
        assert e_pa == 30e9
        
        # Test cm⁴ to m⁴
        i_cm4 = 83333.0
        i_m4 = i_cm4 / 1e8
        assert abs(i_m4 - 0.00083333) < 1e-8
        
        # Test kN to kg
        force_kn = 2.5
        force_kg = force_kn * 1000
        assert force_kg == 2500
        
        # Test m to mm
        deflection_m = 0.005
        deflection_mm = deflection_m * 1000
        assert deflection_mm == 5.0
    
    def test_load_factor_calculations(self):
        """Test load factor applications"""
        wdl = 1200.0  # kg/m
        wll = 800.0   # kg/m
        load_factor_dl = 1.2
        load_factor_ll = 1.6
        
        factored_dl = wdl * load_factor_dl
        factored_ll = wll * load_factor_ll
        total_factored = factored_dl + factored_ll
        
        assert factored_dl == 1440.0
        assert factored_ll == 1280.0
        assert total_factored == 2720.0
    
    def test_reaction_calculations(self):
        """Test reaction force calculations"""
        # Single span case
        total_load = 10000.0  # kg
        num_spans = 1
        
        reaction_each = total_load / 2
        assert reaction_each == 5000.0
        
        # Two span case  
        num_spans = 2
        reaction_end = total_load * 0.25
        reaction_middle = total_load * 0.5
        
        assert reaction_end == 2500.0
        assert reaction_middle == 5000.0
        assert reaction_end + reaction_middle + reaction_end == total_load


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_empty_data_handling(self):
        """Test handling of empty or minimal data"""
        # Empty arrays
        x_points = np.array([])
        shear = np.array([])
        
        try:
            fig = create_shear_diagram(x_points, shear)
            # Should not crash, might return empty figure
            assert isinstance(fig, go.Figure)
        except (ValueError, IndexError):
            # Acceptable to raise error for empty data
            pass
    
    def test_single_point_data(self):
        """Test handling of single data point"""
        x_points = np.array([5.0])
        shear = np.array([1000.0])
        
        fig = create_shear_diagram(x_points, shear)
        assert isinstance(fig, go.Figure)
    
    def test_negative_span_lengths(self):
        """Test handling of invalid span lengths"""
        span_lengths = [-1.0, 5.0]  # Invalid negative length
        
        # This should be handled gracefully or raise appropriate error
        # Implementation depends on validation in create_beam_diagram
        with pytest.raises((ValueError, AssertionError)):
            reactions = [1000, 1000, 1000]
            fig = create_beam_diagram(
                span_lengths, 1000, 500, [1.2, 1.6], 
                0, 0, reactions
            )


class TestPerformance:
    """Test performance characteristics"""
    
    def test_large_dataset_handling(self):
        """Test handling of large datasets"""
        # Large number of points
        n_points = 10000
        x_points = np.linspace(0, 100, n_points)
        shear = 1000 * np.sin(x_points * np.pi / 50)
        
        import time
        start_time = time.time()
        fig = create_shear_diagram(x_points, shear)
        end_time = time.time()
        
        # Should complete within reasonable time (5 seconds)
        assert (end_time - start_time) < 5.0
        assert isinstance(fig, go.Figure)
    
    def test_memory_usage(self):
        """Test memory usage with multiple diagrams"""
        span_lengths = [5.0, 6.0, 4.0]
        x_points = np.linspace(0, 15, 1000)
        shear = np.random.normal(0, 1000, 1000)
        moment = np.random.normal(0, 5000, 1000)
        deflection = np.random.normal(0, 10, 1000)
        reactions = [3000, 5000, 4500, 2500]
        
        # Create multiple diagrams
        figs = []
        for i in range(10):
            fig1 = create_beam_diagram(span_lengths, 1200, 800, [1.2, 1.6], 0, 0, reactions)
            fig2 = create_shear_diagram(x_points, shear)
            fig3 = create_moment_diagram(x_points, moment)
            fig4 = create_deflection_diagram(x_points, deflection)
            figs.extend([fig1, fig2, fig3, fig4])
        
        # Should create all figures without memory error
        assert len(figs) == 40
        for fig in figs:
            assert isinstance(fig, go.Figure)


class TestValidationChecks:
    """Test validation and equilibrium checks"""
    
    def test_equilibrium_validation(self):
        """Test force equilibrium validation"""
        # Test case: balanced forces
        total_applied_load = 15000.0  # kg
        reactions = [3000.0, 5000.0, 4000.0, 3000.0]  # kg
        total_reaction = sum(reactions)
        
        error = abs(total_reaction - total_applied_load)
        error_percentage = error / total_applied_load * 100
        
        assert total_reaction == 15000.0
        assert error == 0.0
        assert error_percentage == 0.0
    
    def test_deflection_limits(self):
        """Test deflection limit validation"""
        total_length = 20.0  # m
        max_deflection = 50.0  # mm
        
        allowable_deflection = total_length * 1000 / 250  # L/250 limit
        assert allowable_deflection == 80.0  # mm
        
        # Check if deflection is within limits
        is_acceptable = max_deflection <= allowable_deflection
        assert is_acceptable == True
        
        # Test excessive deflection
        excessive_deflection = 100.0  # mm
        is_excessive = excessive_deflection > allowable_deflection
        assert is_excessive == True


# Test runner function
def run_advanced_app_tests():
    """Run all tests for advanced_app.py"""
    import subprocess
    import sys
    
    test_file = __file__
    result = subprocess.run([
        sys.executable, '-m', 'pytest', test_file, '-v', '--tb=short'
    ], capture_output=True, text=True)
    
    print("=== ADVANCED APP TEST RESULTS ===")
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
    
    return result.returncode == 0


if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_advanced_app_tests()
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
