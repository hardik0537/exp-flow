
import pandas as pd
import datetime
import numpy 
from sklearn.ensemble import RandomForestClassifier
climate_crime = pd.read_csv('ProcessedData/ny_climate_crime.csv')
print(climate_crime.dtypes)
climate_crime = climate_crime.drop('OFNS_DESC', axis=1)
climate_crime = climate_crime.drop('date', axis=1)
features_list = climate_crime.columns.values[0:6]
print("Features List:", features_list)
X = climate_crime.values[:,0:6]
#print(X)
#set y equal to all Score values
y = climate_crime.values[:,-1]
#print(y)


rf = RandomForestClassifier()
rf.fit(X, y)
print("Features sorted by their score:")
print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), features_list), 
             reverse=True))