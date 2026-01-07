import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Load the data you created in the previous task
df = pd.read_csv('pink_morsels_sales.csv')
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

print("="*60)
print("PINK MORSEL SALES VISUALIZER")
print("="*60)
print(f"Data loaded: {len(df)} records")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Total sales: ${df['sales'].sum():,.2f}")
print("="*60)

# Calculate sales before/after Jan 15, 2021
cutoff_date = pd.Timestamp('2021-01-15')
before_sales = df[df['date'] < cutoff_date]['sales'].sum()
after_sales = df[df['date'] >= cutoff_date]['sales'].sum()

print(f"Sales BEFORE {cutoff_date.date()}: ${before_sales:,.2f}")
print(f"Sales AFTER {cutoff_date.date()}: ${after_sales:,.2f}")

if before_sales > after_sales:
    print(f"📉 Sales DECREASED after price increase by ${before_sales - after_sales:,.2f}")
else:
    print(f"📈 Sales INCREASED after price increase by ${after_sales - before_sales:,.2f}")
print("="*60)

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Header
    html.H1("Pink Morsel Sales Analysis", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    # Subtitle
    html.P("Visualizing sales before and after the price increase on January 15, 2021",
           style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),
    
    # Key metrics row
    html.Div([
        html.Div([
            html.H3(f"${before_sales:,.2f}", style={'color': '#27ae60', 'textAlign': 'center'}),
            html.P("Total Sales BEFORE Jan 15, 2021", style={'textAlign': 'center'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'margin': '5px'}),
        
        html.Div([
            html.H3(f"${after_sales:,.2f}", style={'color': '#e74c3c', 'textAlign': 'center'}),
            html.P("Total Sales AFTER Jan 15, 2021", style={'textAlign': 'center'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'margin': '5px'}),
        
        html.Div([
            html.H3(f"{'Decrease' if before_sales > after_sales else 'Increase'}", 
                   style={'color': '#f39c12', 'textAlign': 'center'}),
            html.P("Price Increase Impact", style={'textAlign': 'center'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px', 'margin': '5px'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Line chart
    dcc.Graph(
        id='sales-line-chart',
        figure={
            'data': [
                # Line for all sales
                go.Scatter(
                    x=df['date'],
                    y=df['sales'],
                    mode='lines+markers',
                    name='Daily Sales',
                    line=dict(color='#3498db', width=2),
                    marker=dict(size=4),
                    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>'
                ),
                # Vertical line for price increase date
                go.Scatter(
                    x=[cutoff_date, cutoff_date],
                    y=[0, df['sales'].max() * 1.1],
                    mode='lines',
                    name='Price Increase (Jan 15, 2021)',
                    line=dict(color='#e74c3c', width=2, dash='dash'),
                    hoverinfo='none'
                )
            ],
            'layout': go.Layout(
                title='Pink Morsel Sales Over Time',
                xaxis={
                    'title': 'Date',
                    'gridcolor': '#ecf0f1',
                    'showgrid': True
                },
                yaxis={
                    'title': 'Sales ($)',
                    'gridcolor': '#ecf0f1',
                    'tickprefix': '$',
                    'showgrid': True
                },
                hovermode='closest',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial, sans-serif'),
                height=500,
                # Add annotation for the price increase
                annotations=[
                    dict(
                        x=cutoff_date,
                        y=df['sales'].max() * 1.05,
                        xref="x",
                        yref="y",
                        text="Price Increase",
                        showarrow=True,
                        arrowhead=2,
                        ax=0,
                        ay=-40,
                        bgcolor="#e74c3c",
                        font=dict(color="white")
                    )
                ]
            )
        }
    ),
    
    # Region selector (optional)
    html.Div([
        html.H3("Filter by Region", style={'marginTop': '30px'}),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': 'All Regions', 'value': 'all'}] + 
                    [{'label': region, 'value': region} for region in sorted(df['region'].unique())],
            value='all',
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'textAlign': 'center', 'marginTop': '20px'}),
    
    # Conclusion box
    html.Div([
        html.H3("Business Insight", style={'color': '#2c3e50'}),
        html.P(
            f"The data shows that sales were {'HIGHER BEFORE' if before_sales > after_sales else 'HIGHER AFTER'} "
            f"the price increase on January 15, 2021.",
            style={'fontSize': '18px', 'lineHeight': '1.6'}
        ),
        html.P(
            f"Total sales decreased by ${abs(before_sales - after_sales):,.2f} "
            f"({abs((before_sales - after_sales)/before_sales*100):.1f}%) "
            f"{'after' if before_sales > after_sales else 'before'} the price change.",
            style={'fontSize': '16px', 'color': '#7f8c8d'}
        )
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '5px',
        'marginTop': '30px',
        'marginBottom': '30px'
    }),
    
    # Footer
    html.Footer(
        "Quantium Data Analysis - Soul Foods Pink Morsel Sales",
        style={'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '30px', 'padding': '20px'}
    )
], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})

# Callback for region filter (optional enhancement)
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Recalculate for filtered data
    before_filtered = filtered_df[filtered_df['date'] < cutoff_date]['sales'].sum()
    after_filtered = filtered_df[filtered_df['date'] >= cutoff_date]['sales'].sum()
    
    fig = go.Figure()
    
    # Add sales line
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['sales'],
        mode='lines+markers',
        name=f'Sales ({selected_region if selected_region != "all" else "All Regions"})',
        line=dict(color='#3498db', width=2),
        marker=dict(size=4),
        hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>'
    ))
    
    # Add vertical line for price increase
    fig.add_trace(go.Scatter(
        x=[cutoff_date, cutoff_date],
        y=[0, filtered_df['sales'].max() * 1.1],
        mode='lines',
        name='Price Increase (Jan 15, 2021)',
        line=dict(color='#e74c3c', width=2, dash='dash'),
        hoverinfo='none'
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Pink Morsel Sales - {selected_region if selected_region != "all" else "All Regions"}',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        yaxis_tickprefix='$',
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        annotations=[
            dict(
                x=cutoff_date,
                y=filtered_df['sales'].max() * 1.05,
                xref="x",
                yref="y",
                text="Price Increase",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                bgcolor="#e74c3c",
                font=dict(color="white")
            )
        ]
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    print("\nStarting Dash app...")
    print("Open your browser and go to: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    print("="*60)
    app.run_server(debug=True)