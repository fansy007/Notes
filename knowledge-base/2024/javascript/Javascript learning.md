# data types
Number
String
Boolean
Undefined
Null
Symbol
BigInt

dynamic type, when define a varible, no need determine data type at once

# declare 变量
let -- means the value we can change lator
const -- define a value can not be changed, and you should give a const a value immediately when you define it
var -- we can avoid use this, it's old way

# Functions
```javascript
'use strict'
function fruiteMaker(apples,oranges) {
    const juice = `juice with ${apples} apples and ${oranges} oranges`;
    return juice;    
}

const sum = function(a,b) {
    return a+b;
}
console.log(sum(10,20));
```

## lamda function
```javascript
const sum2 = (a,b) => {
    return a+b;
}
console.log(sum2(10,20));
```

lamda function can't get a this scope

## use function as a param
```javascript
function fruiteMaker(apples, oranges,fun) {
    const juice = `juice with ${fun(apples)} apples pieces and ${fun(oranges)} oranges pieces`;
    return juice;
}

const cutFruitPieces = fruit => fruit * 4
const cutFruitPieces2 = fruit => fruit * 10

console.log(fruiteMaker(4,5,cutFruitPieces));
console.log(fruiteMaker(4,5,cutFruitPieces2));

```

 # Array
 ```javascript
const friends = ['Tom','Jack'];
const frieds2 = new Array("Lisa","Mary");
console.log(friends,frieds2);
```

```javascript
const friends = ['Tom','Jack'];
friends.push('Jay');
friends.unshift('Johnson');

// pop() -- pop last element, shift() pop first element
log(friends);
log(friends.indexOf('Tom'));
log(friends.includes('Jay'));
```

# Object
```javascript
const jonas = {
    fisstName: 'Jonas',
    lastName: 'Schmedtman',
    age: 2037-1991,
    job: 'teacher',
    friends: ['Micheal','Peter', 'Steven']
}
log(jonas['friends'][2]); // equals jonas.friends[2]
const nameKey ='lastName';
log(jonas[nameKey]);

const key = prompt('what do you want to know about jonas?');
if (jonas[key]==undefined) {
    log('no that property');
} else {
    log(jonas[key]);
}
```

	in javascript `` 中可以使用模版字符串${},""是不可以的

成员方法和this的使用
```javascript
const jonas = {
    fisstName: 'Jonas',
    lastName: 'Schmedtman',
    birthYear: 1991,
    job: 'teacher',
    friends: ['Micheal', 'Peter', 'Steven'],
    calcAge: function() {
        return 2037 - this.birthYear;
    }
}

log(jonas['calcAge']());
```

# CSS
class , id (id是唯一的，class可以复用)

```css
<head>
	<title>learning css</title>
	<link href="style.css" rel="stylesheet"/>    
</head>

------------------------------------------
* {
    margin: 0px;
    padding: 0px;
    box-sizing: border-box;

}

body {
    background-color: rgb(245, 223, 181);
    font-family: Arial;
    font-size: 14px;
    padding: 75px;
}

h1 {
    font-size: 40px;
    margin-bottom: 25px;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

.first {
    color: red;
}

#your-name {
    background-color: rgb(166, 201, 231);
    border: 5px solid #444;
    width: 400px;
    padding: 5px;
    margin-top: 25px;
}

p {
    margin-bottom: 20px;    
}

input,button {
    padding: 10px;
    font-size: 16px;
}

a {
    background-color: yellow;
}

#your-name h2 {
    background-color: olivedrab;
    border-radius: 10px;
    padding: 5px;
    transition: box-shadow 0.3s ease;
}

#your-name h2:hover {
    box-shadow: 0 6px 8px rgba(0,0,0,0.3);
    cursor: pointer;
}

#course-image {
    width: 200px;
}
```
to be coontinue 70...

# hidden show player

html
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <link rel="stylesheet" href="style.css" />
    <title>Modal window</title>
  </head>
  <body>
    <button class="show-modal">Show modal 1</button>
    <button class="show-modal">Show modal 2</button>
    <button class="show-modal">Show modal 3</button>

    <div class="modal hidden">
      <button class="close-modal">&times;</button>
      <h1>I'm a modal window 😍</h1>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </p>
    </div>
    <div class="overlay hidden"></div>
    <script src="script.js"></script>
  </body>
</html>

```

## css
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: inherit;
}

html {
  font-size: 62.5%;
  box-sizing: border-box;
}

body {
  font-family: sans-serif;
  color: #333;
  line-height: 1.5;
  height: 100vh;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: linear-gradient(to top left, #28b487, #7dd56f);
}

.show-modal {
  font-size: 2rem;
  font-weight: 600;
  padding: 1.75rem 3.5rem;
  margin: 5rem 2rem;
  border: none;
  background-color: #fff;
  color: #444;
  border-radius: 10rem;
  cursor: pointer;
}

.close-modal {
  position: absolute;
  top: 1.2rem;
  right: 2rem;
  font-size: 5rem;
  color: #333;
  cursor: pointer;
  border: none;
  background: none;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

p {
  font-size: 1.8rem;
}

/* -------------------------- */
/* CLASSES TO MAKE MODAL WORK */
.hidden {
  display: none;
}

.modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;

  background-color: white;
  padding: 6rem;
  border-radius: 5px;
  box-shadow: 0 3rem 5rem rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(3px);
  z-index: 5;
}

```

## js
```javascript
'use strict';
const log = function (msg) {
    console.log(msg);
}
const $ = document.querySelector.bind(document);
const $a = document.querySelectorAll.bind(document);
const model = $('.modal');
const overlay = $('.overlay');

const btnCloseModal = $('.close-modal');
const btnsOpenModal = $a('.show-modal');
log(btnsOpenModal);
for (let i = 0; i < btnsOpenModal.length; i++) {
    btnsOpenModal[i].addEventListener('click', function(event){
        log('clicked')
        model.classList.remove('hidden');
        overlay.classList.remove('hidden');
    });
}

btnCloseModal.addEventListener('click',function(event){
    model.classList.add('hidden');
    overlay.classList.add('hidden');
});

overlay.addEventListener('click', function(event){
    model.classList.add('hidden');
    overlay.classList.add('hidden');
});

document.addEventListener('keydown',function(event) {
    log(event);
    if(!model.classList.contains('hidden') && event.key=='Escape') {
        model.classList.add('hidden');
        overlay.classList.add('hidden');
    }
});

```

# dive into javascript

low level language -- manage resources manually
high level language -- auto manage resources, garbage collection

procdural programming
OOP
functional programming

prototyped-based object oriented language
![[Pasted image 20241119112645.png]]

first class functions -- function used as virable

dynamically typed language
no need assign a type for a virable, only @ execution time determine it
TS -- use types

Single-threaded 
None block event loop -- use this way to impl multi thread behavior

## JS engine

google: V8 Engine -> nodejs, chrome
![[Pasted image 20241119113332.png|425]]

Modern JS
compilation and interpreter language


Parse code into AST -> compilation AST code -> execution

![[Pasted image 20241119114006.png|725]]


JS engine, Web API
JS access WEB API through windows object

Callback queue (execute by event loop)
click, timer, data

# scope
global scope, function scope, block scope

only const, let is block scoped, var is function scoped
![[Pasted image 20241119154227.png|400]]
scopes has the access to variables from outside scope -- **variable lookup**

# this
>[!note]+ this points to the owner of the function

object method
this -> object called the method

simple function call
this -> undefined

arrow functions
this -> this of the surrounding function (lexical this)

event listener 
this -> Dom element attach to handler

this is not its variable environment

```javascript
const person = {
    year : 2000,
    callAge : function() {
        log(this.year);
    }
}
const lee = {
    year : 2017
}
lee['callAge'] = person.callAge;
lee.callAge();
```

const firstName='Mdtilda'; -- will not assign firstName to global windows object. So this variable is @ top level block scope only. but if use var, that belong to windows object

object will not create a block context, only function can

# primitives and objects

const friend = Object.assign({}, me);
类似于clone使两个object指向不同的对象。


这里的{}是指copy到一个空对象上，也可以copy到一个已有的对象，使这个对象保留原来的不同的对象

# arrays tips

## destructure arrays -- 
const categories = ['Italian','Organic','Pizzeria'];
const [c1,c2] = categories;

if the value no need can empty it like this:
const [c1,,c3] = categories;

can exchange values simplly:
[c1,c3] = [c3,c1]

set a default value:
const [p=1,q=1,r=1] = [8,9];
r will be set to 1 cos no value @ right array

## destructure objects

const {location:loc='', mainMenu} = restaurant;

mutate values:
let a = 100;
let b = 200;
const obj = {a:7,b:8};
({a,b}=obj); -- a, b will be set as 7, 8

can also nested into sub object:

const {openingHours:{fri:{open:a,close:b}}} = restaurant;
log.console(a,b); -- we will populate value into virable a,b

## use destructor as a function param
so there also can setup a default value, for a destruct object

const show = function({name='unknown',age=1}) {
	console.log(name,age);
}

const jonas = {
	name: 'jonas'
}

show(jonas);

# spread operator
...array is to make array extract as elements one by one
can be used for all iterables -- arrays, strings, map, set, object properties
```javascript
const arr1 = [7,8,9];
const arr2 = [1,2,...arr1];

const objCopy = {...obj};
```


collect values back to an array
```javascript
const [a, ...myArry] = [1,2,3]; -- myArry get [2,3] 
```

collect values into array as function parameter
```javascript
const sum = function(...args) {
	let total = 0;
	for(let i=0;i<args.length;i++) {
		total +=args[i];
	}
	return total;
}


```

# for loops
```javascript
({startMenu,mainMenu}=restaurant);
for (let [index, item] of  [...startMenu,...mainMenu].entries ) {
  console.log(index, item);
}
```

# Object modern operators

?. can be used to avoid null property, instead return undefined
```javascript
console.log(restaurant?.openingHours?.thu?.open)
```

?. can also apply to object's function

```javascript
restaurant?.oderPasta('tomato','potato');
```

# loop object

use Object.keys(obj), Object.values(obj), Object.entries(obj) to loop an object

```javascript
for(let item: Object.keys(restaurant.openingHours)) {
	log(item)
}


```

# Set, Map
const mySet = new Set([1,1,2,3]);

const rest = new Map();
rest.set(1,'xxx');
rest.get(1);
rest.delete(1);

convert to a map
```javascript
const question = new Map([['question1', 'what's the most useful language'],[1,'C']]);

const hours = new Map(Object.entries(restaurant.openingHours));

for(const [key,value] of hours) {
	console.log(key,value);
}
```

object vs map
to deal with key value data structures

deal with json, mostly using object directly

# String

slice is similar to java function subString
```javascript
console.log(airline.slice(airline.indexOf('Air'), airline.lastIndexOf(' ')));
```

# function
```javascript
const bookings = [];
const createBooking = function (flighNum, numPassengers=1,price=1) {
    const booking = {
        flighNum,
        numPassengers,
        price
    };

    log(booking);
    bookings.push(booking);
}

createBooking('LH123', undefined ,100);
```

function is just one type of object
higher level function -- callback function

function that return new function

A function return a function
```javascript
const greet = function(greet) {
    return function(name) {
        console.log(`${greet} ${name}`);
    };
};

const greetHey = greet('Hey');
greetHey('Jonas'); // greet('Hey').('Jonas')
```

the same as
```javascript
const greetFun = greet => name=> console.log(`${greet} ${name}`);
greetFun('Hey')('Tom');
```

## bind call apply
```javascript
const lufthansa = {
    airline: 'Lufthansa',
    iatacode: 'LH',
    bookings: [],
    book(flightName, name) {
        log(`flightName: ${flightName}, iatacode:${this.iatacode}, name:${name}`);
    }
}

const eurowings = {
    airline: 'Eurowings',
    iatacode: 'EW',
    bookings: []
}
const book = lufthansa.book.bind(eurowings);
book('flight009','Tom');

lufthansa.book.call(eurowings,'flight009','Tom');
lufthansa.book.apply(eurowings,['flight009','Tom']);
```

# closure
```javascript
const secureBooking = function () {
    let passengerCount = 0;

    return function() {
        passengerCount ++;
        log(`${passengerCount} passengers`);
    }
}

const booker = secureBooking();``
booker();booker();booker();
```

变量passengerCount 属于secureBooking函数，当secureBooking执行完了，这个变量依然存在，被传出来的函数使用，这个机制被称为closure。

A closure give a function access to a variable of its parent function. Even after parent function already executed, destroyed.

sample2

internal call back function execute waiting seconds
```javascript
const boardPassengers = function(n, waiting) {
    const perGroup = n/3;
    setTimeout(function(){
        console.log(`We are now boarding all ${n} pasengers`)
        console.log(`There are 3 groups, each with ${perGroup} passengers`);

    }, waiting*1000);

    console.log(`will start boarding in ${waiting} seconds`);

}

boardPassengers(1000,5);
```

# DOM
![[Pasted image 20241121173041.png]]

- 187待续

