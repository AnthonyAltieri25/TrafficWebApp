from dash import Dash, html, dcc, dash_table, Input, Output, State,  callback_context, callback
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create our time options
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

# Where our dataframe is going to be stored
# Note dataframe must be stored as dictionary
store = dcc.Store(
    id='df_store',
    data=pd.read_csv('CrashData.csv', index_col=0).to_dict('records')
)

sidebar = html.Div(
    children=[
        html.H2("Filters"),
        html.Hr(),
        dbc.Row(
            html.H5("Time (HH:MM AM/PM)")
        ),
        # Start time input
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
        # End time input
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
        # Input date range
        dbc.Row(
            html.H5("Date")
        ),
        dbc.Row(
            html.Div(
                dcc.DatePickerRange(
                    id='date_picker_range',
                    min_date_allowed=dt.date(2019, 1, 1),
                    max_date_allowed=dt.date(2022, 1, 30),
                    month_format='M-D-Y',
                    clearable=True
                )
            )
        ),
        dbc.Row(
            html.Div(
                children='TESTING',
                id='filter_output'
            )
        ),
        html.Br(),
        # Apply filter and reset buttons
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
            data=None,
        )
    ],
    style=CONTENT_STYLE
)


app.layout = html.Div(
    children=[
        sidebar,
        table,
        store
    ]
)

# Function for handling enabling filter button based on filter inputs
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
    # If all fields are completely filled out
    if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
        disable_filter = False
    # If the time field is completely filled and date field is empty
    elif None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm) and all(i == None for i in (start_date, end_date)):
        disable_filter = False
    # If the date field is full but the time field is emtpy
    elif None not in (start_date, end_date) and all(i == None for i in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm)):
        disable_filter = False
    return disable_filter

# Function for updating button style based on if button is enabled
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

# Function attatched to apply filter button to filter the dataframe
@app.callback(
    Output('df_store', 'data'),
    Input('apply_filter_button', 'n_clicks'),
    State('start_time_hour', 'value'),
    State('start_time_minute', 'value'),
    State('start_time_ampm', 'value'),
    State('end_time_hour', 'value'),
    State('end_time_minute', 'value'),
    State('end_time_ampm', 'value'),
    State('date_picker_range', 'start_date'),
    State('date_picker_range', 'end_date'),
    prevent_initial_call = True
)
def filter_data(m_clicks, start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
    df = pd.read_csv('CrashData.csv', index_col=0)
    formatting = '%m/%d/%Y %H:%M'
    df['IncidentDateTime'] = pd.to_datetime(df['IncidentDateTime'], format=formatting)
    # Filter by time
    if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm):
        # Get start/end times and convert them to datetime objects
        formatting = '%I:%M%p'
        start_time = dt.datetime.strptime(f'{start_hr}:{start_min}{start_ampm}', formatting)
        end_time = dt.datetime.strptime(f'{end_hr}:{end_min}{end_ampm}', formatting)
        # Filter the databased on the times
        df = df[(df['IncidentDateTime'].dt.time >= start_time.time()) & (df['IncidentDateTime'].dt.time <= end_time.time())]
    
    return df.to_dict('records')

# Updates the displayed table when the stored dataframe is changed
@app.callback(
    Output('table_data', 'data'),
    Input('df_store', 'data'),
)
def update_table(data):
    df = pd.DataFrame.from_dict(data)
    formatting = ''
    ctx = callback_context
    #True if this is on initial call
    if not ctx.triggered_id:
        formatting = '%m/%d/%Y %H:%M'
    else:
        formatting = 'ISO8601'
    df['IncidentDateTime'] = pd.to_datetime(df['IncidentDateTime'], format=formatting)
    df['IncidentDateTime'] = df['IncidentDateTime'].apply(lambda x: x.strftime("%m/%d/%Y %I:%M%p"))
    return df.to_dict('records')



if __name__ == '__main__':
    app.run(debug=True)