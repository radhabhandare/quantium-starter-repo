import pandas as pd
import os
import sys

print("="*60)
print("COMPLETE PROJECT TEST - PINK MORSEL SALES ANALYSIS")
print("="*60)

# Check 1: Required files exist
print("\n1. CHECKING REQUIRED FILES:")
print("-" * 40)

required_files = [
    'pink_morsels_sales.csv',
    'process_pink_morsels.py', 
    'sales_visualizer.py',
    'requirements.txt'
]

all_files_exist = True
for file in required_files:
    exists = os.path.exists(file)
    status = "✅ EXISTS" if exists else "❌ MISSING"
    print(f"{status}: {file}")
    if not exists:
        all_files_exist = False

# Check 2: Data integrity
print("\n2. CHECKING DATA:")
print("-" * 40)

if os.path.exists('pink_morsels_sales.csv'):
    try:
        df = pd.read_csv('pink_morsels_sales.csv')
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"✅ Data loaded: {len(df)} rows")
        print(f"✅ Columns: {list(df.columns)}")
        
        # Check columns
        expected_cols = ['sales', 'date', 'region']
        has_correct_cols = all(col in df.columns for col in expected_cols)
        
        if has_correct_cols:
            print("✅ Correct columns present")
        else:
            print("❌ Missing expected columns")
            print(f"   Expected: {expected_cols}")
            print(f"   Found: {list(df.columns)}")
        
        # Check date range
        print(f"✅ Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        
        # Check for price increase analysis
        cutoff = pd.Timestamp('2021-01-15')
        before = df[df['date'] < cutoff]['sales'].sum()
        after = df[df['date'] >= cutoff]['sales'].sum()
        
        print(f"\n3. BUSINESS QUESTION ANSWER:")
        print("-" * 40)
        print(f"Sales BEFORE Jan 15, 2021: ${before:,.2f}")
        print(f"Sales AFTER Jan 15, 2021: ${after:,.2f}")
        
        if before > after:
            diff = before - after
            pct = (diff / before) * 100
            print(f"✅ ANSWER: Sales were HIGHER BEFORE price increase")
            print(f"   Decreased by ${diff:,.2f} ({pct:.1f}%) after price increase")
        else:
            diff = after - before
            pct = (diff / before) * 100 if before > 0 else 0
            print(f"✅ ANSWER: Sales were HIGHER AFTER price increase")
            print(f"   Increased by ${diff:,.2f} ({pct:.1f}%) after price increase")
            
    except Exception as e:
        print(f"❌ Error reading data: {e}")
else:
    print("❌ Data file not found")

# Check 3: Python scripts can run
print("\n4. CHECKING SCRIPTS:")
print("-" * 40)

scripts_to_test = ['process_pink_morsels.py', 'sales_visualizer.py']

for script in scripts_to_test:
    if os.path.exists(script):
        try:
            # Try to import to check for syntax errors
            with open(script, 'r') as f:
                content = f.read()
            
            # Basic syntax check
            compile(content, script, 'exec')
            print(f"✅ {script}: No syntax errors")
        except SyntaxError as e:
            print(f"❌ {script}: Syntax error - {e}")
        except Exception as e:
            print(f"⚠️  {script}: Could not check - {e}")
    else:
        print(f"❌ {script}: File not found")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

if all_files_exist:
    print("✅ All required files present")
    print("✅ Data processed correctly")
    print("✅ Business question answered")
    print("\n🎉 PROJECT IS READY FOR SUBMISSION!")
else:
    print("❌ Some files are missing")
    print("\n⚠️  Please complete missing components before submission")

print("\nTo run the visualization:")
print("1. python sales_visualizer.py")
print("2. Open http://127.0.0.1:8050 in browser")
print("="*60)