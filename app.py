import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# This is the main server that runs the web app - it is set up as a DASH server but uses FLASK under the hood

# A small piece of JavaScript essential for the server to run
external_scripts = ["https://code.jquery.com/jquery-1.12.4.min.js"]

# sets the theme, loads the js file and sets the metatags for mobile responsiveness
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.MINTY],
                suppress_callback_exceptions=True)
# Ensures that the graph components match the theme
load_figure_template('minty')

# Creates the server that is run by the index file
server = app.server
