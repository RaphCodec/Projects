import pandas as pd
import tomli

with open('FastFood.config.toml', mode='rb') as fp:
    config = tomli.load(fp)

SRC_FILE = config['SRC_FILE']

df = pd.read_csv(SRC_FILE)

print(df)