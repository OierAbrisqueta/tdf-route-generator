from pathlib import Path
import pandas as pd
import kagglehub

# Download latest version
path = kagglehub.dataset_download("ralle360/historic-tour-de-france-dataset")
INPUT_CSV = Path(path)

