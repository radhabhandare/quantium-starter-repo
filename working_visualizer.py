import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

print("="*60)
print("LOADING PINK MORSEL SALES DATA")
print("="*60)

# Load and check data
try:
    df = pd.read_csv('pink_morsels_sales.csv')
    print(f"✅ Data loaded: {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Regions: {df['region'].unique()}")
    
except Exception as e:
    print(f"❌ Error loading data: {e}")
    # Create dummy data for testing
    df = pd.DataFrame({
        'sales': [100, 200, 150, 300, 250],
        'date': pd.date_range('2021-01-01', periods=5),
        'region': ['north', 'south', 'east', 'west', 'north']
    })

# Price increase date
cutoff_date = pd.Timestamp('2021-01-15')

# Initialize Dash app
app = dash.Dash(__name__)

# Simple layout that will work
app.layout = html.Div([
    html.H1("Pink Morsel Sales Analysis", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'padding': '20px'}),
    
    html.Div([
        html.H3("Select Region to Filter:", style={'marginBottom': '10px'}),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            labelStyle={'display': 'inline-block', 'marginRight': '15px', 'padding': '5px'}
        )
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f0f8ff'}),
    
    dcc.Graph(id='sales-chart', style={'height': '500px', 'padding': '10px'}),
    
    html.Div(id='stats-output', 
             style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#e8f4f8', 
                    'borderRadius': '5px', 'textAlign': 'center'})
])

# Simple callback that will definitely work
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-output', 'children')],
    Input('region-radio', 'value')
)
def update_display(selected_region):
    print(f"Callback triggered with region: {selected_region}")
    
    try:
        # Filter data
        if selected_region == 'all':
            filtered_df = df
            region_label = "All Regions"
            line_color = '#3498db'
        else:
            filtered_df = df[df['region'] == selected_region]
            region_label = selected_region.capitalize()
            line_color = '#e74c3c' if selected_region == 'south' else \
                        '#2ecc71' if selected_region == 'east' else \
                        '#9b59b6' if selected_region == 'west' else '#3498db'
        
        print(f"Filtered data: {len(filtered_df)} rows")
        
        # Create basic figure
        fig = go.Figure()
        
        if len(filtered_df) > 0:
            fig.add_trace(go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['sales'],
                mode='lines+markers',
                name=f'{region_label} Sales',
                line=dict(color=line_color, width=2),
                marker=dict(size=6)
            ))
        
        # Add price increase line
        fig.add_vline(
            x=cutoff_date,
            line_dash="dash",
            line_color="red",
            annotation_text="Price Increase<br>Jan 15, 2021"
        )
        
        # Update layout
        fig.update_layout(
            title=f'Pink Morsel Sales - {region_label}',
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            yaxis_tickprefix="$",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Calculate stats
        before = filtered_df[filtered_df['date'] < cutoff_date]['sales'].sum() if len(filtered_df) > 0 else 0
        after = filtered_df[filtered_df['date'] >= cutoff_date]['sales'].sum() if len(filtered_df) > 0 else 0
        
        # Create stats output
        stats = html.Div([
            html.H4(f"Statistics for {region_label}"),
            html.P(f"Total Records: {len(filtered_df)}"),
            html.P(f"Total Sales: ${filtered_df['sales'].sum():,.2f}"),
            html.P(f"Sales before Jan 15, 2021: ${before:,.2f}"),
            html.P(f"Sales after Jan 15, 2021: ${after:,.2f}"),
            html.P(f"Impact: {'Decrease' if before > after else 'Increase'} of ${abs(before - after):,.2f}")
        ])
        
        return fig, stats
        
    except Exception as e:
        print(f"Error in callback: {e}")
        # Return empty figure and error message
        error_fig = go.Figure()
        error_fig.update_layout(
            title="Error Loading Data",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            plot_bgcolor='white'
        )
        
        error_message = html.Div([
            html.H4("Error occurred"),
            html.P(f"Error: {str(e)}"),
            html.P("Check your data file and try again.")
        ])
        
        return error_fig, error_message

if __name__ == '__main__':
    print("\n" + "="*60)
    print("STARTING DASH APPLICATION")
    print("="*60)
    print("Open your browser and go to: http://127.0.0.1:8050")
    print("="*60)
    app.run(debug=True)
    