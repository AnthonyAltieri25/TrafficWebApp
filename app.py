from dash import Dash, html, dcc, dash_table, Input, Output, State,  callback_context, no_update, ctx
import dash_bootstrap_components as dbc
# For data
import pandas as pd
import datetime as dt
# For graphing
from MapBoxToken import TOKEN
import plotly.express as px
import plotly.graph_objects as go

# Variables
FILE = 'wejo\TotalDataAug19Optimzed.parquet'
COLUMNS =  ['time', 'speed', 'latitude', 'longitude']
temp_df = pd.DataFrame(columns=COLUMNS)

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
    data=None
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
            html.H6(
                children='TESTING',
                id='test_output'
            )
        ),
        html.Br(),

        # BUTTONS

        dbc.Row(
            html.Div(
                children=[
                    # Generate Data button
                    html.Div(
                        html.Button(
                            children='Generate Data',
                            id='generate_data_button',
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
                    # Reset Button
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
        ),
        # Filter current selection button
        dbc.Row(
            html.Div(
                html.Button(
                    children='Filter Current Selection',
                    id='filter_current_button',
                    style={
                        'background-color': '#24a0ed',
                        'color': '#FFFFFF',
                        'border': 'none',
                        'border-radius': 8,
                        'width': '100%',
                        'height': '3rem'
                    }
                )
            )
        )
    ],
    style=SIDEBAR_STYLE
)

CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
}

# Main panel ui layout
main_panel = html.Div(
    children=dcc.Tabs(
        id="tabs",
        value='tab_value',
        children=[
            dcc.Tab(
                label='Data Table',
                children=[
                    dash_table.DataTable(
                        id='table_data',
                        columns=[{'name': col, 'id': col} for col in temp_df.columns],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_cell={'textAlign': 'left'},
                    )
                ]
            ),
            dcc.Tab(
                label='Map',
                children=[
                    dcc.Graph(
                        id='interactive_graph',
                        style={'height': '86vh', 'width': '100%'}
                    ),
                    html.Pre(
                        
                    )
                ]
            )
        ]
    ),  
    style=CONTENT_STYLE
)

# Put all the UI components together
app.layout = html.Div(
    children=[
        sidebar,
        main_panel,
        store
    ]
)

# Function for handling enabling filter button based on filter inputs
@app.callback(
    Output('generate_data_button', 'disabled'),
    Input('start_time_hour', 'value'),
    Input('start_time_minute', 'value'),
    Input('start_time_ampm', 'value'),
    Input('end_time_hour', 'value'),
    Input('end_time_minute', 'value'),
    Input('end_time_ampm', 'value'),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date'),
    Input('interactive_graph', 'selectedData')
)
def enable_generate_data_button(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date, selected_data):
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
    # If there is data box selected
    elif selected_data is not None and 'range' in selected_data:
        disable_filter = False
    return disable_filter

# Function for updating button style based on if button is enabled
@app.callback(
    Output('generate_data_button', 'style'),
    Input('generate_data_button', 'disabled')
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

# Function for handling enabling filter current button based on filter inputs and df_store
@app.callback(
    Output('filter_current_button', 'disabled'),
    Input('start_time_hour', 'value'),
    Input('start_time_minute', 'value'),
    Input('start_time_ampm', 'value'),
    Input('end_time_hour', 'value'),
    Input('end_time_minute', 'value'),
    Input('end_time_ampm', 'value'),
    Input('date_picker_range', 'start_date'),
    Input('date_picker_range', 'end_date'),
    Input('interactive_graph', 'selectedData'),
    Input('df_store', 'data')
)
def enable_generate_data_button(start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date, selected_data, data):
    disable_filter = True
    # If data has been generated
    if data != None:
        # If all fields are completely filled out
        if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
            disable_filter = False
        # If the time field is completely filled and date field is empty
        elif None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm) and all(i == None for i in (start_date, end_date)):
            disable_filter = False
        # If the date field is full but the time field is emtpy
        elif None not in (start_date, end_date) and all(i == None for i in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm)):
            disable_filter = False
        # If there is data box selected
        elif selected_data is not None and 'range' in selected_data:
            disable_filter = False
    return disable_filter

# Function for updating filter current button style based on if button is enabled
@app.callback(
    Output('filter_current_button', 'style'),
    Input('filter_current_button', 'disabled')
)
def update_filter_button(disabled):
    style={
        'background-color': '#24a0ed',
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

# Function attatched to generate data and filter current button to filter the dataframe
@app.callback(
    Output('df_store', 'data'),
    Input('generate_data_button', 'n_clicks'),
    Input('reset_vals_button', 'n_clicks'),
    Input('filter_current_button', 'n_clicks'),
    State('df_store', 'data'),
    State('interactive_graph', 'selectedData'),
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
def generate_data(n_clicks_filter, n_clicks_reset, n_clicks_filter_current, stored_data, selected_data, start_hr, start_min, start_ampm, end_hr, end_min, end_ampm, start_date, end_date):
    df = None
    if 'filter_current_button' == ctx.triggered_id:
        df = pd.DataFrame.from_dict(stored_data)
    else:
        df = pd.read_parquet(FILE, engine='pyarrow')
    formatting = 'ISO8601'
    df['time'] = pd.to_datetime(df['time'], format=formatting)
    # If the filter button was pressed
    if 'generate_data_button' or 'filter_current_button' == ctx.triggered_id:
        # Filter by time
        if None not in (start_hr, start_min, start_ampm, end_hr, end_min, end_ampm):
            # Get start/end times and convert them to datetime objects
            formatting = '%I:%M%p'
            start_time = dt.datetime.strptime(f'{start_hr}:{start_min}{start_ampm}', formatting)
            end_time = dt.datetime.strptime(f'{end_hr}:{end_min}{end_ampm}', formatting)
            # Filter the databased on the times
            df = df[(df['time'].dt.time >= start_time.time()) & (df['time'].dt.time <= end_time.time())]
            if df.empty:
                return no_update
        # Filter by region
        if selected_data is not None and 'range' in selected_data:
            top_left, bottom_right = selected_data['range']['mapbox']
            df = df[
                ((df['latitude'] >= bottom_right[1]) &
                (df['latitude'] <= top_left[1]) &
                (df['longitude'] >= top_left[0]) &
                (df['longitude'] <= bottom_right[0]))
            ]
            if df.empty:
                return no_update 
        return df.to_dict('records')
    # If the reset button was pressed
    elif 'reset_vals_button' == ctx.triggered_id:
        return None

# Updates the displayed table when the stored dataframe is changed
@app.callback(
    Output('table_data', 'data'),
    Input('df_store', 'data'),
)
def update_table(data):
    if data is not None:
        df = pd.DataFrame.from_dict(data)
        df['time'] = df['time']
        formatting = ''
        ctx = callback_context
        #True if this is on initial call
        if not ctx.triggered_id:
            formatting = 'ISO8601'
        else:
            formatting = 'ISO8601'
        df['time'] = pd.to_datetime(df['time'], format=formatting)
        df['time'] = df['time'].apply(lambda x: x.strftime("%m/%d/%Y %I:%M%p"))
        return df.to_dict('records')
    else:
        return []
    

@app.callback(
    Output('interactive_graph', 'figure'),
    Input('df_store', 'data')
)
def create_map(data):
    if data is not None:
        df = pd.DataFrame.from_dict(data)

        # Map/data settings
        trace = go.Scattermapbox(
            lat=df['latitude'],
            lon=df['longitude'],
            mode='markers',
            marker=dict(
                color=df['speed'],
                colorscale='Inferno',
                colorbar=dict(title='Speed'),
                opacity=1
            ),
            text= '<b>Speed:</b> ' + df['speed'].astype(str) + 'mph<br><b>Time:</b> ' + df['time'].astype(str),
            hoverinfo='text'
        )
        
        # Calculate the bounding box
        min_lat, max_lat = min(df['latitude']), max(df['latitude'])
        min_lon, max_lon = min(df['longitude']), max(df['longitude'])
        
        # Layout settings
        layout = go.Layout(
            mapbox=dict(
                style="outdoors",
                center=dict(lat=(min_lat + max_lat) / 2, lon=(min_lon + max_lon) / 2),
                zoom=5,
                accesstoken=TOKEN 
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            uirevision=True,
            autosize=True,
        )
    
        fig = go.Figure(data=[trace], layout=layout)
    
        return fig
    else:
        center_lat = 42.9
        center_lon = -75.2
        # Create a map with a singular invisible point so that box selection is enabled
        trace = go.Scattermapbox(
            lat=[center_lat],
            lon=[center_lon],
            mode='markers',
            marker=dict(size=0)
        )
        
        # Create layout for the Mapbox map
        layout = go.Layout(
            mapbox=dict(
                style="outdoors",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=6.1,
                accesstoken=TOKEN
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            uirevision=True,
            autosize=True,
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return fig

if __name__ == '__main__':
    app.run(debug=True)