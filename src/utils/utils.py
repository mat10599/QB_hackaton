import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from variables import DATA_PATH, SRC_PATH


def generate_and_save_data_plume():
    metadata_path = DATA_PATH / "train_data" / "metadata.csv"
    output_path = SRC_PATH / "app_utils" / "assets" / "data" / "location.csv"
    metadata = pd.read_csv(metadata_path)
    metadata["probability"] = 1
    plume_data = metadata[metadata["plume"]=="yes"][["lat", "lon", "probability"]]
    plume_data["detected"] = True
    plume_data.to_csv(output_path, index=False)


# generate_and_save_data_plume()
