import pandas as pd
from pathlib import Path

def load_data(file_path):
    path = Path(file_path)
    
    if not path.is_file():
        # Try resolving from the project root
        path = Path.cwd().parent / file_path
    
    if not path.is_file():
        print(f"Error: Data file not found at '{path}'")
        return None

    return pd.read_csv(path)

