import pandas as pd

def loadDataFrame(path: str, num_rows: int) -> None:
    df = pd.read_csv(path, nrows=num_rows)
    print(df.to_string())
    return None

loadDataFrame('../datasets/Bus Arrival Departure Times Apr-June 2020.csv', 50)

