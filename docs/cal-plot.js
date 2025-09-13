const calPlotsDiv       = document.getElementById('cal-plots');
const colorSchemeSelect = document.getElementById('colorScheme');
colorSchemeSelect.value = 'YlOrRd'; // Default color scheme



// Function to make the calplots fix their container width
function fixCalPlotsWidth(year) {
    const svg = document.querySelector(`#calplot-${year} svg`);

    const width  = svg.getAttribute('width');
    const height = svg.getAttribute('height');

    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.style.width   = '100%';
    svg.style.height  = 'auto';
    svg.style.display = 'block';
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
}








// Fetch and process data from data.json
fetch('data.json')
.then(response => response.json())
.then(data => {
    // year -> lists of objects {date, total, imagination, porn, hentai}
    const transformedData = {};
    const dateLookup = {}; // lookup object for faster access
    
    // Iterate through years
    for (const year in data) {
        transformedData[year] = []; // Initialize array for this year
        
        // Iterate through months
        for (const month in data[year]) {
            // Iterate through days
            for (const day in data[year][month]) {
                // Count the number of entries for this day
                const entries = data[year][month][day];
                const total = Object.keys(entries).length;
                
                if (total > 0) {
                    let imagination = 0, porn = 0, hentai = 0, manga = 0;
                    
                    // Count each type of entry
                    for (const time in entries) {
                        const type = entries[time];
                        if      (type === 'Imagination') imagination++;
                        else if (type === 'Porn')        porn++;
                        else if (type === 'Hentai')      hentai++;
                        else if (type === 'Manga')       manga++;
                    }

                    // Create a date string in YYYY-MM-DD format
                    const monthNum = new Date(`${month} 1, 2000`).getMonth() + 1;
                    const dateStr = `${year}-${monthNum.toString().padStart(2, '0')}-${day.padStart(2, '0')}`;
                    
                    const entry = {
                        date: dateStr,
                        total: total,
                        imagination: imagination,
                        porn: porn,
                        hentai: hentai,
                        manga: manga
                    };
                    
                    transformedData[year].push(entry);
                    dateLookup[dateStr] = entry; // Store in lookup object
                }
            }
        }
    }

    console.log(transformedData);
    maxFaps   = Math.max(...Object.values(transformedData).flat().map(entry => entry.total));
    startYear = Math.min(...Object.keys(transformedData).map(Number));
    endYear   = Math.max(...Object.keys(transformedData).map(Number));
    nYears    = endYear - startYear + 1;

    
    // Store calendar instances
    const calendars = {};

    // Function to create/update calendar for a year
    function createCalendar(year, colorScheme) {
        let yearDiv = document.createElement('div');
        yearDiv.className = 'cal-plot';
        yearDiv.id = `cal-plot-${year}`;
        yearDiv.innerHTML = `<h3>${year}</h3>
                             <div id="calplot-${year}" class="cal-plot-container"></div>
                             <div id="legend-${year}" class="cal-plot-legend"></div>`;

        calPlotsDiv.appendChild(yearDiv);

        // Create new calendar instance
        const cal = new CalHeatmap();
        calendars[year] = cal;

        cal.paint(
            {
                data: {
                    source: transformedData[year],
                    x: 'date',
                    y: 'total',
                },
                date: { start: new Date(year, 1, 1) },
                scale: {
                    color: {
                        type: 'quantize',
                        scheme: colorScheme,
                        domain: [0, maxFaps],
                    },
                },
                domain: { type: 'month'},
                range: 12,
                // subDomain: { type: 'day', radius: 2 },
                // // domain: { type: 'year' },
                // // range: nYears,
                // // subDomain: { type: 'day', radius: 2 },
                subDomain: { 
                    type: 'day',
                    radius: 2,
                    width: 12,
                    height: 12,
                    gutter: 2, // Space between the squares
                },
                itemSelector: `#calplot-${year}`,
            },
            [
                [
                    Tooltip,
                    {
                        text: function (date, value, dayjsDate) {
                            // 12 Sep '24
                            let dateStr = dayjsDate.format('DD MMM \'YY');
                            if (!value) return `No faps on ${dateStr}`;

                            // Use the lookup object for faster access
                            const key   = dayjsDate.format('YYYY-MM-DD');
                            const entry = dateLookup[key];
                            
                            let text = `${value} fap${value>1 ? 's' : ''} on ${dateStr} (`;
                            let modes = [];
                            if (entry.total === 1) {
                                modes = [entry.imagination ? `Imagination` : entry.porn ? 'Porn': entry.hentai ? 'Hentai' : 'Manga'];
                            }
                            else {
                                if (entry.imagination) modes.push(`Imagination: ${entry.imagination}`);
                                if (entry.porn)        modes.push(`Porn: ${entry.porn}`);
                                if (entry.manga)       modes.push(`Manga: ${entry.manga}`);
                                if (entry.hentai)      modes.push(`Hentai: ${entry.hentai}`);
                            }
                            text += modes.join(', ') + ')';

                            // console.log(`Tooltip for ${dateStr}: ${text}`);
                            return text;
                        },
                    },
                ],
                [
                    Legend,
                    {
                        tickSize: 0,
                        width: 200,
                        itemSelector: `#legend-${year}`,
                        label: 'Daily Faps',
                        includeBlank: true,
                        // labelFormat: function(value) {
                        //     return value === 0 ? '0' : value === maxFaps ? maxFaps.toString() : '';
                        // }
                    },
                ],
            ]
        )
        .then(() => {
            fixCalPlotsWidth(year);
            setCalPlotsTheme();
        });
    }

    // Create initial calendars
    for (let currYear = startYear; currYear <= endYear; currYear++) {
        createCalendar(currYear, 'YlOrRd');
    }

    // Handle color scheme changes
    colorSchemeSelect.addEventListener('change', function() {
        const newScheme = this.value;
        
        // Clear existing calendars
        calPlotsDiv.innerHTML = '';
        
        // Recreate calendars with new color scheme
        for (let currYear = startYear; currYear <= endYear; currYear++) {
            createCalendar(currYear, newScheme);
        }
    });
})
.catch(error => console.error('Error loading data:', error));


// const data = [
//     { date: '2012-01-01', value: 3 },
//     { date: '2012-01-02', value: 6 },
// ];

// const cal = new CalHeatmap();
// cal.paint({
//     data: { source: data, x: 'date', y: 'value' },
//     date: { start: new Date('2012-01-01') },
//     range: 1,
//     domain: { type: 'month' },
//     subDomain: { type: 'day', radius: 2 },
//     itemSelector: '#ex-wind',
// });

// // Navigation
// document.getElementById('prev').addEventListener('click', function (e) {
//     e.preventDefault();
//     cal.previous();
// });

// document.getElementById('next').addEventListener('click', function (e) {
//     e.preventDefault();
//     cal.next();
// });