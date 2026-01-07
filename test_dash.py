import dash
import pandas as pd

print("Testing Quantium Dash setup...")
print("-" * 40)

# Check versions
print(f"Python: {pd.__version__} (pandas)")
print(f"Dash: {dash.__version__}")

# Test basic functionality
app = dash.Dash(__name__)
df = pd.DataFrame({'test': [1, 2, 3]})

print("-" * 40)
print("✅ All tests passed!")
print("Setup complete and working.")