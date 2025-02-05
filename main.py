from   pygal.style import NeonStyle
import pygal

from rich import print_json, inspect
from rich.console import Console

from   calendar import monthrange
from   math     import ceil
import json, os


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
        

        

        








def total_per_month(extractor:Extractor):
    # Initialising
    chart = pygal.HorizontalStackedBar(style=NeonStyle)
    chart.title = 'Total Per Month'

    # Extracting needed data
    data = extractor.modes_per_month()
    data = {i:data[i] for i in list(data.keys())[::-1]}    # Reverses the dic because a horzional stacked bar adds info from the bottom
    
    # Feeding data into chart
    chart.x_labels = data.keys()
    for key in ['Imagination','Porn','Hentai','Manga']:
        chart.add(key, [ data[i][key] for i in data ])

    # Exporting chart
    chart.render_to_file(f'docs/data/total_per_month.svg')



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
    # Initialising
    chart = pygal.Pie(style=NeonStyle)
    chart.title = 'Distribution of modes'

    # Extracting needed data
    data = extractor.total_modes()
    
    # Feeding data into chart
    data  = {key:data[key] for key in sorted(data.keys(), key=lambda x:data[x], reverse=True)}
    total = sum(data.values())
    for key in data.keys():
        chart.add(key, data[key], formatter=lambda x: f'{x} ({ max( round(x/total*100) , 1 )}%)')

    # Exporting chart
    chart.render_to_file(f'docs/data/modes_pie_chart.svg')



def timings_pie_chart(extractor:Extractor):
    # Initialising
    chart       = pygal.Pie(style=NeonStyle)
    chart.title = 'Distribution of timings'

    # Extracting needed data
    data  = extractor.most_occuring_times()
    total = sum(data.values())
    
    # Feeding data into chart
    for key in data.keys():
        chart.add(key, data[key], formatter=lambda x: f'{x} ({ max( round(x/total*100) , 1 )}%)')

    # Exporting chart
    chart.render_to_file(f'docs/data/timings_pie_chart.svg')



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
        total_per_month(extractor)
        modes_per_month(extractor)
        modes_pie_chart(extractor)
        avg_per_month(extractor)
        timings_pie_chart(extractor)
    
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


