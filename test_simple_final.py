"""
Simple test that works with fixed_visualizer.py
Tests the three required components:
1. Header is present
2. Visualization is present  
3. Region picker is present
"""
import sys

print("="*60)
print("SIMPLE TEST FOR FIXED_VISUALIZER.PY")
print("="*60)

# Import your app
try:
    from fixed_visualizer import app
    print("✅ Successfully imported app")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Make sure fixed_visualizer.py exists in the same directory")
    sys.exit(1)

# Helper function to check component types
def check_component_type(component, target_type):
    """Check if component is of target type"""
    return target_type in str(type(component))

# Helper function to find components
def find_components(component, component_list=None):
    """Recursively find all components"""
    if component_list is None:
        component_list = []
    
    component_list.append(component)
    
    if hasattr(component, 'children'):
        children = component.children
        if isinstance(children, list):
            for child in children:
                find_components(child, component_list)
        elif children:
            find_components(children, component_list)
    
    return component_list

print("\n" + "="*60)
print("RUNNING TESTS")
print("="*60)

# Get all components
all_components = find_components(app.layout)

# Test 1: Check for header (H1)
print("\n📋 Test 1: Checking for header...")
h1_components = [c for c in all_components if check_component_type(c, 'H1')]
if h1_components:
    print(f"✅ PASS: Found {len(h1_components)} H1 header(s)")
    for h1 in h1_components:
        if hasattr(h1, 'children'):
            print(f"   Text: {h1.children}")
else:
    print("❌ FAIL: No H1 header found")

# Test 2: Check for visualization (Graph)
print("\n📊 Test 2: Checking for visualization...")
graph_components = [c for c in all_components if check_component_type(c, 'Graph')]
if graph_components:
    print(f"✅ PASS: Found {len(graph_components)} Graph component(s)")
    for graph in graph_components:
        if hasattr(graph, 'id'):
            print(f"   ID: {graph.id}")
else:
    print("❌ FAIL: No Graph component found")

# Test 3: Check for region picker (RadioItems)
print("\n📍 Test 3: Checking for region picker...")
radio_components = [c for c in all_components if check_component_type(c, 'RadioItems')]
if radio_components:
    print(f"✅ PASS: Found {len(radio_components)} RadioItems component(s)")
    for radio in radio_components:
        if hasattr(radio, 'id'):
            print(f"   ID: {radio.id}")
        if hasattr(radio, 'options'):
            print(f"   Options: {len(radio.options)}")
            # Check for region options
            for opt in radio.options[:3]:  # Show first 3
                if 'value' in opt:
                    print(f"     - {opt.get('value')}")
else:
    print("❌ FAIL: No RadioItems component found")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

test1 = len(h1_components) > 0
test2 = len(graph_components) > 0  
test3 = len(radio_components) > 0

print(f"1. Header present: {'✅ PASS' if test1 else '❌ FAIL'}")
print(f"2. Visualization present: {'✅ PASS' if test2 else '❌ FAIL'}")
print(f"3. Region picker present: {'✅ PASS' if test3 else '❌ FAIL'}")

all_passed = test1 and test2 and test3
print("\n" + "="*60)
if all_passed:
    print("🎉 ALL TESTS PASSED!")
else:
    print("⚠️  SOME TESTS FAILED")
print("="*60)

# Exit with appropriate code
sys.exit(0 if all_passed else 1)