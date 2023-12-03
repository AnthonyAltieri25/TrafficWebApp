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
        ),
        html.Br(),
        #Apply filter and reset buttons
        dbc.Row(
            html.Div(
                children=[
                    html.Div(
                        html.Button(
                            children='Apply Filter',
                            id='apply_filter_button',
                            disabled = True,
                            style={
                                'background-color': '#5dbea3',
                                'color': '#FFFFFF',
                                'border': 'none',
                                'border-radius': 8,
                                'width': '100%',
                                'height': '3rem',
                            }
                        ),
                        style = {
                            'width': '50%'
                        }
                    ),
                    html.Div(
                        html.Button(
                            children='Reset',
                            id='reset_vals_button',
                            style={
                                'background-color': '#f44336',
                                'color': '#FFFFFF',
                                'border': 'none',
                                'border-radius': 8,
                                'width': '100%',
                                'height': '3rem'
                            }
                        ),
                        style={
                            'width': '50%'
                        }
                    )
                ],
                style={
                    'display': 'flex'
                }
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

#Function for handling enabling filter button based on filter inputs
@app.callback(
    Output('apply_filter_button', 'disabled'),
    Input('start_time_hour', 'value'),
    Input('start_time_minute', 'value'),
    Input('start_time_ampm', 'value'),
    Input('end_time_hour', 'value'),
    Input('end_time_minute', 'value'),
    Input('end_time_ampm', 'value'),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date')
)
def enable_filter_button(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
    disable_filter = True
    #If all fields are completely filled out
    if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
        disable_filter = False
    #If the time field is completely filled and date field is empty
    elif None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm) and all(i == None for i in (start_date, end_date)):
        disable_filter = False
    #If the date field is full but the time field is emtpy
    elif None not in (start_date, end_date) and all(i == None for i in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm)):
        disable_filter = False
    return disable_filter

#Function for updating button style based on if button is enabled
@app.callback(
    Output('apply_filter_button', 'style'),
    Input('apply_filter_button', 'disabled')
)
def update_filter_button(disabled):
    style={
        'background-color': '#5dbea3',
        'color': '#FFFFFF',
        'border': 'none',
        'border-radius': 8,
        'width': '100%',
        'height': '3rem',
    }
    if disabled:
        style['opacity'] = .6
    else:
        style['opacity'] = 1
    return style

#Function attatched to apply filter button to filter the dataframe


if __name__ == '__main__':
    app.run(debug=True)