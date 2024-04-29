from   calendar import monthrange


class Extractor:
    def __init__(self, raw_data, MONTHS:dict[str,int]):
        self.raw_data = raw_data
        self.MONTHS   = MONTHS


    def modes_per_day(self, raw_data:dict):
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
        raw_data = self.raw_data
        data = {}

        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    key       = f'{date}/{self.MONTHS[month]}/{yr[-2:]}'
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



    def most_occuring_times(self, raw_data:dict):
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
        raw_data = self.raw_data
        ranges = [
            (1,    400),
            (401,  800),
            (801,  1200),
            (1201, 1600),
            (1601, 2000),
            (2001, 2400),
        ]
        times = []
        data  = {'%04d-%04d'%i:0 for i in ranges}

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
            for rng in ranges:
                if rng[0] <= int(time) <= rng[1]:
                    key        = f'{rng[0]:04d}-{rng[1]:04d}'
                    data[key] += 1
                    break
    
        return data



    def modes_per_month(self, raw_data:dict):
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
        raw_data = self.raw_data
        data   = {}
        
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



    def total_per_month(self, raw_data:dict):
        '''
        {
            'August-22': 8
        }
        '''
        raw_data = self.raw_data
        data   = {}

        for yr in raw_data:
            for month in raw_data[yr]:
                key       = f'{month}-{yr[-2:]}'
                data[key] = 0
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        data[key] += 1

        return data
    


    def total_modes(self, raw_data:dict):
        '''
        {
            'Imagination': 9,
            'Porn': 4,
            'Hentai': 3,
            'Manga': 1
        }
        '''
        raw_data = self.raw_data
        data = {
            'Imagination': 0,
            'Porn': 0,
            'Hentai': 0,
            'Manga': 0
        }
        
        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        mode = raw_data[yr][month][date][time]
                        data[mode] += 1

        return data
    


    def avg_per_month(self, raw_data:dict):
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
        raw_data = self.raw_data
        data   = {}

        for yr in raw_data:
            for month in raw_data[yr]:
                key        = f'{month}-{yr[-2:]}'
                no_of_days = monthrange(int(yr), self.MONTHS[month])[1]
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
        

        