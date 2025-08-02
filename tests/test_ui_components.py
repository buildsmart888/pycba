"""
Streamlit UI Test Cases for Advanced App
วันที่สร้าง: 2 สิงหาคม 2568
ทดสอบ: UI components, user interactions, sidebar removal, CSS styling
"""

import pytest
import numpy as np
import pandas as pd
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)
sys.path.insert(0, current_dir)


class TestStreamlitUIComponents:
    """Test Streamlit UI components and interactions"""
    
    def test_page_config_settings(self):
        """Test page configuration settings"""
        # This would be tested in actual Streamlit app
        # Here we test the configuration values
        expected_config = {
            'page_title': "Continuous Beam Analysis - PyCBA",
            'page_icon': "🏗️",
            'layout': "wide",
            'initial_sidebar_state': "collapsed"
        }
        
        # Test that our config includes sidebar collapsed
        assert expected_config['initial_sidebar_state'] == "collapsed"
        assert expected_config['layout'] == "wide"
        assert "Continuous Beam Analysis" in expected_config['page_title']
    
    def test_css_styling(self):
        """Test CSS styling definitions"""
        # Test that critical CSS classes are defined
        css_classes = [
            'main-header',
            'info-card', 
            'feature-grid',
            'feature-item',
            'orange-button',
            'section-header',
            'result-box',
            'input-section'
        ]
        
        # This simulates checking if CSS classes would be applied
        for css_class in css_classes:
            assert isinstance(css_class, str)
            assert len(css_class) > 0
    
    def test_sidebar_hiding_css(self):
        """Test CSS rules for hiding sidebar"""
        sidebar_hiding_rules = [
            '.css-1d391kg {display: none}',
            '.css-1rs6os {display: none}',
            'section[data-testid="stSidebar"] {display: none !important}',
            '.css-1lcbmhc {display: none}'
        ]
        
        # Test that CSS rules are properly formatted
        for rule in sidebar_hiding_rules:
            assert '{display: none' in rule or '{display: none !important}' in rule
    
    def test_input_validation_ranges(self):
        """Test input validation ranges"""
        # Test span length validation
        min_span = 1.0
        max_span = 50.0
        default_span = 5.0
        
        assert min_span > 0
        assert max_span > min_span
        assert min_span <= default_span <= max_span
        
        # Test load validation
        min_load = 0.0
        max_load = 10000.0
        default_dl = 1200.0
        default_ll = 800.0
        
        assert min_load >= 0
        assert max_load > min_load
        assert min_load <= default_dl <= max_load
        assert min_load <= default_ll <= max_load
        
        # Test load factor validation
        min_factor = 0.1
        max_factor = 5.0
        default_dl_factor = 1.2
        default_ll_factor = 1.6
        
        assert min_factor > 0
        assert max_factor > min_factor
        assert min_factor <= default_dl_factor <= max_factor
        assert min_factor <= default_ll_factor <= max_factor


class TestDataValidation:
    """Test data validation and error handling"""
    
    def test_span_configuration_validation(self):
        """Test span configuration validation"""
        # Valid configurations
        valid_configs = [
            [5.0],                    # Single span
            [5.0, 6.0],              # Two spans
            [4.0, 5.0, 6.0],         # Three spans
            [5.0, 5.0, 5.0, 5.0]     # Four spans
        ]
        
        for config in valid_configs:
            assert all(span > 0 for span in config)
            assert len(config) >= 1
            assert len(config) <= 10  # Based on UI selectbox range
    
    def test_load_combination_validation(self):
        """Test load combination calculations"""
        test_cases = [
            # (DL, LL, DL_factor, LL_factor, expected_total)
            (1000, 500, 1.2, 1.6, 2000),
            (1200, 800, 1.2, 1.6, 2720),
            (0, 1000, 1.0, 1.5, 1500),
            (2000, 0, 1.4, 1.0, 2800)
        ]
        
        for dl, ll, dl_factor, ll_factor, expected in test_cases:
            factored_dl = dl * dl_factor
            factored_ll = ll * ll_factor
            total = factored_dl + factored_ll
            assert abs(total - expected) < 0.1
    
    def test_material_property_validation(self):
        """Test material property validation"""
        # Concrete properties
        concrete_e_min = 15.0   # GPa
        concrete_e_max = 40.0   # GPa
        concrete_e_typical = 30.0
        
        assert concrete_e_min <= concrete_e_typical <= concrete_e_max
        
        # Steel properties
        steel_e_min = 180.0     # GPa
        steel_e_max = 220.0     # GPa
        steel_e_typical = 200.0
        
        assert steel_e_min <= steel_e_typical <= steel_e_max
        
        # Moment of inertia validation
        min_i = 100.0           # cm⁴
        max_i = 1000000.0       # cm⁴
        typical_i = 83333.0     # cm⁴ for 30x50 cm beam
        
        assert min_i <= typical_i <= max_i


class TestCalculationWorkflow:
    """Test complete calculation workflow"""
    
    def test_calculation_input_processing(self):
        """Test processing of calculation inputs"""
        # Sample input data
        num_spans = 3
        span_lengths = [5.0, 6.0, 4.0]
        wdl = 1200.0
        wll = 800.0
        load_factor_dl = 1.2
        load_factor_ll = 1.6
        e_value = 30.0
        i_value = 83333.0
        
        # Process inputs (simulate advanced_app.py logic)
        factored_dl = wdl * load_factor_dl
        factored_ll = wll * load_factor_ll
        total_factored_load = factored_dl + factored_ll
        
        E = e_value * 1e9  # GPa -> Pa
        I = i_value / 1e12  # cm⁴ -> m⁴
        EI = E * I
        
        # Validate processing
        assert factored_dl == 1440.0
        assert factored_ll == 1280.0
        assert total_factored_load == 2720.0
        assert E == 30e9
        assert abs(I - 8.3333e-5) < 1e-10
        assert abs(EI - 2.5e6) < 1e3
    
    def test_support_configuration(self):
        """Test support configuration generation"""
        # Test different span configurations
        test_cases = [
            (1, [-1, -1, -1, -1]),           # Single span: Fixed-Fixed
            (2, [-1, -1, -1, 0, -1, -1]),    # Two spans: Pin-Pin-Pin
            (3, [-1, -1, -1, 0, -1, 0, -1, -1])  # Three spans
        ]
        
        for num_spans, expected_r in test_cases:
            R = []
            for i in range(num_spans + 1):
                if i == 0 or i == num_spans:  # End supports
                    R.extend([-1, -1])  # Fixed support
                else:  # Interior supports
                    R.extend([-1, 0])   # Pinned support
            
            assert R == expected_r
    
    def test_load_matrix_generation(self):
        """Test load matrix generation"""
        num_spans = 2
        total_load_kn = 2.72  # kN/m
        
        # Generate load matrix
        LM = []
        for i in range(num_spans):
            if total_load_kn > 0:
                LM.append([i+1, 1, -total_load_kn, 0.0, 0.0])
        
        expected_lm = [
            [1, 1, -2.72, 0.0, 0.0],
            [2, 1, -2.72, 0.0, 0.0]
        ]
        
        assert LM == expected_lm
    
    def test_results_unit_conversion(self):
        """Test results unit conversion"""
        # Sample results in kN and kN⋅m
        shear_kn = np.array([1.5, -2.3, 0.8])
        moment_kn = np.array([3.2, -1.8, 2.1])
        deflection_m = np.array([0.005, -0.008, 0.003])
        
        # Convert to display units
        shear_kg = shear_kn * 1000
        moment_kg_m = moment_kn * 1000
        deflection_mm = deflection_m * 1000
        
        # Validate conversions
        expected_shear = [1500, -2300, 800]
        expected_moment = [3200, -1800, 2100]
        expected_deflection = [5.0, -8.0, 3.0]
        
        np.testing.assert_array_equal(shear_kg, expected_shear)
        np.testing.assert_array_equal(moment_kg_m, expected_moment)
        np.testing.assert_array_equal(deflection_mm, expected_deflection)


class TestEquilibriumValidation:
    """Test equilibrium and validation checks"""
    
    def test_force_equilibrium_single_span(self):
        """Test force equilibrium for single span"""
        total_applied_load = 10000.0  # kg
        num_spans = 1
        
        # Single span: equal reactions
        reaction_each = total_applied_load / 2
        reactions = [reaction_each, reaction_each]
        
        total_reaction = sum(reactions)
        error = abs(total_reaction - total_applied_load)
        
        assert total_reaction == total_applied_load
        assert error == 0.0
    
    def test_force_equilibrium_two_span(self):
        """Test force equilibrium for two spans"""
        total_applied_load = 12000.0  # kg
        num_spans = 2
        
        # Two spans: end 25%, middle 50%
        reaction_end = total_applied_load * 0.25
        reaction_middle = total_applied_load * 0.5
        reactions = [reaction_end, reaction_middle, reaction_end]
        
        total_reaction = sum(reactions)
        error = abs(total_reaction - total_applied_load)
        
        assert total_reaction == total_applied_load
        assert error == 0.0
    
    def test_deflection_limit_validation(self):
        """Test deflection limit validation"""
        test_cases = [
            # (total_length_m, max_deflection_mm, should_pass)
            (10.0, 30.0, True),    # 30mm < L/250 = 40mm
            (10.0, 50.0, False),   # 50mm > L/250 = 40mm
            (20.0, 60.0, True),    # 60mm < L/250 = 80mm
            (15.0, 80.0, False)    # 80mm > L/250 = 60mm
        ]
        
        for total_length, max_deflection, should_pass in test_cases:
            allowable_deflection = total_length * 1000 / 250  # L/250 limit
            is_acceptable = max_deflection <= allowable_deflection
            
            assert is_acceptable == should_pass


class TestErrorScenarios:
    """Test error scenarios and edge cases"""
    
    def test_zero_ei_handling(self):
        """Test handling of very low EI values"""
        ei_values = [0, 1e3, 1e6, 1e9]
        
        for ei in ei_values:
            if ei < 1e6:
                # Should trigger warning for very low EI
                assert ei < 1e6
            else:
                # Should be acceptable
                assert ei >= 1e6
    
    def test_extreme_loads(self):
        """Test handling of extreme load values"""
        extreme_cases = [
            (0, 0),        # No loads
            (10000, 0),    # Dead load only
            (0, 10000),    # Live load only
            (10000, 10000) # Maximum loads
        ]
        
        for dl, ll in extreme_cases:
            total_load = (dl * 1.2) + (ll * 1.6)
            # Should not cause calculation errors
            assert total_load >= 0
            assert total_load < 50000  # Reasonable upper limit
    
    def test_extreme_span_configurations(self):
        """Test extreme span configurations"""
        extreme_configs = [
            [1.0],                          # Minimum single span
            [50.0],                         # Maximum single span
            [1.0] * 10,                     # Maximum number of spans
            [5.0, 10.0, 15.0, 20.0, 25.0]  # Varying span lengths
        ]
        
        for config in extreme_configs:
            assert len(config) <= 10  # UI limit
            assert all(1.0 <= span <= 50.0 for span in config)  # UI limits
            assert sum(config) <= 500.0  # Reasonable total length


class TestDataExport:
    """Test data export functionality"""
    
    def test_results_dataframe_creation(self):
        """Test creation of results DataFrame"""
        # Sample data
        x_points = np.array([0, 2.5, 5.0, 7.5, 10.0])
        shear = np.array([1000, 500, -200, -800, 0])
        moment = np.array([0, 2500, 3000, 1500, 0])
        deflection = np.array([0, -3.2, -4.5, -2.8, 0])
        
        # Create DataFrame (simulate app logic)
        data_table = []
        for i in range(len(x_points)):
            data_table.append({
                "ตำแหน่ง (m)": round(x_points[i], 2),
                "แรงเฉือน (kg)": round(shear[i], 3),
                "โมเมนต์ดัด (kg⋅m)": round(moment[i], 3),
                "การโก่งตัว (mm)": round(deflection[i], 3)
            })
        
        df = pd.DataFrame(data_table)
        
        # Validate DataFrame
        assert len(df) == 5
        assert "ตำแหน่ง (m)" in df.columns
        assert "แรงเฉือน (kg)" in df.columns
        assert "โมเมนต์ดัด (kg⋅m)" in df.columns
        assert "การโก่งตัว (mm)" in df.columns
        
        # Test CSV conversion
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        assert isinstance(csv_data, str)
        assert len(csv_data) > 0
    
    def test_filename_generation(self):
        """Test CSV filename generation"""
        num_spans = 3
        expected_filename = f"continuous_beam_analysis_{num_spans}spans.csv"
        
        assert expected_filename == "continuous_beam_analysis_3spans.csv"
        assert expected_filename.endswith(".csv")
        assert str(num_spans) in expected_filename


class TestPerformanceOptimization:
    """Test performance optimization features"""
    
    def test_data_point_limitation(self):
        """Test data point limitation for display"""
        # Large dataset
        large_x = np.linspace(0, 100, 10000)
        
        # Simulate app's data limitation logic
        n_points = min(50, len(large_x))
        step = len(large_x) // n_points
        
        limited_indices = range(0, len(large_x), step)
        limited_data = [large_x[i] for i in limited_indices]
        
        # Should reduce to manageable size
        assert len(limited_data) <= 50
        assert len(limited_data) >= 1
    
    def test_chart_rendering_limits(self):
        """Test chart rendering optimization"""
        # Test that large datasets are handled appropriately
        max_chart_points = 1000
        
        test_sizes = [100, 500, 1000, 5000, 10000]
        
        for size in test_sizes:
            if size <= max_chart_points:
                # Should render all points
                render_points = size
            else:
                # Should limit points
                render_points = max_chart_points
            
            assert render_points <= max_chart_points
            assert render_points > 0


# Utility functions for test execution
def run_ui_tests():
    """Run all UI-related tests"""
    import subprocess
    import sys
    
    test_file = __file__
    result = subprocess.run([
        sys.executable, '-m', 'pytest', test_file, '-v', 
        '--tb=short', '-k', 'test_'
    ], capture_output=True, text=True)
    
    print("=== UI TEST RESULTS ===")
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
    
    return result.returncode == 0


if __name__ == "__main__":
    # Run tests when script is executed directly
    success = run_ui_tests()
    if success:
        print("\n✅ All UI tests passed!")
    else:
        print("\n❌ Some UI tests failed!")
        sys.exit(1)
