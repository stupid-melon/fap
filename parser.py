import json
from rich import print_json

MONTHS = {
    'JAN':  'January',
    'FEB':  'February',
    'MAR':  'March',
    'APR':  'April',
    'MAY':  'May',
    'JUN':  'June',
    'JUL':  'July',
    'JULY': 'July',
    'AUG':  'August',
    'SEP':  'September',
    'OCT':  'October',
    'NOV':  'November',
    'DEC':  'December',
}

MODES = {
    None: 'Imagination',
    'N':  'Imagination',
    'P':  'Porn',
    'H':  'Hentai',
    'M':  'Manga',
}




def get_val(string: str):
    val = None
    for i in string:
        if i.isalpha():
            val = i
    
    key = [i for i in string if not i.isalpha()]
    key = ''.join(key)
    key = key.replace(' ', '')

    return key, val     # key: "0300"  |  val: None/"P"






with open('docs/data.txt') as f:
    data_txt = f.read()


lines = data_txt.split('\n')
lines = [line.strip(' ') for line in lines]
lines = [line for line in lines if line]


data = {}

'''
key1: Year
key2: Month
key3: Date
key4: Time
val: Attribute, like P
'''

for line in lines:
    # If is a line where the month is defined
    if not ':' in line:
        key2, key1 = line.split('-')           # DEC-22 -> ["DEC", "22"]
        key2 = MONTHS[key2]                    # DEC    -> December
        key1 = f'20{key1}'                     # "22"   -> "2022"
        if not data.get(key1):                 # If this is the first time we are using the year, creates an empty dic to be filled
            data[key1]   = {}
        data[key1][key2] = {}
        continue
    
    key3, times = line.split(':')               # "23: 1300, 1645"  -> "23" & "1300, 1645"

    times = times.split(',')                    # "1300, 1645"      -> ["1300"," 1645"]
    times = [i.strip(' ') for i in times]       # ["1300"," 1645"]  -> ["1300","1645"]
    times = [] if times[0]=='-' else times

    data[key1][key2][key3] = {}
    
    for i in times:
        # i is like "2200 H"
        key4, val = get_val(i)
        val       = MODES[val]                  # "H" -> "Hentai"
        data[key1][key2][key3][key4] = val




# print_json(data=data)

# Deletes the last month of data cz its prolly incomplete
last_yr  = list(data.keys())[-1]
last_mon = list(data[last_yr].keys())[-1]
del data[last_yr][last_mon]

# Dumps the data
with open('docs/data.json', 'w') as f:
    json.dump(data, f, indent=2)


'''
{
    2022: {
        JAN: {
            1: {
                "0100": null,
                "1500": "P"
            }
        }
    }
}

'''

