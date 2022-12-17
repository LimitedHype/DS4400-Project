# DS4400-Project

## Recompute datasets (optional)

```
mkdir datasets
cd datasets
# download datasets from https://drive.google.com/drive/folders/1XFQqWuOAkiDSIUuU3IVS0DPfzgqwH1f5?usp=sharing
cd ../dataframe
python3 save.py
python3 convert_to_features.py
python3 save_weather.py

```

## Install Conda env

```
conda env create -f environment.yml
conda activate machine-learning
```

## Run code

```
jupyter notebook src
```
