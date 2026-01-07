"""
Pytest version of the simple test
"""
import pytest
from fixed_visualizer import app

def get_all_components(component):
    """Get all components recursively"""
    components = [component]
    
    if hasattr(component, 'children'):
        children = component.children
        if isinstance(children, list):
            for child in children:
                components.extend(get_all_components(child))
        elif children:
            components.extend(get_all_components(children))
    
    return components

# Get all components once
all_components = get_all_components(app.layout)

def test_header_exists():
    """Test 1: Header is present"""
    h1_found = any('H1' in str(type(c)) for c in all_components)
    assert h1_found, "No H1 header found in the app"
    print("✅ Header test passed")

def test_visualization_exists():
    """Test 2: Visualization is present"""
    graph_found = any('Graph' in str(type(c)) for c in all_components)
    assert graph_found, "No Graph/visualization found in the app"
    print("✅ Visualization test passed")

def test_region_picker_exists():
    """Test 3: Region picker is present"""
    radio_found = any('RadioItems' in str(type(c)) for c in all_components)
    assert radio_found, "No RadioItems (region picker) found in the app"
    print("✅ Region picker test passed")