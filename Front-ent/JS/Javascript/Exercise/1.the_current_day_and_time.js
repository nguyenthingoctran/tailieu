// Write a JavaScript program to display the current day and time in the following format.
// Sample Output : Today is : Tuesday.
// Current time is : 10 PM : 30 : 38

function weekdays(weekday) {
  switch (weekday) {
    case 0:
      return "Sunday"
    case 1:
      return "Monday"
    case 2:
      return "Tuesday"
    case 3:
      return "Thursday"
    case 4:
      return "Wednesday"
    case 5:
      return "Friday"
    default: return "Saturday"
  }
}

function get_hours(hours){
  if (hours > 12){
    return (hours - 12)+"PM"
  }else{
    return hours+"AM"
  }
}

var newDate = new Date();

var date = newDate.getDay();
var is_weedays = weekdays(date);

var hours = newDate.getHours();

console.log('Today is : '+ is_weedays +'.')
console.log('Current time is : '+ get_hours(hours) +' : 30 : 38')