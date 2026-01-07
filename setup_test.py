# Create a new test file
cat > setup_test.py << "EOF"
import dash
import pandas as pd
import sys

print("="*60)
print("QUANTIUM DASH ENVIRONMENT SETUP VERIFICATION")
print("="*60)
print(f"Python Version: {sys.version.split()[0]}")
print(f"Dash Version: {dash.__version__}")
print(f"Pandas Version: {pd.__version__}")
print("-"*60)

# Test Dash components
try:
    from dash import html, dcc
    print("✅ Dash HTML and Core components imported successfully")
except Exception as e:
    print(f"❌ Dash components import failed: {e}")

# Test pandas
try:
    df = pd.DataFrame({'data': [1, 2, 3], 'values': ['a', 'b', 'c']})
    print(f"✅ Pandas DataFrame created: {df.shape[0]} rows x {df.shape[1]} columns")
except Exception as e:
    print(f"❌ Pandas DataFrame creation failed: {e}")

print("="*60)
print("✅ ENVIRONMENT SETUP COMPLETE - READY FOR DASH DEVELOPMENT")
print("="*60)
EOF