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
![[Pasted image 20241203154530.png|600]]

to be continue 58 CSS grid