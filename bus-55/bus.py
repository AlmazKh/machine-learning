import pandas as pandas
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble  import RandomForestRegressor

columns = ["report_time", "event_time", "garag_numb", "marsh", "graph", "smena", "time_nav", "latitute",
           "longitude", "speed", "azimuth"]
dtypes = [datetime, datetime, str, int, int, int, datetime, float, float, int, int]
# ONLY GARAG NUMBER = 4707
dataset = pandas.read_csv("select___from_kazan_bus_log_where_garag_.csv", parse_dates=['report_time'])

dataset['hour'] = dataset['report_time'].dt.hour
dataset['minute'] = dataset['report_time'].dt.minute
dataset['second'] = dataset['report_time'].dt.second

X = dataset[['hour', 'minute', 'second']]
y = dataset[['latitute', 'longitude']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

model = RandomForestRegressor(n_estimators=25, random_state=42, max_depth=15, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_pred = pandas.DataFrame({'latitute': y_pred[:, 0], 'longitude': y_pred[:, 1]})

y_test = y_test.reset_index()
X_test = X_test.reset_index()

d = pandas.DataFrame({'Hour': X_test['hour'], 'Minute': X_test['minute'], 'Second': X_test['second'],
                  'Actual latitude': y_test['latitute'], 'Predicted latitude': y_pred['latitute'],
                  'Actual Longitude': y_test['longitude'], 'Predicted Longtitude': y_pred['longitude']})


pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)
print(d)
