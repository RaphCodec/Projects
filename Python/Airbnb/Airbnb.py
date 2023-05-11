import pandas as pd

def main():
    df = pd.read_csv('listings.csv')
    print(len(df))
    df = df.drop(['neighbourhood_group_cleansed'], axis=1)
    df = df.dropna()
    print(len(df))


if __name__ == '__main__':
    main()