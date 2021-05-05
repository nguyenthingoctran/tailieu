// Write a JavaScript program to get the current date.
var date = new Date();
var dd = date.getDate();
var mm = date.getMonth();
var yyyy = date.getFullYear();

function add_zero(number){
  if ( number < 10 ) {
    return "0" + number
  }else{
    return number
  }
}

console.log(add_zero(dd) + "-" + add_zero(mm) + '-' + yyyy);
console.log(add_zero(dd) + "/" + add_zero(mm) + '/' + yyyy);
