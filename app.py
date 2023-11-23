from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
from datetime import date

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read in my data
df = pd.read_csv('CrashData.csv', index_col=0)
formatting = '%m/%d/%Y %H:%M'
df['IncidentDateTime'] = pd.to_datetime(df['IncidentDateTime'], format=formatting)
df['IncidentDateTime'] = df['IncidentDateTime'].apply(lambda x: x.strftime("%m/%d/%Y %I:%M%p"))
#Create our time options
HOURS = [f"{i:02d}" for i in range(1, 13)]
MINUTES = [f"{i:02d}" for i in range(0, 60)]
AMPM = ['AM', 'PM']

# App layout
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '17rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa'
}

sidebar = html.Div(
    children=[
        html.H2("Filters"),
        html.Hr(),
        dbc.Row(
            html.H5("Time (HH:MM AM/PM)")
        ),
        #Start time input
        dbc.Row(
          html.Label('Start')  
        ),
        dbc.Row(
            html.Div(
                children=[
                    html.Div(
                        dcc.Dropdown(
                            id='start_time_hour',
                            options=HOURS,
                            value=None,
                            placeholder='HH',
                            clearable=True,
                        ),
                        style=dict(width='30%')
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='start_time_minute',
                            options=MINUTES,
                            value=None,
                            placeholder='MM',
                            clearable=True,
                        ),
                        style=dict(width='30%')
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='start_time_ampm',
                            options=AMPM,
                            value=None,
                            placeholder='AM/PM',
                            clearable=True,
                        ),
                        style=dict(width='40%')
                    )
                ],
                style=dict(display='flex')
            ), 
        ),
        #End time input
        dbc.Row(
          html.Label('End')  
        ),
        dbc.Row(
            html.Div(
                children=[
                    html.Div(
                        dcc.Dropdown(
                            id='end_time_hour',
                            options=HOURS,
                            value=None,
                            placeholder='HH',
                            clearable=True,
                        ),
                        style=dict(width='30%')
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='end_time_minute',
                            options=MINUTES,
                            value=None,
                            placeholder='MM',
                            clearable=True,
                        ),
                        style=dict(width='30%')
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='end_time_ampm',
                            options=AMPM,
                            value=None,
                            placeholder='AM/PM',
                            clearable=True,
                        ),
                        style=dict(width='40%')
                    )
                ],
                style=dict(display='flex')
            ), 
        ),
        html.Br(),
        #Input date range
        dbc.Row(
            html.H5("Date")
        ),
        dbc.Row(
            html.Div(
                dcc.DatePickerRange(
                    id='date_picker_range',
                    min_date_allowed=date(2019, 1, 1),
                    max_date_allowed=date(2022, 1, 30),
                    month_format='M-D-Y',
                    clearable=True
                )
            )
        ),
        dbc.Row(
            html.Div(
                id='filter_output'
            )
        )
    ],
    style=SIDEBAR_STYLE
)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

table = html.Div(
    children=[
        dash_table.DataTable(
            id='table_data',
            data=df.to_dict('records'),
            #columns=[{"name": i, "id": i} for i in df.columns]
        )
    ],
    style=CONTENT_STYLE
)


app.layout = html.Div(
    children=[
        sidebar,
        table
    ]
)

@app.callback(
    Output('filter_output', 'children'),
    Input('start_time_hour', 'value'),
    Input('start_time_minute', 'value'),
    Input('start_time_ampm', 'value'),
    Input('end_time_hour', 'value'),
    Input('end_time_minute', 'value'),
    Input('end_time_ampm', 'value'),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date')
)
def update_data(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
    
    # Handles time input
    # If there is a value in all time fields
    if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm):
        start_time_input = f"{start_hr}:{start_min}{start_ampm}"
        end_time_input = f"{end_hr}:{end_min}{end_ampm}"
    if (start_date is not None) and (end_date is not None):
        pass
    return "TESTING"
        
    
        

if __name__ == '__main__':
    app.run(debug=True)