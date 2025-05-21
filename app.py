import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import guest_behaviors, revenue_cancellations

# Initialize the Dash app with a custom Bootstrap theme and external stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'], suppress_callback_exceptions=True)
server = app.server
# Define the navigation bar with custom colors
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Guest Behaviors", href="/guest-behaviors", id="guest-behaviors-link", style={'color': '#FFFFFF'})),
        dbc.NavItem(dbc.NavLink("Revenue & Cancellations", href="/revenue-cancellations", id="revenue-cancellations-link", style={'color': '#FFFFFF'})),
    ],
    brand="Hotel Booking Analysis Dashboard",
    brand_href="/",
    color="#1E90FF",  # Dodger Blue for navbar
    dark=True,
    sticky="top",
)

# Define the app layout with navigation and page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content", style={"padding": "20px", "backgroundColor": "#F8F9FA"})
])

# Callback to handle page routing
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/guest-behaviors":
        return guest_behaviors.layout
    elif pathname == "/revenue-cancellations":
        return revenue_cancellations.layout
    else:
        return guest_behaviors.layout  

# Run the app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=10000, debug=True)