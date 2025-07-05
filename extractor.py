import pandas as pd

from calendar import monthrange
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union, List
from collections import defaultdict
from operator import lt, gt



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
    'December': 12,
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}




class Extractor:
    def __init__(self, raw_data:dict):
        self.data = {}

        # Convert the years and dates to ints
        for yr_ in raw_data:
            yr = int(yr_)
            self.data[yr] = {}
            for month in raw_data[yr_]:
                self.data[yr][month] = {}
                for date_ in raw_data[yr_][month]:
                    date = int(date_)
                    self.data[yr][month][date] = raw_data[yr_][month][date_].copy()
        
        start_year  = min(self.data.keys()) # 2021
        start_month = min(self.data[start_year].keys(), key=lambda x: MONTHS[x]) # April
        start_date  = min(self.data[start_year][start_month].keys()) # 1

        end_year    = max(self.data.keys()) # 2025
        end_month   = max(self.data[end_year].keys(), key=lambda x: MONTHS[x]) # 'December'
        end_date    = max(self.data[end_year][end_month].keys()) # 31

        self.start_date = datetime(start_year, MONTHS[start_month], start_date)
        self.end_date   = datetime(end_year,   MONTHS[end_month],   end_date)
        self.date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='D')



    def total_stuff(self) -> dict:
        '''
        {
            'totalFaps': 100,
            'avgPerDay': 1.5,
            'nDays': 67,
            'timeDiff': {
                'years':  2,
                'months': 3,
                'days':   15
            }
        '''
        total = sum(
            len(self.data[yr][month][date])
            for yr    in self.data
            for month in self.data[yr]
            for date  in self.data[yr][month]
        )
        time_diff     = self.end_date - self.start_date
        n_days        = time_diff.days + 1
        relative_diff = relativedelta(self.end_date + timedelta(days=1), self.start_date)
        avg_per_day   = total / n_days

        active_days = len([date for date in self.date_range if any(self.data[date.year][MONTHS[date.month]][date.day].values())])
        
        return {
            'totalFaps': total,
            'avgPerDay': round(avg_per_day, 2),
            'activeDays': active_days,
            'nDays': n_days,
            'timeDiff': {
                'years':  relative_diff.years,
                'months': relative_diff.months,
                'days':  relative_diff.days
            }
        }



    def longest_fap_nofap_streak(self, type_='fap') -> Union[List[tuple], int]:
        '''
        Returns the longest streak of consecutive days with faps and the length of that streak
        [('01-01-2021', '05-01-2021'), ('10-01-2021', '15-01-2021')] , 5
        '''
        date_range = self.date_range

        # Basically we create a dict where the keys are the dates and the value is a boolean indicating whether there is a fap on that date
        has_fapped = {date: False for date in date_range}
        for yr in self.data:
            for month in self.data[yr]:
                for day in self.data[yr][month]:
                    if len(self.data[yr][month][day]) == 0: continue
                    date = datetime(yr, MONTHS[month], day)
                    has_fapped[date] = True
        
        # We use a 2 pointer approach to find the longest streak(s). Sort of like leetcode 485 (Max Consecutive Ones)
        pairs       = []
        max_streak  = 0
        curr_streak = 0
        start_date  = None
        end_date    = None
        # If it is a fap streak, we look for 1s, else for 0s
        target = True if type_ == 'fap' else False

        for date in date_range:
            if has_fapped[date] == target:
                # If its the start of a streak
                if curr_streak == 0:
                    curr_streak = 1
                    start_date  = date
                else: curr_streak += 1
            else:
                # If its the end of a streak
                if curr_streak:
                    end_date = date - timedelta(days=1)
                    # Check if its the same as max streak
                    if curr_streak == max_streak: pairs.append((start_date,end_date))
                    # If its bigger
                    elif curr_streak > max_streak:
                        max_streak = curr_streak
                        pairs = [(start_date,end_date)]
                    curr_streak = 0
                    start_date = end_date = None
        
        pairs = [ {'start': start.strftime('%d-%m-%Y'), 'end': end.strftime('%d-%m-%Y')} for start, end in pairs ]
        return {'pairs': pairs, 'maxStreak': max_streak}



    def most_day(self) -> Union[List[str], int]:
        '''
        Returns the day(s) with the most faps and the number of faps on that day, as well as the modes
        ['01-01-2021', '02-01-2021'] , 5 , {'01-01-2021': {'Imagination':1}}
        '''
        max_faps = 0
        max_days = []

        for yr in self.data:
            for month in self.data[yr]:
                for date in self.data[yr][month]:
                    faps = len(self.data[yr][month][date].values())
                    readable   = datetime(yr, MONTHS[month], date).strftime('%d-%m-%Y')
                    if faps > max_faps:
                        max_faps = faps
                        max_days = [readable]
                    elif faps == max_faps:
                        max_days.append(readable)
        
        # Get the modes for the max days
        modes = {}
        for readable in max_days:
            modes[readable] = defaultdict(int)
            date, month, year = readable.split('-')
            year  = int(year) + 2000
            month = MONTHS[int(month)]
            date  = int(date)
            for time in self.data[yr][month][date]:
                mode = self.data[yr][month][date][time]
                modes[readable][mode] += 1

        return {
            'days': max_days,
            'maxFaps': max_faps,
            'modes': modes
        }



    def least_most_time_diff(self, type_:str='most') -> Union[List[tuple], int]:
        '''
        Returns the pair(s) of times with the least or most time difference (in minutes) between them
        [('01-01-2021 13:00', '01-01-2021 13:30'), ('01-01-2021 14:00', '01-01-2021 14:30')] , 30
        '''
        pairs     = []
        best_diff = float('inf') if type_ == 'least' else -float('inf')
        op        = gt if type_ == 'most' else lt  # If we want the most time difference, we use gt, else lt

        times = [
            datetime.strptime(f'{yr}-{MONTHS[month]}-{date} {time}', '%Y-%m-%d %H%M')
            for yr    in self.data
            for month in self.data[yr]
            for date  in self.data[yr][month]
            for time  in self.data[yr][month][date]
        ]
        
        last_time = None
        for curr_time in sorted(times):
            if last_time is not None:
                diff = (curr_time - last_time).total_seconds() // 60
                if op(diff, best_diff):
                    # If we found a new minimum or maximum difference
                    best_diff = diff
                    pairs     = [(last_time, curr_time)]
                elif diff == best_diff:
                    pairs.append((last_time, curr_time))
            last_time = curr_time
        
        # Convert pairs to 01-01-2021 13:00 format
        # pairs = [(p1.strftime('%d-%m-%Y %H:%M'), p2.strftime('%d-%m-%Y %H:%M')) for p1, p2 in pairs]
        pairs = [ {'start': p1.strftime('%d-%m-%Y %H:%M'), 'end': p2.strftime('%d-%m-%Y %H:%M')} for p1, p2 in pairs ]
        best_diff = timedelta(minutes=best_diff)
        best_diff = {
            'months':  best_diff.days // 30,
            'days':    best_diff.days % 30,
            'hours':   best_diff.seconds // 3600,
            'minutes': best_diff.seconds // 60 % 60
        }
        return {'pairs': pairs, 'bestDiff': best_diff}
        


    def modes_per_day(self):
        '''
        {
            '1/11/21': {
                'Imagination': 1,
                'Porn': 1,
                'Hentai: 0,
                'Manga': 0
            }
        }
        '''
        data = {}
        raw_data = self.data

        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    # key       = f'{date}/{MONTHS[month]}/{yr[-2:]}'
                    key       = f'{date}/{MONTHS[month]}/{yr%100}'
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



    def most_occuring_time_bins(self):
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
        raw_data = self.data

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
    



    def times_frequncies(self):
        '''
        {
            '0000': 5,
            '0100': 2,
            '0200': 0,
            '0300': 1,
            '0400': 1,
        '''
        counts   = defaultdict(int)
        raw_data = self.data
        for yr in raw_data:
            for month in raw_data[yr]:
                for date in raw_data[yr][month]:
                    for time in raw_data[yr][month][date]:
                        counts[time] += 1
        
        # Sort the dictionary by keys (times)
        return dict(sorted(counts.items(), key=lambda item: item[0]))



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
        raw_data = self.data
        
        for yr in raw_data:
            for month in raw_data[yr]:
                key       = f"{month}-{yr%100}"
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
        raw_data = self.data
        
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
        raw_data = self.data

        for yr in raw_data:
            for month in raw_data[yr]:
                key        = f"{month}-{yr%100}"
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
        