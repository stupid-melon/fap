fetch('data/data.txt')
.then(response => response.text())
.then(data => {
    let pre = document.getElementById('raw_data');
    pre.textContent = data;
});


function formatTimeDiff(diff) {
    let years   = diff.years;
    let months  = diff.months;
    let days    = diff.days;
    let hours   = diff.hours;
    let minutes = diff.minutes;
    
    let toJoin = [];
    if (years > 0)   toJoin.push(years   + ' year'  + (years > 1 ? 's' : ''));
    if (months > 0)  toJoin.push(months  + ' month' + (months > 1 ? 's' : ''));
    if (days > 0)    toJoin.push(days    + ' day'   + (days   > 1 ? 's' : ''));
    if (hours > 0)   toJoin.push(hours   + ' hour'  + (hours  > 1 ? 's' : ''));
    if (minutes > 0) toJoin.push(minutes + ' minute' + (minutes > 1 ? 's' : ''));

    if (toJoin.length === 0) {return '0 days';}
    if (toJoin.length === 1) {return toJoin[0];}
    if (toJoin.length === 2) {return toJoin.join(' and ');}

    return toJoin.slice(0, -1).join(', ') + ', and ' + toJoin[toJoin.length - 1];
}



function formatDate(dateString) {
    // // 16-08-2022 -> 16 Aug 2022
    // return dayjs(dateString, 'DD-MM-YYYY').format('DD MMM YYYY');
    // 16-08-2022 -> 16 Aug'22
    return dayjs(dateString, 'DD-MM-YYYY').format("DD MMM'YY");
}

function formatTiming(timingString) {
    // 16-08-2022 19:30 -> 16 Aug'22 7:30pm
    return dayjs(timingString, 'DD-MM-YYYY HH:mm').format("DD MMM'YY h:mma");
}

function formatModes(modes) {
    let modeStrings = [];
    for (const [mode, count] of Object.entries(modes)) {
        modeStrings.push(`${mode}: ${count}`);
    }
    return modeStrings.join(', ');
}



fetch('data/stats.json')
.then(response => response.json())
.then(data => {
    document.getElementById('total-faps').textContent             = data.totalFaps;    
    document.getElementById('total-time-diff').textContent        = formatTimeDiff(data.timeDiff);
    document.getElementById('avg-per-day').textContent            = data.avgPerDay;
    document.getElementById('n-days').textContent                 = data.nDays;
    document.getElementById('active-days').textContent            = data.activeDays;
    document.getElementById('active-days-percentage').textContent = Math.round((data.activeDays / data.nDays) * 100) + '%';

    document.getElementById('longest-fap-streak').textContent         = data.longestFapStreak.maxStreak;
    document.getElementById('longest-fap-streak-start').textContent   = formatDate(data.longestFapStreak.pairs[0].start);
    document.getElementById('longest-fap-streak-end').textContent     = formatDate(data.longestFapStreak.pairs[0].end);
    document.getElementById('longest-nofap-streak').textContent       = data.longestNofapStreak.maxStreak;
    document.getElementById('longest-nofap-streak-start').textContent = formatDate(data.longestNofapStreak.pairs[0].start);
    document.getElementById('longest-nofap-streak-end').textContent   = formatDate(data.longestNofapStreak.pairs[0].end);

    document.getElementById('most-faps-in-a-day').textContent      = data.mostDay.maxFaps + ' (' + formatModes(data.mostDay.modes[data.mostDay.days[0]]) + ')';
    document.getElementById('most-faps-in-a-day-date').textContent = formatDate(data.mostDay.days[0]);
    
    document.getElementById('least-time-diff').textContent          = formatTimeDiff(data.leastTimeDiff.bestDiff);
    document.getElementById('least-time-diff-timing-1').textContent = formatTiming(data.leastTimeDiff.pairs[0].start);
    document.getElementById('least-time-diff-timing-2').textContent = formatTiming(data.leastTimeDiff.pairs[0].end);
    
    document.getElementById('most-time-diff').textContent          = formatTimeDiff(data.mostTimeDiff.bestDiff);
    document.getElementById('most-time-diff-timing-1').textContent = formatTiming(data.mostTimeDiff.pairs[0].start);
    document.getElementById('most-time-diff-timing-2').textContent = formatTiming(data.mostTimeDiff.pairs[0].end);
});



// Hologram glow effect for #introductory-info
const introInfo = document.getElementById('introductory-info');
if (introInfo) {
    introInfo.addEventListener('mousemove', function(e) {
        const rect = introInfo.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        introInfo.style.setProperty('--holo-x', `${x}%`);
        introInfo.style.setProperty('--holo-y', `${y}%`);
    });
}



// Banner management
function dismissBanner(bannerId) {
    document.getElementById(bannerId).classList.add('hidden');
    localStorage.setItem(`banner-${bannerId}-dismissed`, 'true');
}


// Check for previously dismissed banners on page load
function checkDismissedBanners() {
    const banners = ['mobile-warning', 'hover-info'];
    banners.forEach(bannerId => {
        const isDismissed = localStorage.getItem(`banner-${bannerId}-dismissed`) === 'true';
        console.log(`Banner ${bannerId} dismissed: ${isDismissed}`);
        if (!isDismissed) {document.getElementById(bannerId).classList.remove('hidden');}
    });
}




// Initialize dismissed banners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    checkDismissedBanners();
});



