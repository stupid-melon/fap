// // Original data
// const rawData = {
//     "01-01-2024": 7,
//     "02-01-2024": 10,
// };

// // Like  { date: '2012-01-01', value: 3 },
// const rawData2 = [
//     { date: '2024-01-01', value: 7 },
//     { date: '2024-01-02', value: 10 },
// ];

// // Convert to timestamp-based data
// const parsedData = {};
// for (const date in rawData) {
//     const [day, month, year] = date.split('/');
//    // const ts = new Date(`${year}-${month}-${day}`).getTime() / 1000; // Unix timestamp in seconds
//    const ts = dayjs(`${date}`, "DD/MM/YYYY").unix(); // returns seconds
//
//     parsedData[ts] = rawData[date];
// }
// console.log(parsedData);




// Fetch and process data from data.json
fetch('data.json')
.then(response => response.json())
.then(data => {
    // Transform the nested data structure into an array of {date, value} objects
    const transformedData = [];
    const dateLookup = {}; // New lookup object for faster access
    
    // Iterate through years
    for (const year in data) {
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
                    
                    transformedData.push(entry);
                    dateLookup[dateStr] = entry; // Store in lookup object
                }
            }
        }
    }

    console.log(transformedData);
    maxFaps   = Math.max(...transformedData.map(entry => entry.total));
    startYear = Math.min(...transformedData.map(entry => new Date(entry.date).getFullYear()));
    endYear   = Math.max(...transformedData.map(entry => new Date(entry.date).getFullYear()));
    nYears    = Math.max(...transformedData.map(entry => new Date(entry.date).getFullYear())) - startYear + 1;

    for (let currYear = startYear; currYear <= endYear; currYear++) {
        console.log(`Year ${currYear}: ${transformedData.filter(entry => new Date(entry.date).getFullYear() === currYear).length} entries`);
    }

    // Initialize and render the calendar heatmap
    const cal = new CalHeatmap();
    cal.paint(
        {
            data: {
                source: transformedData,
                x: 'date',
                y: 'total',
            },
            date: { start: new Date(startYear+1, 0, 1) }, // For some reason the +1 is necessary
            scale: {
                color: {
                    type: 'quantize',
                    scheme: 'Oranges',
                    domain: [0, maxFaps],
                },
            },
            // domain: { type: 'month' },
            // range: 12,
            // subDomain: { type: 'day', radius: 2 },
            domain: { type: 'year' },
            range: nYears,
            subDomain: { type: 'day', radius: 2 },
            itemSelector: '#ex-wind',
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

                        return text;
                    },
                },
            ],
            [
                Legend,
                {
                    tickSize: 0,
                    width: 100,
                    itemSelector: '#ex-wind-legend',
                    label: 'Daily Faps',
                },
            ],
        ]
    );
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