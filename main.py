from   pygal.style import NeonStyle, Style, LightColorizedStyle, LightStyle, DefaultStyle, CleanStyle
import pygal
import calplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

from rich import print_json, inspect
from rich.console import Console
from extractor import Extractor

from   calendar import monthrange
<<<<<<< HEAD
from   datetime import datetime, timedelta
from   dateutil.relativedelta import relativedelta
=======
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807
from   math     import ceil
import json, os
from   typing import Union, List
from   collections import defaultdict
from   operator import lt, gt

webpage_bg_color = [10/255, 10/255, 10/255]
text_color_calplot = 'white'
rcParams['text.color'] = text_color_calplot

# For calplot
from matplotlib.colors import LinearSegmentedColormap, Colormap, ListedColormap

def generate_cmap(max_faps:int) -> LinearSegmentedColormap:
    # Make sure the first color is transparent, for the -1 values
    colors = [webpage_bg_color]
    # Now generate n_bins - 1 colors from white to dark red
    range_of_colors = ['white', '#ffd700', '#ff8c00', '#ff4500', '#8b0000']
    linear_cmap  = LinearSegmentedColormap.from_list('custom_cmap', range_of_colors, N=max_faps)
    other_colors = linear_cmap(np.linspace(0, 1, max_faps))
    # Append them and return
    colors.extend(other_colors)
    cmap = ListedColormap(colors)
    return cmap, linear_cmap

# colors = ['white', '#ffd700', '#ff8c00', '#ff4500', '#8b0000']  # white to dark red
# n_bins = 6
# cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=n_bins)

NeonStyle.transition        = '0.3s ease-out'
NeonStyle.background        = 'transparent'
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

LightNeonStyle = Style(
    background='transparent',
    plot_background='#f8f8f8',
    foreground='rgba(30, 30, 30, 1)',
    foreground_strong='rgba(0, 0, 0, 1)',
    foreground_subtle='#aaa',
    guide_stroke_color='#ccc',
    guide_stroke_dasharray='4,4',
    major_guide_stroke_color='#bbb',
    major_guide_stroke_dasharray='6,6',

    colors=(
        '#ff005d',  # hot pink
        '#44d62c',  # bright green
        '#00eaff',  # cyan
        '#a262f4',  # lavender neon
        '#5c6975',  # steel
        '#ff6e6e',  # soft red
        '#ff2c9c',  # pinkish magenta
        '#96e072',  # light lime
        '#fdae61',  # warm orange
        '#4cc9f0',  # sky blue
        '#6c757d',  # muted grey
        '#7b2cbf'   # rich purple
    ),

    dot_opacity='1',
    opacity='.3',
    opacity_hover='.8',
    stroke_opacity='.8',
    stroke_opacity_hover='.95',
    stroke_width='1',
    stroke_width_hover='4',

    font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    label_font_size=10,
    legend_font_size=14,
    major_label_font_size=10,
    no_data_font_size=64,
    title_font_size=16,
    tooltip_font_size=14,
    value_font_size=16,
    value_label_font_size=10,

    transition='0.3s ease-out',
    value_background='rgba(240, 240, 240, 1)',
)

STYLES = [NeonStyle, LightNeonStyle]





<<<<<<< HEAD
# Decorator for dual theme pygal plots
def dual_theme_pygal(base_filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for style, suffix in zip(STYLES, ['dark', 'light']):
                themed_filename = f"{base_filename}_{suffix}.svg"
                func(*args, style=style, filename=themed_filename, **kwargs)
        return wrapper
    return decorator
=======

class Extractor:
    def __init__(self, raw_data:dict):
        self.raw_data = raw_data


    def modes_per_day(self):
        '''
        {
            '1/11/21': {
                'Imagination': 1,
                'Porn': 1,
                'Hentai: 0,
                'Manga: 0
            }
        }
        '''
        data = {}
        raw_data = self.raw_data

        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    key       = f'{date}/{MONTHS[month]}/{yr[-2:]}'
                    data[key] = {
                        'Imagination': 0,
                        'Porn': 0,
                        'Hentai': 0,
                        'Manga': 0
                    }
                    for time in raw_data[yr][month][date]:
                        mode = raw_data[yr][month][date][time]
                        data[key][mode] += 1
        
        return data



    def most_occuring_times(self):
        '''
        {
            '0001 - 0400': x,
            '0401 - 0800': x,
            '0801 - 1200': x,
            '1201 - 1600': x,
            '1601 - 2000': x,
            '2001 - 2400': x,
        }
        '''
        ranges = [
            (1,    400),
            (401,  800),
            (801,  1200),
            (1201, 1600),
            (1601, 2000),
            (2001, 2400),
        ]
        times = []
        data = { f'{i:04d}-{j:04d}' : 0 for i,j in ranges }
        raw_data = self.raw_data

        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        times.append(time)

        # Replace all the '0000' with '2400', cz its mathematically easier
        for i, time in enumerate(times):
            if time == '0000':
                times[i] = '2400'
        
        for time in times:
            for start,end in ranges:
                if start <= int(time) <= end:
                    key        = f'{start:04d}-{end:04d}'
                    data[key] += 1
                    break
    
        return data



    def modes_per_month(self):
        '''
        {
            'August-22': {
                'Imagination': 5,
                'Porn': 2,
                'Hentai: 0,
                'Manga: 1
            }
        }
        '''
        data   = {}
        raw_data = self.raw_data
        
        for yr in raw_data:
            for month in raw_data[yr]:
                key       = f'{month}-{yr[-2:]}'
                data[key] = {
                    'Imagination': 0,
                    'Porn': 0,
                    'Hentai': 0,
                    'Manga': 0
                }
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        mode = raw_data[yr][month][date][time]
                        data[key][mode] += 1

        return data
    


    def total_modes(self):
        '''
        {
            'Imagination': 9,
            'Porn': 4,
            'Hentai': 3,
            'Manga': 1
        }
        '''
        data = {
            'Imagination': 0,
            'Porn': 0,
            'Hentai': 0,
            'Manga': 0
        }
        raw_data = self.raw_data
        
        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        mode = raw_data[yr][month][date][time]
                        data[mode] += 1

        return data
    


    def avg_per_month(self):
        '''
        {
            'August-22': {
                'Total': 1.3,
                'Imagination': 1,
                'Porn': 0.1,
                'Hentai': 0.1,
                'Manga': 0.1
            }
        }
        '''
        data   = {}
        raw_data = self.raw_data

        for yr in raw_data:
            for month in raw_data[yr]:
                key        = f'{month}-{yr[-2:]}'
                no_of_days = monthrange(int(yr), MONTHS[month])[1]
                data[key]  = {
                    'Total': 0,
                    'Imagination': 0,
                    'Porn': 0,
                    'Hentai': 0,
                    'Manga': 0
                }
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        mode = raw_data[yr][month][date][time]
                        data[key][mode]    += 1
                        data[key]['Total'] += 1
                for i in data[key]:
                    data[key][i] = round( data[key][i] / no_of_days , 2 )
        
        return data
        

        

        
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807




def statistics(extractor:Extractor):
    total_stuff = extractor.total_stuff()
    most_time = sorted(extractor.times_frequncies().items(), key=lambda x:x[1], reverse=True)[0]
    most_time = {'time': most_time[0], 'count': most_time[1]}  # {'time': '0000', 'count': 5}
    most_time 
    stats = {
        'totalFaps':          total_stuff['totalFaps'],
        'avgPerDay':          total_stuff['avgPerDay'],
        'activeDays':         total_stuff['activeDays'],
        'nDays':              total_stuff['nDays'],
        'timeDiff':           total_stuff['timeDiff'],
        'mostDay':            extractor.most_day(),
        'leastTimeDiff':      extractor.least_most_time_diff(type_='least'),
        'mostTimeDiff':       extractor.least_most_time_diff(type_='most'),
        'mostTime':           most_time,
        'longestFapStreak':   extractor.longest_fap_nofap_streak(type_='fap'),
        'longestNofapStreak': extractor.longest_fap_nofap_streak(type_='nofap'),
    }
    with open('docs/stats.json', 'w') as f: json.dump(stats, f, indent=4)




<<<<<<< HEAD
@dual_theme_pygal('docs/charts/total_per_month')
def total_per_month(extractor:Extractor, style=None, filename=None):
    '''
    Creates a horizontal stacked bar chart for total per month, grouped by mode.
    '''
=======
def total_per_month(extractor:Extractor):
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807
    # Initialising
    chart = pygal.HorizontalStackedBar(style=style)
    chart.title = 'Total Per Month'

    # Extracting needed data
    data = extractor.modes_per_month()
    data = {i:data[i] for i in list(data.keys())[::-1]}    # Reverses the dic because a horzional stacked bar adds info from the bottom
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in ['Imagination','Porn','Hentai','Manga']:
        chart.add(key, [ data[i][key] for i in data ])

    # Exporting chart
    chart.render_to_file(filename)



<<<<<<< HEAD
@dual_theme_pygal('docs/charts/average_per_month')
def avg_per_month(extractor:Extractor, style=None, filename=None):
    '''
    Creates a line chart for average per day for every month.
    '''
=======
def avg_per_month(extractor:Extractor):
    # Initialising
    chart = pygal.Line(style=NeonStyle)
    chart.title = 'Average/Day For Every Month'

    # Extracting needed data
    data = extractor.avg_per_month()
    data = {key:val['Total'] for key,val in data.items()}
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    chart.x_label_rotation = -90
    chart.add('Total', [ data[i] for i in data ])

    # Set lower limit to 0 and upper limit to ceiling of max value
    chart.range = (0, ceil(max(data.values())))
    # Exporting chart
    chart.render_to_file(f'docs/data/average_per_month.svg')



def modes_per_month(extractor:Extractor):
    # Initialising
    chart = pygal.HorizontalStackedBar(style=NeonStyle, value_formatter=lambda x: f'{round(x*100)}%')
    chart.title = 'Distribution of Modes Per Month'

    # Extracting needed data
    data = extractor.modes_per_month()
    data = {i:data[i] for i in list(data.keys())[::-1]}    # Reverses the dic because a horzional stacked bar adds info from the bottom
    
    # Turns the data into a proportion
    for key in data:
        total = sum(data[key].values())
        for mode in data[key]:
            data[key][mode] = data[key][mode] / total
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in ['Imagination','Porn','Manga','Hentai']:
        chart.add(key, [ data[i][key] for i in data ])
    
    # Exporting chart
    chart.render_to_file(f'docs/data/modes_per_month.svg')



def modes_pie_chart(extractor:Extractor):
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807
    # Initialising
    chart = pygal.Line(style=style)
    chart.title = 'Average/Day For Every Month'

    # Extracting needed data
    data = extractor.avg_per_month()
    data = {key:val['Total'] for key,val in data.items()}
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    chart.x_label_rotation = -90
    chart.add('Total', [ data[i] for i in data ])

    # Set lower limit to 0 and upper limit to ceiling of max value
    chart.range = (0, ceil(max(data.values())))
    # Exporting chart
    chart.render_to_file(filename)



@dual_theme_pygal('docs/charts/modes_per_month')
def modes_per_month(extractor:Extractor, style=None, filename=None):
    '''
    Creates a horizontal stacked bar chart for the distribution of modes per month (as proportions).
    '''
    # Initialising
    chart = pygal.HorizontalStackedBar(style=style, value_formatter=lambda x: f'{round(x*100)}%')
    chart.title = 'Distribution of Modes Per Month'

    # Extracting needed data
    data = extractor.modes_per_month()
    data = {i:data[i] for i in list(data.keys())[::-1]}    # Reverses the dic because a horzional stacked bar adds info from the bottom
    
    # Turns the data into a proportion
    for key in data:
        total = sum(data[key].values())
        for mode in data[key]:
            data[key][mode] = data[key][mode] / total
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in ['Imagination','Porn','Manga','Hentai']:
        chart.add(key, [ data[i][key] for i in data ])
    
    # Exporting chart
    chart.render_to_file(filename)



@dual_theme_pygal('docs/charts/modes_pie_chart')
def modes_pie_chart(extractor:Extractor, style=None, filename=None):
    '''
    Creates a pie chart for the distribution of modes (total counts).
    '''
    # Initialising
    chart = pygal.Pie(style=style)
    chart.title = 'Distribution of modes'

    # Extracting needed data
    data = extractor.total_modes()
    
    # Feeding data into chart
    data  = {key:data[key] for key in sorted(data.keys(), key=lambda x:data[x], reverse=True)}
    total = sum(data.values())
    for key in data.keys():
        chart.add(key, data[key], formatter=lambda x: f'{x} ({ max( round(x/total*100) , 1 )}%)')

    # Exporting chart
    chart.render_to_file(filename)



<<<<<<< HEAD
@dual_theme_pygal('docs/charts/timings_pie_chart')
def timings_pie_chart(extractor:Extractor, style=None, filename=None):
    '''
    Creates a pie chart for the distribution of timings (time bins).
    '''
    # Initialising
    chart = pygal.Pie(style=style)
    chart.title = 'Distribution of timings'

    # Extracting needed data
    data  = extractor.most_occuring_time_bins()
=======
def timings_pie_chart(extractor:Extractor):
    # Initialising
    chart       = pygal.Pie(style=NeonStyle)
    chart.title = 'Distribution of timings'

    # Extracting needed data
    data  = extractor.most_occuring_times()
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807
    total = sum(data.values())
    
    # Feeding data into chart
    for key in data.keys():
        chart.add(key, data[key], formatter=lambda x: f'{x} ({ max( round(x/total*100) , 1 )}%)')

    # Exporting chart
    chart.render_to_file(filename)



@dual_theme_pygal('docs/charts/timings_bar_chart')
def timings_bar_chart(extractor:Extractor, style=None, filename=None):
    '''
    Creates a horizontal bar chart for the top 10 timings (most frequent times).
    '''
    # Initialising
    chart = pygal.HorizontalBar(style=style, value_formatter=lambda x: f'{round(x*100)}%')
    chart.title = 'Top 10 timings'

    # Extracting needed data
    data = extractor.times_frequncies()
    
    # Feeding data into chart
    total = sum(data.values())
    data  = {key:data[key] for key in sorted(data.keys(), key=lambda x:data[x], reverse=True)[:10]}
    for key in data.keys():
        chart.add(key, data[key], formatter=lambda x: f'{x} ({ max( round(x/total*100) , 1 )}%)')

    # Exporting chart
    chart.render_to_file(filename)



def calendar_heatmap(extractor:Extractor):
    # Extract data per day
    data = extractor.modes_per_day()
    
    # Convert to pandas Series with datetime index
    dates:list[pd.Timestamp] = []
    values = []
    for date_str, modes in data.items():
        # Convert date string to datetime
        day, month, year = date_str.split('/')
        date = pd.to_datetime(f'20{year}-{month}-{day}')
        # Sum up all modes for the day
        total = sum(modes.values())
        dates.append(date)
        values.append(total)
    
    # Create Series with datetime index
    series = pd.Series(values, index=dates)
    
    start_date = min(dates)
    end_date   = max(dates)
    start_month , start_year = start_date.month, start_date.year
    end_month   , end_year   = end_date.month, end_date.year

    # Fill the dates from 1st jan of start_year to last day of the month before start_month with -1
    start  = pd.Timestamp(year=start_year, month=1,           day=1)
    end    = pd.Timestamp(year=start_year, month=start_month, day=1) - pd.Timedelta(days=1)
    start_dates  = pd.date_range(start, end, freq='D').to_list()
    start_series = pd.Series(-1, index=start_dates)

    # Fill the dates from 1st day of next month of end_month to end of the year with -1
    start = pd.Timestamp(year=end_year, month=end_month+1, day=1)
    end   = pd.Timestamp(year=end_year, month=12, day=31)
    end_dates  = pd.date_range(start, end, freq='D').to_list()
    end_series = pd.Series(-1, index=end_dates)

    # Concatenate the start, series and end series
    series = pd.concat([start_series, series, end_series])

    
    # Create calendar heatmap (cis_cmap -> cmap w/o trans)
    cmap, cis_cmap = generate_cmap(max(series))
    fig, axs = calplot.calplot(
        series,
        cmap=cmap,
        # cmap = 'YlOrRd',
        edgecolor='black',
        linewidth=0.5,
        colorbar=False,
        subplot_kws = {'facecolor': '#11000020'}, # idk how it works, but it just works
        # subplot_kws={'facecolor': webpage_bg_color},
        suptitle='Total Faps Per Day',
        # colorbar_kws={'label': 'Count', 'labelcolor': text_color_calplot, 'tickcolor': text_color_calplot}
    )

    # Add colorbar with custom styling
    norm = plt.Normalize(0, max(series))
    sm = plt.cm.ScalarMappable(cmap=cis_cmap, norm=norm)
    # cbar = plt.colorbar(sm, ax=axs)  # Make colorbar thinner with fraction and add some padding
    cbar = plt.colorbar(sm, ax=axs, aspect=60)  # Make colorbar thinner with fraction and add some padding
    cbar.set_label('Count', color=text_color_calplot)
    cbar.ax.yaxis.set_tick_params(color=text_color_calplot)
    cbar.ax.yaxis.label.set_color(text_color_calplot)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=text_color_calplot)

    # Customise label colors
    for ax in axs.ravel():  # Handle multiple months
        # Weekday labels
        for label in ax.get_yticklabels():
            label.set_color(text_color_calplot) 
            label.set_fontsize(8)
        # Month Labels
        for label in ax.get_xticklabels():label.set_color(text_color_calplot)


    # Save the plot
    plt.savefig('docs/charts/calendar_heatmap.png', bbox_inches='tight', dpi=600, transparent=True)
    plt.close()





# def total_per_day(raw_data:dict):
#     # Initialising
#     chart = pygal.Bar(style=NeonStyle)
#     chart.title = 'Average/Day For Every Month'
#     chart.config.show_legend = False

#     # Extracting needed data
#     data = extractor.modes_per_day(raw_data)
#     # data = {i:data[i] for i in list(data.keys())[::-1]}                   # Reverses the dic because a horzional chart adds info from the bottom
    
#     # Feeding data into chart
#     chart.x_labels = data.keys()
#     for key in ['Imagination','Porn','Hentai','Manga']:
#         chart.add(key, [ data[i][key] for i in data ])

#     # Exporting chart
#     chart.render_to_file(f'docs/data/total_per_day.svg')






if __name__ == '__main__':
    try:
        console = Console()
        
        raw_data = {}
        with open('docs/data.json') as f:
            raw_data = json.load(f)

        extractor = Extractor(raw_data)
<<<<<<< HEAD
        statistics(extractor)
        total_per_month(extractor)
        avg_per_month(extractor)
        modes_per_month(extractor)
        modes_pie_chart(extractor)
        timings_pie_chart(extractor)
        # # timings_bar_chart(extractor)
        # # calendar_heatmap(extractor)
        # # calendar_heatmap_altair(extractor)
=======
        total_per_month(extractor)
        modes_per_month(extractor)
        modes_pie_chart(extractor)
        avg_per_month(extractor)
        timings_pie_chart(extractor)
>>>>>>> 3e1edf18b40924974f1fb26abc2ed2aee039c807
    
    except Exception as e:
        console.print_exception()









'''
Total per month (stacked graph w/ modes)
Average per month ??
per day (stacked graph w/ modes)
Pie chart of modes
Most used times (like 0000-0800, 0800-1600, 1600-2400)

-> Add raw data
'''


