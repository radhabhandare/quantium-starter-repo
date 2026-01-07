import pandas as pd
import os

print("="*60)
print("DEBUG DATA CHECK")
print("="*60)

# Check if file exists
if not os.path.exists('pink_morsels_sales.csv'):
    print("❌ ERROR: pink_morsels_sales.csv not found!")
    print("Run process_pink_morsels.py first to create this file.")
    exit(1)

# Try to load data
try:
    df = pd.read_csv('pink_morsels_sales.csv')
    print(f"✅ File loaded: {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    print(f"\nData types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    print(f"\nChecking for issues:")
    
    # Check date column
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
            print(f"✅ Date column can be converted to datetime")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        except Exception as e:
            print(f"❌ Date conversion error: {e}")
            print(f"   Sample dates: {df['date'].head().tolist()}")
    else:
        print("❌ No 'date' column found!")
        print(f"   Available columns: {list(df.columns)}")
    
    # Check sales column
    if 'sales' in df.columns:
        print(f"✅ Sales column found")
        print(f"   Sales total: ${df['sales'].sum():,.2f}")
        print(f"   Sales min/max: ${df['sales'].min():,.2f} / ${df['sales'].max():,.2f}")
    else:
        print("❌ No 'sales' column found!")
    
    # Check region column
    if 'region' in df.columns:
        print(f"✅ Region column found")
        print(f"   Unique regions: {df['region'].unique().tolist()}")
    else:
        print("❌ No 'region' column found!")
    
    # Check for NaN values
    print(f"\nMissing values:")
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            print(f"  ❌ {col}: {missing} missing values")
        else:
            print(f"  ✅ {col}: No missing values")
    
    # Create a test dataframe for debugging
    test_df = df.copy()
    if 'date' in test_df.columns:
        test_df['date'] = pd.to_datetime(test_df['date'], errors='coerce')
    
    print(f"\n" + "="*60)
    print("CREATING CLEAN DATA FILE FOR DEBUGGING")
    print("="*60)
    
    # Save a clean version
    clean_df = df.copy()
    
    # Ensure date is datetime
    if 'date' in clean_df.columns:
        clean_df['date'] = pd.to_datetime(clean_df['date'], errors='coerce')
        # Remove rows with invalid dates
        clean_df = clean_df.dropna(subset=['date'])
    
    # Ensure sales is numeric
    if 'sales' in clean_df.columns:
        clean_df['sales'] = pd.to_numeric(clean_df['sales'], errors='coerce')
        clean_df = clean_df.dropna(subset=['sales'])
    
    clean_df.to_csv('pink_morsels_clean.csv', index=False)
    print(f"✅ Clean data saved: pink_morsels_clean.csv ({len(clean_df)} rows)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()