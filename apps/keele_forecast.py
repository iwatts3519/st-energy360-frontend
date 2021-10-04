from azure.storage.blob import BlobClient
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import pandas as pd
import dash_table
import json


def fetch_new_data():
    with open('config.json') as f:
        credentials_json = json.load(f)

    blob1 = BlobClient.from_connection_string(conn_str=credentials_json["CONNECTIONSTRING"],
                                              container_name=credentials_json["CONTAINERNAME"],
                                              blob_name=credentials_json["BLOBNAME"])
    with open(credentials_json["LOCALFILENAME"], 'wb') as my_blob1:
        blob_data = blob1.download_blob()
        blob_data.readinto(my_blob1)

    blob2 = BlobClient.from_connection_string(conn_str=credentials_json["CONNECTIONSTRING"],
                                              container_name=credentials_json["CONTAINERNAME"],
                                              blob_name=credentials_json["BLOBNAMEACC"])
    with open(credentials_json["LOCALFILENAMEACC"], 'wb') as my_blob2:
        blob_data = blob2.download_blob()
        blob_data.readinto(my_blob2)

    keele_df = pd.read_csv('./Data/new_predictions.csv')
    acc_df = pd.read_csv('./Data/accuracy_frame.csv')
    keele_df = keele_df.round({'PV_obs': 2})
    return keele_df, acc_df


keele_df, acc_df = fetch_new_data()

layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col([
                html.Br()

            ])
        ]),
    dbc.Row(
        [
            dbc.Col([
                html.H1('Keele Home Farm Solar Production 7 day Forecast')
            ])
        ], className='justify-center'),

    dbc.Row(
        [

            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='Figure_Keele'),
                ]),
            ], width={'size': 6, 'offset': 3},
                className='align-self-start'),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Forecast', className='card-title'),
                        html.P('Please use the slider below to set your prediction horizon in hours.'),
                        html.P('Hover over the graph for more details or select an area of the graph to zoom in.')

                    ])
                ]),
            ], width={'size': 2, 'offset': .5},
                className='align-self-start')
        ]),

    dbc.Row(
        [
            dbc.Col([
                html.Br()

            ])
        ]),
    dbc.Row([
        dbc.Col(
            dcc.RangeSlider(
                id='forecast-slider',
                min=0,
                max=168,
                step=1,
                value=[0, 24],
                marks={
                    0: '0H',
                    24: '24H',
                    48: '48H',
                    72: '72H',
                    96: '96H',
                    120: '120H',
                    144: '144H',
                    168: '168H'
                }),
            width={'size': 10, 'offset': 1}
        )

    ]),
    dbc.Row([
        html.Br()
    ]),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in keele_df.columns],
                data=keele_df.to_dict('records'),
                page_size=10,
            )
        ], width={'size': 2, 'offset': 1}
        ),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='Figure_Keele_2'),
            ]),
        ], width={'size': 5, 'offset': 1},
            className='align-self-start'),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Accuracy Indicator', className='card-title'),
                    html.P(
                        'This graph shows us an indication of the previous 7 days accuracy by comparing predictions '
                        'with actual historic results.'),
                    html.P('Hover over the graph for more details or select an area of the graph to zoom in.')
                ])
            ]),
        ], width={'size': 2, 'offset': .5},
            className='align-self-start')

    ]),
    dbc.Row([
        html.Br(),
        html.Br(),
        html.Br()
    ]),

], fluid=True)


# -------------------------------------------------------------------------------------
@app.callback(Output(component_id="Figure_Keele", component_property="figure"),
              Output(component_id="Figure_Keele_2", component_property="figure"),
              Input('forecast-slider', 'value')
              )
def update_graph(fs_value):
    keele_df, acc_df = fetch_new_data()
    acc_df = acc_df.tail(48)
    dff = keele_df[fs_value[0]:fs_value[1]]
    dff2 = acc_df
    fig = px.line(dff, x='timestamp',
                  y='PV_obs',
                  labels={'timestamp': 'Timestamp', 'PV_obs': 'Prediction (KWH)'},
                  title="Production Forecast",
                  color_discrete_sequence=['purple'])  # plotting production prediction

    fig.update_layout(height=350, showlegend=False)
    fig2 = px.line(dff2, x='timestamp',
                   y=['Actual', 'Prediction'],
                   labels={'timestamp': 'Timestamp', 'value': 'Prediction (KWH)'},
                   title="Previous 2 days Actual vs Prediction",
                   color_discrete_sequence=['red', 'orange'])  # plotting production prediction

    fig2.update_layout(height=350)

    return fig, fig2
