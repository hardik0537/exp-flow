from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler

from pyspark.ml.evaluation import BinaryClassificationEvaluator,MulticlassClassificationEvaluator

#from pyspark.ml import PipelineModel

sc =SparkContext()
sqlContext = SQLContext(sc)
humidity = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/humidity.csv')
pressure = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/pressure.csv')
temperature = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/temperature.csv')
weather_description = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/weather_description.csv')
wind_direction = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/wind_direction.csv')
wind_speed = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('D:/ExperienceFlow/3/Data/wind_speed.csv')


keep_list = ["datetime", "NewYork"]
keep_list2 = ["datetime", "New York"]
humidity = humidity.select([column for column in humidity.columns if column in keep_list])
humidity2 = humidity.withColumnRenamed("NewYork", "humidity")
 


pressure = pressure.select([column for column in pressure.columns if column in keep_list])
pressure2 = pressure.withColumnRenamed("NewYork", "pressure")

temperature = temperature.select([column for column in temperature.columns if column in keep_list2])
temperature2 = temperature.withColumnRenamed("New York", "temperature")

weather_description = weather_description.select([column for column in weather_description.columns if column in keep_list2])
weather_description2 = weather_description.withColumnRenamed("New York", "weather_description")

wind_direction = wind_direction.select([column for column in wind_direction.columns if column in keep_list2])
wind_direction2 = wind_direction.withColumnRenamed("New York", "wind_direction")

wind_speed = wind_speed.select([column for column in wind_speed.columns if column in keep_list2])
wind_speed2 = wind_speed.withColumnRenamed("New York", "wind_speed")


ny_climate = humidity2.join(pressure2,['datetime'], "inner")
ny_climate = ny_climate.join(temperature2,['datetime'], "inner")
ny_climate = ny_climate.join(weather_description2,['datetime'], "inner")
ny_climate = ny_climate.join(wind_direction2,['datetime'], "inner")
ny_climate = ny_climate.join(wind_speed2,['datetime'], "inner")
# Filling NA, Null values with the previous value as the climate is not going to change drastically in an hour.
ny_climate = ny_climate.fillna('ffill')
#Dropping 1st row of the dataset.
ny_climate = ny_climate.dropna()
'''
ny_climate.select( 
   to_date('datetime', 'yyyy-mm-dd').alias('date') 
  , 'humidity', 'pressure', 'temperature', 'weather_description', 'wind_direction', 'wind_speed'
).show(20)
'''
#new_df = ny_climate.withColumn("new_col", .when(df["col-1"] > 0.0, 1).otherwise(0))
ny_climate = ny_climate.select(
        to_date('datetime', 'yyyy-mm-dd').alias('date'),
        'humidity', 
        'pressure', 
        'temperature', 
        'wind_direction', 
        'wind_speed',
        when( (ny_climate["weather_description"].like("%cloud%")) , 1)
        .when((ny_climate["weather_description"].like("%clear%")) , 2)
        .when((ny_climate["weather_description"].like("thunderstorm%rain%")) | (ny_climate["weather_description"].like("thunderstorm%drizzle%")) , 6)
        .when((ny_climate["weather_description"].like("%snow%")) , 5)
        .when((ny_climate["weather_description"].like("%rain%")) | (ny_climate["weather_description"].like("%drizzle%")) , 4)
        .otherwise(3).alias('weather_desc_cat'))

# Taking mean of the climate features per day. 
ny_climate_agg = ny_climate.groupBy("date") \
    .mean() \
    .orderBy(col("date").desc()) 
#ny_climate_agg.show(20)
ny_climate_agg.toPandas().to_csv('D:/ExperienceFlow/3/ny_climate_agg.csv')
#ny_climate_agg.write.csv('D:/ExperienceFlow/3/ny_climate_agg.csv')
