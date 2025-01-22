import pandas as pd
from pathlib import Path
    
def load_file(filePath):
    file = Path(filePath)
    if not file.exists():
        raise FileNotFoundError(f"File {file} not found")
    if file.suffix == ".json":
        return pd.read_json(file)
    elif file.suffix == ".csv":
        return pd.read_csv(file)
    elif file.suffix in (".xls", ".xlsx"):
        return pd.read_excel(file)
    raise ValueError("Invalid file format")

def filter_data(filePath, **kwargs):
    df = load_file(filePath)
    filtered_data = []
    data = df.to_dict(orient="records")
    for item in data:
        if all(item.get(key) == value for key, value in kwargs.items()):
            filtered_data.append(item)
 
    return filtered_data

filter_output = filter_data(r'E:\GRC\output\Jewel_2025-01-22_validated.json',weight="Approx",volume_deals_description="Sale Price: $4.99 Lb Save Up To: $1.0 Lb")
print(filter_output)