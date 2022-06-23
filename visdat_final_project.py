# -*- coding: utf-8 -*-
"""VISDAT_FINAL_PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fTexW06rNFDg8rnR8GN3vY05vieg2HuR

### LIBRARIES
"""
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Colorblind8
from bokeh.layouts import widgetbox, row
from bokeh.models import  Select

data = pd.read_csv("covid_19_indonesia_time_series_all.csv")
data.info()

data = data.rename(columns={'Date': 'date', 
                        'Location ISO Code': 'location_iso_code', 
                        'Location': 'location', 
                        'New Cases': 'new_cases', 
                        'New Deaths': 'new_deaths',
                        'New Recovered': 'new_recovered', 
                        'New Active Cases': 'new_active_cases', 
                        'Total Cases': 'total_cases', 
                        'Total Deaths': 'total_deaths',
                        'Total Recovered': 'total_recovered', 
                        'Total Active Cases': 'total_active_cases', 
                        'Location Level': 'location_level',
                        'City or Regency': 'city_or_regency', 
                        'Province': 'province', 
                        'Country': 'country', 
                        'Continent': 'continent', 
                        'Island': 'island',
                        'Time Zone': 'time_zone', 
                        'Special Status': 'special_status', 
                        'Total Regencies': 'total_regencies', 
                        'Total Cities': 'total_cities',
                        'Total Districts': 'total_districts', 
                        'Total Urban Villages': 'total_urban_villages', 
                        'Total Rural Villages': 'total_rural_villages',
                        'Area (km2)': 'area_(km2)', 
                        'Population': 'population', 
                        'Population Density': 'population_density', 
                        'Longitude': 'longitude',
                        'Latitude': 'latitude', 
                        'New Cases per Million': 'new_cases_per_million', 
                        'Total Cases per Million': 'total_cases_per_million',
                        'New Deaths per Million': 'new_deaths_per_million', 
                        'Total Deaths per Million': 'total_deaths_per_million',
                        'Total Deaths per 100rb': 'total_deaths_per_100rb', 
                        'Case Fatality Rate': 'case_fatality_rate', 
                        'Case Recovered Rate': 'case_recovered_rate',
                        'Growth Factor of New Cases': 'growth_factor_of_new_cases', 
                        'Growth Factor of New Deaths': 'growth_factor_of_new_deaths'})

data['date'] = pd.to_datetime(data['date'])

data['year'] = 2020

data.set_index('year', inplace=True)

data = data.loc[:,['date','location','total_cases','total_deaths','island','province','population','continent','new_cases','new_deaths','total_active_cases']]

data.dropna(how="any",inplace = True)

province_list = data.province.unique().tolist()

island_list = data.island.unique().tolist()

color_mapper = CategoricalColorMapper(factors=island_list, palette=Colorblind8)

color_mapper_2 = CategoricalColorMapper(factors=province_list, 
                                      palette=['#440154', 
                                               '#404387', 
                                               '#29788E', 
                                               '#22A784', 
                                               '#79D151', 
                                               '#FD0724',
                                               '#37AB65', 
                                               '#7C60A8', 
                                               '#CF95D7', 
                                               '#F6CC1D',
                                               '#3DF735', 
                                               '#AD6D70',
                                               '#440154', 
                                               '#404387', 
                                               '#29788E', 
                                               '#22A784', 
                                               '#79D151', 
                                               '#FD0724',
                                               '#37AB65', 
                                               '#7C60A8', 
                                               '#CF95D7', 
                                               '#F6CC1D',
                                               '#3DF735', 
                                               '#AD6D70',
                                               '#440154', 
                                               '#404387', 
                                               '#29788E', 
                                               '#22A784', 
                                               '#79D151', 
                                               '#FD0724',
                                               '#37AB65', 
                                               '#7C60A8', 
                                               '#CF95D7', 
                                               '#F6CC1D'])

source = ColumnDataSource(data={
    "x"                : data.loc[2020].date,
    "y"                : data.loc[2020].total_cases,
    "province"         : data.loc[2020].province,
    "pop"              : data.loc[2020].population,
    "island"           : data.loc[2020].island,
})

plot_1 = figure(title='Persebaran Covid-19 dengan data Kasus dan Kematian', x_axis_label='Total Kematia', y_axis_label='Total Kasus',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='Total Kematian @x| Total Kasus @y | @province' )])

plot_1.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='province', transform=color_mapper_2), legend='province')

plot_1.add_layout(plot_1.legend[0], 'right')

plot_2 = figure(title='Persebaran Covid-19 Indonesia berdasarkan Kasus Baru dan Total Kasus setiap pulau', x_axis_label='Kasus Baru', y_axis_label='Total Kasus',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='Total Kasus @y')])

colors = ['#440154', '#404387', '#29788E', '#22A784', '#79D151', '#FD0724','#37AB65', '#7C60A8', '#CF95D7', '#F6CC1D','#3DF735', '#AD6D70']
color_id =0
for reg in island_list:
    
    date = data.loc[data.island == reg ,'new_cases']
    total_cases = data.loc[data.island == reg ,'total_cases']
    plot_2.circle(date,total_cases ,color= colors[color_id] , alpha=0.8, line_width=4,legend=reg ) 
    
    color_id = color_id + 1

plot_2.legend.location = 'bottom_right'
plot_2.legend.click_policy="hide"

def update_plot(attr, old, new):
    yr = 2020
    x = x_select.value
    y = y_select.value
    plot_1.xaxis.axis_label = x
    plot_1.yaxis.axis_label = y
    new_data = {
    'x'             : data.loc[yr][x],
    'y'             : data.loc[yr][y],
    'province'      : data.loc[yr].province,
    'pop'           : data.loc[yr].population,
    'island'        : data.loc[yr].island_unique,
    }
    source.data = new_data
    
    plot_1.title.text = 'Covid-19 data pulau %d' % yr


x_select = Select(
    options=['total_deaths', 'total_cases', 'new_cases', 'new_deaths'],
    value='total_cases',
    title='Data axis X'
)

x_select.on_change('value', update_plot)

y_select = Select(
    options=['total_deaths', 'total_cases', 'new_cases', 'new_deaths'],
    value='total_cases',
    title='Data axis Y'
)

y_select.on_change('value', update_plot)


layout_2 =  plot_2
curdoc().add_root(layout_2)

layout = row(widgetbox(x_select, y_select), plot_1)
curdoc().add_root(layout)
