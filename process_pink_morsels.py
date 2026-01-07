import pandas as pd
import os
import glob

print("Processing Pink Morsel sales data...")
print("="*50)

# Get all CSV files in data folder
csv_files = glob.glob('data/*.csv')
print(f"Found {len(csv_files)} CSV files")

all_data = []

for file_path in csv_files:
    # Read CSV
    df = pd.read_csv(file_path)
    file_name = os.path.basename(file_path)
    
    # Filter for pink morsels only
    pink_data = df[df['product'] == 'pink morsel'].copy()
    
    if len(pink_data) > 0:
        # Clean price (remove $) and convert to float
        pink_data['price'] = pink_data['price'].str.replace('$', '', regex=False).astype(float)
        
        # Calculate sales
        pink_data['sales'] = pink_data['price'] * pink_data['quantity']
        
        # Keep only needed columns
        pink_data = pink_data[['sales', 'date', 'region']]
        
        all_data.append(pink_data)
        
        print(f"  {file_name}: {len(df)} rows → {len(pink_data)} pink morsels")

# Combine all data
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Convert date and sort
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    combined_df = combined_df.sort_values('date')
    
    # Save to CSV
    combined_df.to_csv('pink_morsels_sales.csv', index=False)
    
    print("\n" + "="*50)
    print(f"✅ SUCCESS: Created 'pink_morsels_sales.csv'")
    print(f"   Total rows: {len(combined_df)}")
    print(f"   Columns: {list(combined_df.columns)}")
    
    # Show sample
    print("\nSample data (first 5 rows):")
    print(combined_df.head())
    
else:
    print("❌ No pink morsel data found!")

print("="*50)