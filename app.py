from shiny import App, render, ui
from shinywidgets import output_widget, register_widget, render_widget
import numpy as np
import plotly.graph_objs as go
import plotly.express as px



app_ui = ui.page_fluid(
    ui.h2("Interactive Traffic Map"),
    ui.markdown("Insert explanation of what this thing is"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_date_range(id = "date_range",
                                label = "Date range input"),
             ui.output_data_frame("df")
        ),
        ui.panel_main(
            output_widget("map_graph")
        )
    )
    
    
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"Your date is{input.date_range()}"
    
    @output
    @render_widget
    def map_graph():
        TOKEN = "pk.eyJ1IjoiYWx0aWVyYSIsImEiOiJjbG91OWIza3AwZXR0MmpvOXhtbjExMG9lIn0.v_mpsx8D79ahuCbiP4DhNA"
        px.set_mapbox_access_token(TOKEN)
        df = px.data.carshare()
        
        fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)  

        return fig
    
    @output
    @render.data_frame
    def df():
        df = px.data.carshare()
        return df
        


app = App(app_ui, server)
