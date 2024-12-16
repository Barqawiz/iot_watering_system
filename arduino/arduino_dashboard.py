import pandas as pd 
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table

from pathlib import Path
import os
import glob
from typing import List

BASE_PATH = Path(os.getcwd()) / "logs"
FILENAMES = glob.glob(str(BASE_PATH) + "/sensorlogs_*.csv")

def prepare_dataframe(filenames: List[str], moisture_threshold: int = 595) -> pd.DataFrame:
    """
    Helper function to prepare the DataFrame for visualization
    through Plotly and Dash

    Parameters
    ==========
    filenames : List[str]
        List of CSV files to load as Pandas DataFrames

    moisture_threshold: int
        Threshold level for differentiating between dry and wet soil.

    Returns
    =======
        Concatenated DataFrame of all the relevant log files.
    """
    df = pd.concat([pd.read_csv(fname, parse_dates=["timestamp"]) for fname in filenames])
    df["above_threshold"] = df["moisture_reading"] > moisture_threshold
    return df
    

def visualize_data(df: pd.DataFrame):
    """
    Create the Plotly Line Graph based on the measurement readings,
    and append it to a Dash dashboard along with the table of records

    Parameters
    ==========
    df : pd.DataFrame
        DataFrame of soil moisture readings

    Returns
    =======
        Dash App with Graph and Table components    
    """
    # Create the Line Graph component
    fig = go.Figure()

    fig.add_trace(go.Scatter(
         x=df["timestamp"],
         y=df["moisture_reading"],
         mode="lines+markers",
         name="Moisture Level Readings"
    ))

    fig.update_layout(
        title="Moisture Level Readings over Time",
        xaxis_title="Timestamp",
        yaxis_title="Soil Moisture Reading"
    )

    # Create the full Dash App
    app = Dash()

    app.layout = html.Div([
        html.H1("Moisture Sensor Data Dashboard"),
        dcc.Graph(id='sensor-graph', figure=fig),
        html.H2("Moisture Sensor Data Table"),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"id": i, "name": i} for i in df.columns],
            page_size=5,
            style_table={"overflowY": "scroll", "height": "300px"},
            style_cell={"minWidth": "100px"}
        )

    ])
    return app

if __name__ == "__main__":
    df = prepare_dataframe(FILENAMES)
    app = visualize_data(df)
    app.run(debug=True)