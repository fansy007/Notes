# tools
Prettier (code formatter)
set default formatter -> prettier @ vscode settings
set format on save -> check box of it
set autosave -> onFocus change
set tab size -> 2

## other plugin
image preview
color highlight
auto rename tag. -- in setting -> auto close tag (open this)

# center the page
```javascript
.container {
  width: 800px;
  margin-left: auto;
  margin-right: auto;  // the same as -- margin: 0px auto;
}
```

# box display
inline box -- only occupy the width they need, not occupy height

block box -- occupy the whole line, will change line for next element

display: block
display: inline

inline-block, will works as inline, but can occupy height
img is default inline-block element

```javascript
nav a:link {
  background-color: orangered;
  display: inline-block;
  margin-right: 30px;
  margin-top: 10px;
}
nav a:link:last-child {
  margin-right: 0px;
  background-color: #fff;
}
```

39 to be continue...

# absolute position
set the mother container relative,
set it self absolute
![[Pasted image 20241203101402.png]]

# pseudo element
h1::first-letter(pseudo element)
h1:first-child (pseudo class)


```javascript
h3 + p::first-line { // + will pick next sibling element
  color: red;
}
```


::after put at the last child of parent
::before put at the first of parent
```javascript
h2::after {
  content: "TOP";
  background-color: yellow;
  font-size: 16px;
  font-weight: bold;
  display: inline-block;
  padding: 5px 10px;
  position: absolute;
  right: 0px;
  top: -10px;
}
```

# good website
MDN
html validator online -- html validator web page
code pen
diff checker

# !!layout
page layout
component layout

float layout -- old
flexbox -- new 1 dimensional grid
css grid -- new 2 dimensional grid

## old style float
float will not occupy space
```javascript
article {
  background-color: green;
  width: 825px;
  float: left;
}

aside {
  background-color: red;
  width: 300px;
  float: right;
}

footer {
  background-color: yellow;
  clear: float;
}
```

# flex
main axis -- horizental
cross axis -- vertical

aligh items one to another inside a container
vertical centering -- justify-content: center;
horisental center -- align-items: center;

```javascript
      .container {
        /* STARTER */
        font-family: sans-serif;
        background-color: #ddd;
        font-size: 30px;
        margin: 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;

        /* FLEXBOX */
      }
```
![[Pasted image 20241203154530.png|950]]

# CSS grid
![[Pasted image 20241224145617.png]]

![[Pasted image 20241224145822.png]]

![[Pasted image 20241224150019.png]]



100px
1fr -- occupy the space by percentage (frations)

grid-template-columns: repeat(3,1fr)
grid-template-columns: 1fr 1fr 1fr

# design
typography
make text beautiful and easy to read

serif vs sans-serif
![[Pasted image 20241225100343.png|350]]

good and popular typeface, some popular sans-serif types
limit your page of font < 2 

![[Pasted image 20241225102256.png]]

![[Pasted image 20241225102730.png]]

size and wright
normal text: use font size 16-32px 
long text: 20px+

headline: 50px+ and bold 600+, exp --
85px, 700

less than 75 characters per line

line height 1.5 - 2 for normal, big text <1.5

letter sapcing -3.5px for big text

small title with capitals and bold big spacing

never align text @ center, always left align

## fonts.google.com

title 

h1 {
 font-size:44px;
 line-height:1.1;
 letter-spacing: -1px;
 }

# color
choose the right color
match your website's personality, color convey meaning

![[Pasted image 20241225110033.png|500]]
TOOLS:
Open color
tailwindcss

use a main color, a grey color (a drk version of another color, not really grey)
secondary color (related with your main color)
create lighter and darker versions (tints and shades) -- palleton.com, coolors

![[Pasted image 20241225110442.png|500]]


use main color to draw attension elements -- for exp: button
use colors to add interesting accents and to make section stand out
use colors strategicallty in images and illustrations

use a tint of the background ("lighter version")

lighter the color of black of text
don't make text too light, check contrast between text and background colors -- coolors
![[Pasted image 20241225111853.png|600]]

## yeun.github.io/open-color

# images
product photos
story telling photos -- choose someone using the product
illustrations -- a more abstract way to telling stories
patterns -- add behind an image

you should only use relevant images --
unsplash

to show real people to trigger people's emotions

crop images to fit your message

darker or  brightening image for writing text

position text into neutral image area

original image should be 2x as big as display size

squoosh the image size

when using multiple images, make those the same dimensions

# icons
phosphor icons
never mix icon packs
only use svg icons (vector based, can be scaled)

adjust to webside personality, roundness, weight depend on typography
provide visual assistance to text

icon + text combination
used as bullet points

.feature-icon {
	stroke: #087f5b;
	 width: 32px;
	 height:32px;
}

# shadows
use shadows in small doses -- if all elements with shadows, then that's no difference with no shadows
don't make shadows too dark
use small shadows for standout elements
```css
.chair-box {
  padding: 24px;
  box-shadow: 0px 20px 30px 0px rgba(0, 0, 0, 0.3); // 左右 上下 模糊度 拓展 颜色和透明度
}
```

# border radius

more fun, less serious

use radius @ -- buttons, images, around icons, standout sections
```css
img {
  width: 100%;
  border-radius: 12px;
  border-bottom-left-radius: 0px;
}
```

# white space
# visual hierarchy
draw attention to the most important elements
defining a path guild user through the page

position important elements closer to the top of the page where they get more attention
use image mindfully as they draw a lot attention
use whitespace strategically to emphasize elements
font size, weight, whitespace, color for text to convey importance
titles, subtitles, links,buttons,data points,icons

emphasize component by background colors, shadow, border
de-emphasize component B to show importance of component A

# UX
user experience

use patterns users know
make the call action button the most prominent element, make text descriptive
blue text and underline text only for links
animations should have a purpose and fast
offer user good feedback for all actions: errors, form success
place action button where they will create an effect

use a very descriptive keyword focused headline on the main page
cutoff fluff and make the content 100% clear
use simple words
break up long words with sub-headings,images,block quotes,bullet points etc


# Personality

## serious/elegant
![[Pasted image 20241226100015.png]]

## minimalist/simple
![[Pasted image 20241226100306.png]]

![[Pasted image 20241226100348.png|500]]

## plain/neutral
![[Pasted image 20241226100535.png]]

## bold/confident
![[Pasted image 20241226100740.png]]

## calm peaceful
![[Pasted image 20241226100933.png]]

## startup unbeat
![[Pasted image 20241226101223.png]]
![[Pasted image 20241226101347.png|475]]
## playful fun
![[Pasted image 20241226101515.png|800]]
![[Pasted image 20241226101619.png|500]]
# summarize the styles
![[Pasted image 20241226101933.png]]

# good resource
land-book
awwwards
screenlane

inspiring by above pages, and the one fit for yours

# from element to webpage

![[Pasted image 20241226104124.png]]

1. use common elements and comonents to convey your website's infomation
2. combine components into layouts using layout patterns
3. assemble different layout into webpage

![[Pasted image 20241226104446.png]]
