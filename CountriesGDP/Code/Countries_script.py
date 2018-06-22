# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 23:03:24 2018

@author: Hardik Galiawala
"""

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.offline as off


def read_csv(file_name):
    return pd.read_csv(file_name)

def data_cleaning(dataframe):
    # Replacing NaN with 0 
    clean_df = dataframe.fillna(0)
    # Converting data columns from objects to numeric.
    clean_df = clean_df.convert_objects(convert_numeric=True)
    return clean_df
    

def remove_column(dataframe, column_name):
    return(dataframe.drop(column_name, axis=1))



def plot_scatter(dataframe, x_axis, y_axis, group_hue, graph_title = '', graph_text = ''):
    
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'yellow', 'brown', 'black']
    
    opt = []
    opts = []
    for i in range(0, len(colors)):
        opt = dict(
            target = dataframe[group_hue][[i]].unique(), value = dict(marker = dict(color = colors[i]))
        )
        opts.append(opt)
    
    data = [dict(
      type = 'scatter',
      mode = 'markers',
      x = dataframe[x_axis],
      y = dataframe[y_axis],
      text = dataframe[group_hue],
      hoverinfo = 'text',
      opacity = 0.8,
      marker = dict(
          size = 10,
          sizemode = 'area',
          sizeref = 200000),
      transforms = [
          dict(
            type = 'groupby',
            groups = dataframe[group_hue],
            styles = opts
          ),
          dict(
            type = 'aggregate',
            groups = dataframe[group_hue],
            aggregations = [
                dict(target = 'x', func = 'sum'),
                dict(target = 'y', func = 'sum'),
                dict(target = 'marker.size', func = 'sum')
            ]
          )]
    )]
    
    layout = dict(
        title = '<b>'+graph_title+'</b><br>'+ graph_text +'GDP',
        yaxis = dict(
            type = 'log'
        )
    )
    
    
    off.plot({'data': data, 'layout': layout}, validate=False, image='png')


countries_stats_df = read_csv('countries.csv')
countries_stats_df = data_cleaning(countries_stats_df)
print(countries_stats_df.dtypes)
#plot_scatter(countries_stats_df, "GDP ($ per capita)", "Population", "Country", "1(a)", "GDP (X-axis) v/s Population (Y-axis) v/s Countries")
#plot_scatter(countries_stats_df, "GDP ($ per capita)", "Population", "Region", "1(a)", "GDP (X-axis) v/s Population (Y-axis) v/s Region")


'''
sns.lmplot("GDP ($ per capita)", "Population", 
           data = countries_stats_df,
           hue = "Country")
#sns.despine()
'''
#corr = countries_stats_df.corr()
#print(corr)
#sns.heatmap(corr)
#sns.pairplot(countries_stats_df)