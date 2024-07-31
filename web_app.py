from dash import Dash, html, dash_table, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dashboard_data_parser import *

from dash_bootstrap_templates import load_figure_template

load_figure_template(["cyborg"])

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)


creds_audits_log_df = parse_creds_audits_log('/home/grant/projects/ssh-honeypot/test_log_files/creds_audits.log')
cmd_audits_log_df = parse_cmd_audits_log('/home/grant/projects/ssh-honeypot/test_log_files/cmd_audits.log')


top_ip_address = top_10_calculator(creds_audits_log_df, "ip_address")
top_usernames = top_10_calculator(creds_audits_log_df, "username")
top_passwords = top_10_calculator(creds_audits_log_df, "password")

top_cmds = top_10_calculator(cmd_audits_log_df, "Command")

get_ip_to_country = ip_to_country_code(creds_audits_log_df)
top_country = top_10_calculator(get_ip_to_country, "Country_Code")

image = 'assets/images/honeypy-logo-white.png'

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc_css])
app.title = "HONEYPY"
#app._favicon = "../static/images/Logo.png"

tables = html.Div([
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "IP Address", 'id': 'ip_address'}],
                    style_table={'width': '100%', 'color': 'black'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "Usernames", 'id': 'username'}],
                    style_table={'width': '100%'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),
        
            dbc.Col(
                dash_table.DataTable(
                    data=creds_audits_log_df.to_dict('records'),
                    columns=[{"name": "Passwords", 'id': 'password'}],
                    style_table={'width': '100%','justifyContent': 'center'},
                    style_cell={'textAlign': 'left', 'color': '#2a9fd6'},
                    style_header={'fontWeight': 'bold'},
                    page_size=10
                ),
            ),       
        ])
])

apply_table_theme = html.Div(
    [tables],
    className="dbc"
)

app.layout = dbc.Container([
    # Honeypot Title.
    html.Div([html.Img(src=image, style={'height': '25%', 'width': '25%'})], style={'textAlign': 'center'}, className='dbc'),
    # Row 1 - 3 Top 10 Dashboards.
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(top_ip_address, x="ip_address", y='count')), width=4),
        dbc.Col(dcc.Graph(figure=px.bar(top_usernames, x='username', y='count')), width=4),
        dbc.Col(dcc.Graph(figure=px.bar(top_passwords, x='password', y='count')), ),
    ], align='center', class_name='mb-4'),

    # Row 2: Top 10 Commands + Country Codes.
    dbc.Row([
        dbc.Col(dcc.Graph(figure=px.bar(top_cmds, x='Command', y='count')), style={'width': '33%', 'display': 'inline-block'}),
        dbc.Col(dcc.Graph(figure=px.bar(top_country, x="Country_Code", y='count')), style={'width': '33%', 'display': 'inline-block'}),
        # Add another graph or placeholder if needed to make the rows even
       
    ], align='center', class_name='mb-4'),

    # Table Titles.
    html.Div([
        html.H3(
            "Intelligence Data", 
            style={'textAlign': 'center', "font-family": 'Consolas, sans-serif', 'font-weight': 'bold'}, 
        ),
        ]),
    #html.Div(children="Intelligence Data", style={'textAlign': 'center', "fontsize": "750", "font-family": 'sans-serif', 'font-weight': 'bold'}, className="dbc"),
    # Row 3: Tables with data.
    apply_table_theme

    

])


if __name__ == '__main__':
    app.run(debug=True)

