def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['ACCIDENT DATE', 'ACCIDENT TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'accident date_accident time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

