var today = new Date();
var day_in_current_month = today.getTime();

if (today.getMonth() == 11 && today.getDate() > 25){
    var year = today.getFullYear() + 1
}else{
    var year = today.getFullYear()
}

var next_christmas = new Date(year, 11, 25)
var one_day = 1000*60*60*24;

var time_from_today_to_next_xmas = Math.ceil((next_christmas.getTime() - today.getTime())/one_day);

console.log(time_from_today_to_next_xmas)