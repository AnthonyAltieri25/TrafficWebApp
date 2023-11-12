#Core imports
from shiny import App, render, ui
#For displaying/importing the map
from shinywidgets import output_widget, register_widget, render_widget
#For styling
import shinyswatch
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

TIMES = (
    "12:00 AM",
    "1:00 AM",
    "2:00 AM",
    "3:00 AM",
    "4:00 AM",
    "5:00 AM",
    "6:00 AM",
    "7:00 AM",
    "8:00 AM",
    "9:00 AM",
    "10:00 AM",
    "11:00 AM",
    "12:00 PM",
    "1:00 PM",
    "2:00 PM",
    "3:00 PM",
    "4:00 PM",
    "5:00 PM",
    "6:00 PM",
    "7:00 PM",
    "8:00 PM",
    "9:00 PM",
    "10:00 PM",
    "11:00 PM"
)

app_ui = ui.page_fillable(
    #Style
    shinyswatch.theme.minty(),
    #Page title
    ui.h2("Interactive Traffic Map"),
    #Title explanation
    #ui.markdown("Insert explanation of what this thing is"),
    ui.layout_sidebar(
        ui.sidebar(
            #Checkbox for enabling filtering by date
            ui.input_checkbox("date_checkbox", "Filter by date", False),
            #Date filter selection
            ui.panel_conditional(
                "input.date_checkbox",
                ui.input_date_range("date_range", "Date range"),
            ),
            #Checkbox for enabling filtering by time
            ui.input_checkbox("time_checkbox", "Filter by time", False),
            #Start time filter selection
            ui.panel_conditional(
                "input.time_checkbox",
                ui.input_select("start_time", "Start time", TIMES)
            ),
            #End time filter selection
            ui.panel_conditional(
                "input.time_checkbox",
                ui.input_select("end_time", "End time", TIMES)
            ),
            title="Tools",
            width=300
        ),
        ui.card(
            output_widget("map_graph"),
            full_screen=True,
        )
        
    ) 
)


def server(input, output, session):   
    @output
    @render_widget
    def map_graph():
        #I get 50k free loads before having to pay
        TOKEN = "pk.eyJ1IjoiYWx0aWVyYSIsImEiOiJjbG91OWIza3AwZXR0MmpvOXhtbjExMG9lIn0.v_mpsx8D79ahuCbiP4DhNA"
        px.set_mapbox_access_token(TOKEN)
        df = px.data.carshare()

        fig = px.scatter_mapbox(
            df, 
            lat="centroid_lat",
            lon="centroid_lon",
            color="peak_hour",
            size="car_hours",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15,
            zoom=10,
            mapbox_style='streets',
        )
        
        return fig
    
    @output
    @render.data_frame
    def df():
        df = px.data.carshare()
        return df
        


app = App(app_ui, server)
