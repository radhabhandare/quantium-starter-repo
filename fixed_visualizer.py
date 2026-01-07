import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('pink_morsels_sales.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Price increase date
cutoff_date = pd.Timestamp('2021-01-15')

# Calculate overall stats
before_sales = df[df['date'] < cutoff_date]['sales'].sum()
after_sales = df[df['date'] >= cutoff_date]['sales'].sum()
total_sales = df['sales'].sum()

# Initialize Dash app
app = dash.Dash(__name__)

# App layout with enhanced styling
app.layout = html.Div([
    # Header Section with gradient background
    html.Div([
        html.H1("🍬 Pink Morsel Sales Dashboard", 
                style={
                    'color': 'white',
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '2.5rem',
                    'marginBottom': '10px'
                }),
        html.P("Analyzing the impact of price increase on January 15, 2021",
               style={
                   'color': 'rgba(255, 255, 255, 0.9)',
                   'textAlign': 'center',
                   'fontFamily': 'Arial, sans-serif',
                   'fontSize': '1.1rem',
                   'marginBottom': '30px'
               })
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '40px 20px',
        'borderRadius': '10px',
        'marginBottom': '30px'
    }),
    
    # Stats Cards Row
    html.Div([
        html.Div([
            html.Div([
                html.H3("📊", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4(f"${total_sales:,.0f}", 
                       style={'color': '#4a5568', 'marginBottom': '5px', 'fontSize': '1.8rem'}),
                html.P("Total Sales", style={'color': '#718096', 'fontSize': '0.9rem'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'transition': 'transform 0.3s'
            })
        ], style={'width': '24%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H3("⬆️", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4(f"${before_sales:,.0f}", 
                       style={'color': '#38a169', 'marginBottom': '5px', 'fontSize': '1.8rem'}),
                html.P("Before Price Increase", style={'color': '#718096', 'fontSize': '0.9rem'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'transition': 'transform 0.3s'
            })
        ], style={'width': '24%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H3("⬇️", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4(f"${after_sales:,.0f}", 
                       style={'color': '#e53e3e', 'marginBottom': '5px', 'fontSize': '1.8rem'}),
                html.P("After Price Increase", style={'color': '#718096', 'fontSize': '0.9rem'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'transition': 'transform 0.3s'
            })
        ], style={'width': '24%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Div([
                html.H3("📈", style={'fontSize': '2rem', 'marginBottom': '10px'}),
                html.H4(f"{'Decrease' if before_sales > after_sales else 'Increase'}", 
                       style={'color': '#d69e2e', 'marginBottom': '5px', 'fontSize': '1.8rem'}),
                html.P("Overall Impact", style={'color': '#718096', 'fontSize': '0.9rem'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'textAlign': 'center',
                'transition': 'transform 0.3s'
            })
        ], style={'width': '24%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'marginBottom': '40px'}),
    
    # Region Filter Section
    html.Div([
        html.H2("Filter by Region", 
                style={
                    'color': '#2d3748',
                    'fontFamily': 'Arial, sans-serif',
                    'marginBottom': '20px',
                    'borderBottom': '2px solid #e2e8f0',
                    'paddingBottom': '10px'
                }),
        
        # Radio Buttons for Region Selection
        html.Div([
            dcc.RadioItems(
                id='region-radio',
                options=[
                    {'label': html.Span(['🌍 All Regions'], 
                                       style={'fontWeight': 'bold', 'paddingLeft': '10px'}),
                     'value': 'all'},
                    {'label': html.Span(['⬆️ North'], 
                                       style={'color': '#4299e1', 'paddingLeft': '10px'}),
                     'value': 'north'},
                    {'label': html.Span(['➡️ East'], 
                                       style={'color': '#48bb78', 'paddingLeft': '10px'}),
                     'value': 'east'},
                    {'label': html.Span(['⬇️ South'], 
                                       style={'color': '#ed8936', 'paddingLeft': '10px'}),
                     'value': 'south'},
                    {'label': html.Span(['⬅️ West'], 
                                       style={'color': '#9f7aea', 'paddingLeft': '10px'}),
                     'value': 'west'}
                ],
                value='all',
                labelStyle={
                    'display': 'inline-block',
                    'marginRight': '20px',
                    'padding': '12px 20px',
                    'backgroundColor': '#f7fafc',
                    'borderRadius': '8px',
                    'border': '2px solid #e2e8f0',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s'
                },
                inputStyle={'marginRight': '8px'},
                style={'marginBottom': '30px'}
            )
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
        
        # Chart Container
        html.Div([
            dcc.Graph(id='sales-chart')
        ], style={
            'backgroundColor': 'white',
            'padding': '25px',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
        })
    ], style={
        'backgroundColor': '#f8fafc',
        'padding': '30px',
        'borderRadius': '10px',
        'marginBottom': '40px'
    }),
    
    # Insights Panel
    html.Div([
        html.H2("📊 Business Insights", 
                style={
                    'color': '#2d3748',
                    'fontFamily': 'Arial, sans-serif',
                    'marginBottom': '20px'
                }),
        
        html.Div([
            html.Div([
                html.H4("💰 Price Increase Impact", 
                       style={'color': '#4a5568', 'marginBottom': '15px'}),
                html.P([
                    "The price increase on ",
                    html.Strong("January 15, 2021"),
                    " resulted in a ",
                    html.Strong(f"{'decrease' if before_sales > after_sales else 'increase'} of ${abs(before_sales - after_sales):,.0f}"),
                    f" ({abs((before_sales - after_sales)/before_sales*100):.1f}%) in sales."
                ], style={'lineHeight': '1.6', 'color': '#4a5568'}),
                
                html.Hr(style={'borderColor': '#e2e8f0', 'margin': '20px 0'}),
                
                html.H4("🎯 Recommendation", 
                       style={'color': '#4a5568', 'marginBottom': '15px'}),
                html.P([
                    "Based on the data, we recommend ",
                    html.Strong("reviewing the pricing strategy"),
                    " for Pink Morsels. ",
                    "Consider regional performance variations shown in the filter above."
                ], style={'lineHeight': '1.6', 'color': '#4a5568'})
            ], style={'padding': '20px'})
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'borderLeft': '5px solid #4299e1'
        })
    ], style={'marginBottom': '40px'}),
    
    # Footer
    html.Footer([
        html.P("Soul Foods • Quantitative Analysis Dashboard • Powered by Quantium",
               style={
                   'textAlign': 'center',
                   'color': '#a0aec0',
                   'padding': '20px',
                   'borderTop': '1px solid #e2e8f0',
                   'marginTop': '30px',
                   'fontSize': '0.9rem'
               })
    ])
], style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f1f5f9',
    'minHeight': '100vh',
    'padding': '20px',
    'maxWidth': '1200px',
    'margin': '0 auto'
})

# Callback for updating chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    # Filter data based on selection
    if selected_region == 'all':
        filtered_df = df
        region_label = "All Regions"
        line_color = '#4c51bf'
    else:
        filtered_df = df[df['region'] == selected_region]
        region_label = selected_region.capitalize()
        
        # Different colors for each region
        region_colors = {
            'north': '#4299e1',  # Blue
            'east': '#48bb78',   # Green
            'south': '#ed8936',  # Orange
            'west': '#9f7aea'    # Purple
        }
        line_color = region_colors.get(selected_region, '#4c51bf')
    
    # Calculate stats for filtered data
    before_filtered = filtered_df[filtered_df['date'] < cutoff_date]['sales'].sum()
    after_filtered = filtered_df[filtered_df['date'] >= cutoff_date]['sales'].sum()
    
    # Create figure
    fig = go.Figure()
    
    # Add sales line
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['sales'],
        mode='lines+markers',
        name=f'{region_label} Sales',
        line=dict(color=line_color, width=3),
        marker=dict(size=6, color=line_color),
        hovertemplate='<b>Date</b>: %{x|%b %d, %Y}<br><b>Sales</b>: $%{y:,.2f}<br><b>Region</b>: ' + region_label + '<extra></extra>'
    ))
    
    # Add vertical line for price increase
    fig.add_vline(
        x=cutoff_date,
        line_dash="dash",
        line_color="#e53e3e",
        line_width=2,
        annotation_text="Price Increase<br>Jan 15, 2021",
        annotation_position="top right",
        annotation_font_size=12,
        annotation_font_color="#e53e3e"
    )
    
    # Add shaded areas for before/after
    if len(filtered_df) > 0:
        min_date = filtered_df['date'].min()
        max_date = filtered_df['date'].max()
        max_sales = filtered_df['sales'].max() * 1.1
        
        # Shade before period (green)
        fig.add_vrect(
            x0=min_date,
            x1=cutoff_date,
            fillcolor="rgba(72, 187, 120, 0.1)",
            layer="below",
            line_width=0,
            annotation_text="Before Price Increase",
            annotation_position="top left",
            annotation_font_size=10
        )
        
        # Shade after period (red)
        fig.add_vrect(
            x0=cutoff_date,
            x1=max_date,
            fillcolor="rgba(229, 62, 62, 0.1)",
            layer="below",
            line_width=0,
            annotation_text="After Price Increase",
            annotation_position="top right",
            annotation_font_size=10
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'Pink Morsel Sales - {region_label}',
            'font': {'size': 24, 'color': '#2d3748'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12),
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )
    
    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
    
    return fig

# Run the app - FIXED LINE
if __name__ == '__main__':
    print("="*60)
    print("🎨 ENHANCED PINK MORSEL SALES DASHBOARD")
    print("="*60)
    print("Features:")
    print("• Interactive region filtering with radio buttons")
    print("• Modern, visually appealing design")
    print("• Color-coded regions")
    print("• Shaded before/after periods")
    print("• Responsive layout with cards")
    print("="*60)
    print("\nStarting server...")
    print("Open your browser and go to: http://127.0.0.1:8050")
    print("="*60)
    # FIX: Changed from app.run_server() to app.run()
    app.run(debug=True)