# pages/guest_behaviors.py
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from components.plots import lead_time_distribution, stay_duration_patterns, booking_patterns_market_segment

# Define the layout for the Guest Behaviors page
layout = dbc.Container([
    html.H2("Guest Behaviors", className="mt-4 mb-4 text-center"),
    
    # Hotel Type Filter
    dbc.Row([
        dbc.Col([
            html.Label("Select Hotel Type:"),
            dcc.Dropdown(
                id="hotel-type-dropdown-gb",
                options=[
                    {"label": "All", "value": "All"},
                    {"label": "Resort Hotel", "value": "Resort Hotel"},
                    {"label": "City Hotel", "value": "City Hotel"},
                ],
                value="All",
                clearable=False,
                style={"width": "100%"}
            ),
        ], width=4, className="mb-4"),
    ], justify="center"),

    # Section 1: Lead Time Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("1. When Do Guests Book? (Lead Time Distribution)"),
                dbc.CardBody([
                    html.Label("Select Lead Time Range:"),
                    dcc.RangeSlider(
                        id="lead-time-slider",
                        min=0,
                        max=737,
                        step=10,
                        value=[0, 737],
                        marks={0: "0", 200: "200", 400: "400", 600: "600", 737: "737"},
                        className="mb-3"
                    ),
                    dcc.Graph(id="lead-time-plot"),
                    html.H5("Insight:"),
                    html.P("Most bookings occur with lead times under 100 days, with a sharp peak at 0-10 days (likely last-minute bookings). Resort Hotels have a lower median lead time (~47 days) and a longer tail, compared to City Hotels (median ~50 days)."),
                    html.H5("Recommendation:"),
                    html.P("Resort Hotels should offer early-bird discounts for bookings made 3+ months in advance, while City Hotels can focus on last-minute marketing (e.g., flash sales).")
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    # Section 2: Stay Duration Patterns
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("2. How Long Do They Stay? (Stay Duration Patterns)"),
                dbc.CardBody([
                    dcc.Graph(id="stay-duration-plot"),
                    html.H5("Insight:"),
                    html.P("Resort Hotels have longer average stays, peaking in summer (e.g., August ~5.5 nights), while City Hotels show shorter, more stable stays (~2.5 to 3.5 nights) year-round."),
                    html.H5("Recommendation:"),
                    html.P("Resort Hotels can offer extended-stay packages in summer, while City Hotels should optimize room turnover with competitive pricing for shorter stays.")
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    # Section 3: Booking Patterns by Market Segment
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("3. Who Are the Guests? (Booking Patterns by Market Segment)"),
                dbc.CardBody([
                    dcc.Graph(id="market-segment-plot"),
                    html.H5("Insight:"),
                    html.P("City Hotels rely heavily on the Online TA segment (~60-70%), while Resort Hotels have a more balanced distribution, with significant bookings from Groups (~15-20%) and Offline TA/TO (~20-25%)."),
                    html.H5("Recommendation:"),
                    html.P("City Hotels should optimize online booking platforms, while Resort Hotels can target group travelers with tailored packages.")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
], fluid=True)

# Callback for Lead Time Distribution Plot
@callback(
    Output("lead-time-plot", "figure"),
    [Input("hotel-type-dropdown-gb", "value"),
     Input("lead-time-slider", "value")]
)
def update_lead_time_plot(hotel_type, lead_time_range):
    return lead_time_distribution(hotel_type, lead_time_range)

# Callback for Stay Duration Patterns Plot
@callback(
    Output("stay-duration-plot", "figure"),
    [Input("hotel-type-dropdown-gb", "value")]
)
def update_stay_duration_plot(hotel_type):
    return stay_duration_patterns(hotel_type)

# Callback for Market Segment Plot
@callback(
    Output("market-segment-plot", "figure"),
    [Input("hotel-type-dropdown-gb", "value")]
)
def update_market_segment_plot(hotel_type):
    return booking_patterns_market_segment(hotel_type)
