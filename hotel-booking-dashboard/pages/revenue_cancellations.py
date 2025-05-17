# pages/revenue_cancellations.py
import dash
from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from components.plots import adr_vs_stay_length, cancellations_by_lead_time, cancellation_trends_by_month

# Define the layout for the Revenue & Cancellations page
layout = dbc.Container([
    html.H2("Revenue & Cancellations", className="mt-4 mb-4 text-center"),
    
    # Hotel Type Filter
    dbc.Row([
        dbc.Col([
            html.Label("Select Hotel Type:"),
            dcc.Dropdown(
                id="hotel-type-dropdown-rc",
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

    # Tabs for Revenue and Cancellations
    dbc.Tabs([
        # Tab 1: Revenue Insights
        dbc.Tab(label="Revenue Insights", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("4. What Drives Revenue? (ADR and Stay Length)"),
                        dbc.CardBody([
                            html.Label("Select Stay Length Range:"),
                            dcc.RangeSlider(
                                id="stay-length-slider",
                                min=0,
                                max=50,
                                step=1,
                                value=[0, 50],
                                marks={0: "0", 10: "10", 20: "20", 30: "30", 40: "40", 50: "50"},
                                className="mb-3"
                            ),
                            dcc.Graph(id="adr-stay-plot"),
                            html.H5("Insight:"),
                            html.P("Higher revenue is associated with longer stays and higher ADRs. Resort Hotels benefit from mid-length stays (5-10 nights), while City Hotels rely on volume."),
                            html.H5("Recommendation:"),
                            html.P("Resort Hotels should target premium pricing for mid-length stays, while City Hotels can focus on competitive rates for shorter stays.")
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
        ]),

        # Tab 2: Cancellation Insights
        dbc.Tab(label="Cancellation Insights", children=[
            # Section 5: Cancellations by Lead Time
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("5. Why Do Guests Cancel? (Cancellations by Lead Time and Hotel Type)"),
                        dbc.CardBody([
                            dcc.Graph(id="cancel-lead-time-plot"),
                            html.H5("Insight:"),
                            html.P("Canceled bookings have higher lead times (Resort Hotels: median ~120 days, City Hotels: ~100 days), suggesting uncertainty over longer timeframes."),
                            html.H5("Recommendation:"),
                            html.P("Implement stricter cancellation policies for long lead times, or offer incentives for non-refundable bookings.")
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),

            # Section 6: Cancellation Trends by Month
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("6. When Are Cancellations Most Likely? (Cancellation Trends by Month)"),
                        dbc.CardBody([
                            dcc.Graph(id="cancel-trends-plot"),
                            html.H5("Insight:"),
                            html.P("City Hotels peak in April (~35%) due to corporate clients, while Resort Hotels drop in August (~15%) due to committed summer plans."),
                            html.H5("Recommendation:"),
                            html.P("City Hotels should offer incentives in spring, while Resort Hotels can confidently offer last-minute deals in summer.")
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
        ]),
    ]),

    # Summary of Recommendations
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Summary of Recommendations"),
                dbc.CardBody([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th("Hotel Type"),
                                html.Th("Strategy"),
                                html.Th("Focus Area"),
                            ])
                        ]),
                        html.Tbody([
                            html.Tr([html.Td("Resort Hotel"), html.Td("Early-bird discounts"), html.Td("Long lead-time bookings")]),
                            html.Tr([html.Td("Resort Hotel"), html.Td("Extended-stay packages"), html.Td("Summer months (July, August)")]),
                            html.Tr([html.Td("Resort Hotel"), html.Td("Group packages"), html.Td("Groups market segment")]),
                            html.Tr([html.Td("Resort Hotel"), html.Td("Premium pricing"), html.Td("Mid-length stays (5-10 nights)")]),
                            html.Tr([html.Td("Resort Hotel"), html.Td("Stricter cancellation policies"), html.Td("Long lead times, spring")]),
                            html.Tr([html.Td("Resort Hotel"), html.Td("Last-minute deals"), html.Td("Summer (low cancellation risk)")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Last-minute marketing (flash sales)"), html.Td("Short lead-time bookings")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Optimize room turnover"), html.Td("Short stays year-round")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Optimize online booking platforms"), html.Td("Online TA segment")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Corporate amenities"), html.Td("Corporate segment")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Competitive pricing"), html.Td("Short stays")]),
                            html.Tr([html.Td("City Hotel"), html.Td("Incentives (e.g., loyalty points)"), html.Td("Spring (high cancellation risk)")]),
                        ])
                    ], className="table table-striped")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
], fluid=True)

# Callback for ADR vs. Stay Length Plot
@callback(
    Output("adr-stay-plot", "figure"),
    [Input("hotel-type-dropdown-rc", "value"),
     Input("stay-length-slider", "value")]
)
def update_adr_stay_plot(hotel_type, stay_length_range):
    return adr_vs_stay_length(hotel_type, stay_length_range)

# Callback for Cancellations by Lead Time Plot
@callback(
    Output("cancel-lead-time-plot", "figure"),
    [Input("hotel-type-dropdown-rc", "value")]
)
def update_cancel_lead_time_plot(hotel_type):
    return cancellations_by_lead_time(hotel_type)

# Callback for Cancellation Trends by Month Plot
@callback(
    Output("cancel-trends-plot", "figure"),
    [Input("hotel-type-dropdown-rc", "value")]
)
def update_cancel_trends_plot(hotel_type):
    return cancellation_trends_by_month(hotel_type)