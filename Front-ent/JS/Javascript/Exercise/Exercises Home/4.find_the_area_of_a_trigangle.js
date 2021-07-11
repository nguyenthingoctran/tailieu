// Write a JavaScript program to find the area of a triangle where lengths of the three of its sides are 5, 6, 7. 
var side_1 = 5
var side_2 = 6
var side_3 = 7

var p = (side_1 + side_2 + side_3)/2
var s = Math.sqrt(p*(p-side_1)*(p-side_2)*(p-side_3))

console.log(s)