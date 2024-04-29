from   pygal.style import NeonStyle
import pygal

import parser
from extractor import Extractor

import json, os


NeonStyle.transition        = '0.3s ease-out'
NeonStyle.background      = 'rgba(0,0,0,0)'
NeonStyle.foreground        = 'rgba(200, 200, 200, 1)'
NeonStyle.foreground_strong = 'rgba(255, 255, 255, 1)'
NeonStyle.colors = (
    '#ff5995',
    '#b6e354',
    # '#feed6c',
    '#8cedff',
    '#9e6ffe',
    '#899ca1',
    '#f8f8f2',
    '#bf4646',
    # '#516083',
    '#f92672',
    '#82b414',
    '#fd971f',
    '#56c2d6',
    '#808384',
    '#8c54fe',
    # '#465457'
)

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

MODES = [
    'Imagination',
    'Porn',
    'Manga',
    'Hentai'
]








        








def modes_per_month(raw_data:dict):
    # Initialising
    chart = pygal.HorizontalStackedBar(style=NeonStyle)
    chart.title = 'Modes Per Month'

    # Extracting needed data
    data = extractor.modes_per_month(raw_data)
    data = {i:data[i] for i in list(data.keys())[::-1]}    # Reverses the dic because a horzional stacked bar adds info from the bottom
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in MODES:
        chart.add(key, [ data[i][key] for i in data ])

    # Exporting chart
    chart.render_to_file(f'docs/charts/modes_per_month.svg')


def total_per_month(raw_data:dict):
    # Initialising
    chart = pygal.Line(style=NeonStyle)
    chart.title = 'Total Per Month'

    # Extracting needed data
    data = extractor.total_per_month(raw_data)

    # Feeding data into chart
    chart.x_labels = data.keys()
    chart.add('Total', [ data[i] for i in data ])
    # Rotating the x-axis labels
    chart.x_label_rotation = 90
    # Set the y axis to start from 0
    chart.range = (0, max(data.values())+1)

    # Exporting chart
    chart.render_to_file(f'docs/charts/total_per_month.svg')



def modes_pie_chart(raw_data:dict):
    # Initialising
    chart = pygal.Pie(style=NeonStyle)
    chart.title = 'Distribution of modes'

    # Extracting needed data
    data = extractor.total_modes(raw_data)
    # Sorts the data in descending order
    data = {key:val for key, val in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    
    # Feeding data into chart
    for key in data.keys():
        chart.add(key, data[key])

    # Exporting chart
    chart.render_to_file(f'docs/charts/modes_pie_chart.svg')



def total_per_day(raw_data:dict):
    # Initialising
    chart = pygal.Bar(style=NeonStyle)
    chart.title = 'Average/Day For Every Month'
    chart.config.show_legend = False

    # Extracting needed data
    data = extractor.modes_per_day(raw_data)
    # data = {i:data[i] for i in list(data.keys())[::-1]}                   # Reverses the dic because a horzional chart adds info from the bottom
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in ['Imagination','Porn','Hentai','Manga']:
        chart.add(key, [ data[i][key] for i in data ])

    # Exporting chart
    chart.render_to_file(f'docs/charts/total_per_day.svg')



def timings_pie_chart(raw_data:dict):
    # Initialising
    chart       = pygal.Pie(style=NeonStyle)
    chart.title = 'Distribution of timings'

    # Extracting needed data
    data = extractor.most_occuring_times(raw_data)
    
    # Feeding data into chart
    for key in data.keys():
        chart.add(key, data[key])

    # Exporting chart
    chart.render_to_file(f'docs/charts/timings_pie_chart.svg')




parser.main()

with open('docs/data.json') as f:
    raw_data = json.load(f)

extractor = Extractor(raw_data, MONTHS)

total_per_month(raw_data)
modes_per_month(raw_data)
total_per_day(raw_data)
modes_pie_chart(raw_data)
timings_pie_chart(raw_data)
    










'''
-> Make the timings pie chart into a bin chart
-> Make the total per day into a line chart
-> Add a bar-like chart depicting the ratio of the modes
'''


