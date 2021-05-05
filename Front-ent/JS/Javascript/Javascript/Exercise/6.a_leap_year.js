var year = 2016

function check_a_leap_year(year){
  if ( (( year % 4 == 0 ) && ( year % 100 != 0 )) || ( year % 400 == 0 ) ){
    return year + " a leap year"
  }else{
    return year + " is not a lead year"
  }
}

function check_1(year){

}

console.log(check_a_leap_year(2016))
console.log(check_a_leap_year(2000))
console.log(check_a_leap_year(1700))
console.log(check_a_leap_year(1800))
console.log(check_a_leap_year(100))