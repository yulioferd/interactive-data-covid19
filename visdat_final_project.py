# -*- coding: utf-8 -*-
"""VISDAT_FINAL_PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fTexW06rNFDg8rnR8GN3vY05vieg2HuR

### LIBRARIES
"""

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6,Colorblind8
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select
from bokeh.io import show


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

data["DateString"] = data["date"].dt.strftime("%Y%m%d")

data['DateString'] = data['DateString'].astype(float)

# data.head()

data.set_index('DateString', inplace=True)

# data.info()

data = data.loc[:,['date','location','total_cases','total_deaths','province','population','island','continent','new_cases','new_deaths','total_active_cases']]

data.head()

data.dropna(how="any",inplace = True)
data.info()

data

# Make a list of the unique values from the region column: regions_list
province_list = data.province.unique().tolist()

island_list = data.island.unique().tolist()

island_list

color_mapper = CategoricalColorMapper(factors=province_list, palette=Colorblind8)

source = ColumnDataSource(data={
    "x"                : data.loc[data['island'] == 'Sumatera'].date,
    "y"                : data.loc[data['island'] == 'Sumatera'].total_cases,
    "province"         : data.loc[data['island'] == 'Sumatera'].province,
    "pop"              : data.loc[data['island'] == 'Sumatera'].population,
    "island"           : data.loc[data['island'] == 'Sumatera'].island,
})

# Create the figure: plot
plot = figure(title='Covid-19 Indonesia', x_axis_label='Date', y_axis_label='Total Kasus',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@y')])

plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='province', transform=color_mapper), legend='province')

plot.legend.location = 'top_left'

def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    # yr = slider.value
    x_island = select_island.value
    # y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = 'x'
    plot.yaxis.axis_label = 'y'
    # new data
    new_data = {
    'x'             : data.loc[data['island'] == x_island].date,
    'y'             : data.loc[data['island'] == x_island].total_cases,
    'province'      : data.loc[data['island'] == x_island].province,
    'pop'           : data.loc[data['island'] == x_island].population,
    'island'        : data.loc[data['island'] == x_island].island,

    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'Covid-19 data pulau %d' % x_island

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
select_island = Select(
    options=island_list,
    value='Nusa Tenggara',
    title='Pulau Indonesia'
)

# Attach the update_plot callback to the 'value' property of x_select
select_island.on_change('value', update_plot)

# y_select = Select(
#     options=['total_deaths', 'total_cases', 'new_cases', 'new_deaths'],
#     value='total_cases',
#     title='y-axis data'
# )

# Attach the update_plot callback to the 'value' property of y_select
# y_select.on_change('value', update_plot)

# Create layout and add to current document
layout = row(widgetbox(select_island), plot)
curdoc().add_root(layout)

show(layout)