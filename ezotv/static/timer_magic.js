countdown.setLabels(
        '| másodperce| perce| órája| napja|| hónapja| éve|||',
        '| másodperce| perce| órája| napja|| hónapja| éve|||',
        ' és ',
        ', ',
        'most!');
        


var timerlist = []; // <- very important list
var player_info_cols = document.getElementsByClassName("player_info");

// Discover stuff to tick
for (var i = 0; i < player_info_cols.length; i++) {
   timerlist.push({
        date: new Date(player_info_cols[i].getAttribute("data-last-seen")), 
        target: player_info_cols[i]
   });
}

// Start timers

window.setInterval(function() {
        for (var i = 0; i < timerlist.length; i++) {
                var ts = countdown(timerlist[i].date, null ,countdown.YEARS|countdown.MONTHS|countdown.DAYS|countdown.HOURS|countdown.MINUTES|countdown.SECONDS, 2);
                timerlist[i].target.innerHTML = ts.toHTML();
                delete ts;
        }
} , 1000);


