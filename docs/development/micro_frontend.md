# Micro frontend applications

Tracardi uses micro application to interact with customers. Micro-apps are regular ReactJs, or Angular, or plain
Javascript apps that can be bundled into single javascript file and injected into the webpage.

We use a ReactJs template repo for new ReactJs app.

To start developing Micro Frontend App use the tracardi-uix-template on [http://github.com/tracardi/tracardi-uix-template](http://github.com/tracardi/tracardi-uix-template)

1. Goto [http://github.com/tracardi/tracardi-uix-template](http://github.com/tracardi/tracardi-uix-template)
2. Click button Use this template. __Big green button__ at the top right side of the screen. 
3. Enter the name of your repository

This will create a repo with files needed to start working on the app. Now its time to clone the repo and enter its
folder and type

`npm install`

This will install all the required dependencies.

!!! Tip
    If you would like to cooperate with other contributors on this app or want the repo to be part of Tracardi organization
    on the GitHub let us know (on
    our [Slack workspace](https://join.slack.com/t/tracardi/shared_invite/zt-10y7w0o9y-PmCBnK9qywchmd1~KIER2Q)). We will
    create a repo that you can fork.

## Source code

Now, let's inspect the repo folders and find out what we have here:

There are two main folders:

* __public__ - it holds the index.html file that you can use later for testing your micro-frontend-app
* __src__ - this is where is your code. We will inspect this folder further below

The other files are `package.js` and `README.md` with installation tips. 

!!! Tip
    
    Please edit the app name in package.js. 
    `{"name": "<name-widget>", ...}`

### Source folder

Inside `src` folder you will find a `index.js` file. This is where your app starts. Please change the 

```javascript
const widgetName = 'tracardi-uix-your-name'
```

to have the name of your app. 

Then there is `App.js`. This is the injected micro-frontend-app. Notice that it takes the domElement.

```javascript title="App.js"
import React from 'react';
import "regenerator-runtime/runtime";

function App({domElement}) {  // (1)

    const attribute = domElement.getAttribute("data-attribute1") || "I am test attribute"
    return <h1>"Hello world " + {attribute}</h1>

}

export default App;
```

1. Dom parameter used to read the configuration of the micro-frontend-app. The configuration will be filled in Tracardi and passed as data attributes.  

This is because we need some way to pass the parameters to the app. And it is done by defining them inside the dom elements like this.

```html title="This is the example form index.html"

<div class="tracardi-uix-your-name" data-attribute1="my-attribute1" data-attribute2="my-attribute1"></div>
<script src="widget/index.js"></script>
```

!!! Tip

    __Please notice__ that the class of the `div` must be the same as the application name defined in the `index.js` file. See below.

## Connecting the app container with the code

You will need to define __connection between the HTML and your app__. The `src/index.js` file is responsible for this.
It is done in `const widgetName = 'tracardi-uix-your-name'`
and `const widgetDivs = document.querySelectorAll('.'+widgetName)` line. You also need to reference this name
in `index.html`. See the class of a div.

=== "src/index.js"

    ```javascript 
    import React from 'react';
    import ReactDOM from 'react-dom';
    import App from './App';
    
    const widgetName = 'tracardi-uix-your-name'  // (1)
    const widgetDivs = document.querySelectorAll('.'+widgetName)
    
    widgetDivs.forEach(Div => {
        ReactDOM.render(
            <React.StrictMode>
                <App domElement={Div} />
            </React.StrictMode>,
            Div
        );
    })
    ```

    1. Your app placeholder class name. Please change it to yout app name and prefix it with: `tracardi-uix-`. This name must also be a class name for __div__ tag in `index.html`

=== "public/index.html"

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <!-- (1) -->
        <div class="tracardi-uix-your-name" data-attribute="my-attribute"></div> 
        <script src="../widget/index.js"></script>
    </body>
    </html>
    ```

    1. Class name of `div` must be the same as `widgetName` in __src/index.js__

## Building micro frontend app

When you are done, use `yarn build:widget` to generate the micro frontend JS file. The build operation should create
__index.js__ file in a __widget__ folder.

## Micro frontend app design

Most apps triggered on the customers pages are popup apps so make sure you use some popup canvas, or a
drawer where you place your app.

!!! Info

    We use material-ui for this but this is up to you how you handle it.

Here is a simple example of an App where we use [Snackbar](https://mui.com/material-ui/react-snackbar/#main-content)
from [material-ui](https://mui.com) to display content.



```javascript
import React, {useState} from 'react';
import Snackbar from '@mui/material/Snackbar';
import Box from "@mui/material/Box";
import {Button, Typography} from "@mui/material";

function App({domElement}) {

    const title = domElement.getAttribute("data-title") || null
    const message = domElement.getAttribute("data-message") || null
    const ctaLabel = domElement.getAttribute("data-cta-button") || null
    const ctaLink = domElement.getAttribute("data-cta-link") || null
    const cancelLabel = domElement.getAttribute("data-cancel-button") || null
    const vertical = domElement.getAttribute("data-vertical") || "bottom"
    const horizontal = domElement.getAttribute("data-horizontal") || "right"
    const autoHide = domElement.getAttribute("data-auto-hide") || "60000"
    const borderRadius = domElement.getAttribute("data-border-radius") || "2"
    const borderShadow = domElement.getAttribute("data-border-shadow") || "1"
    const minWidth = domElement.getAttribute("data-min-width") || "300"
    const maxWidth = domElement.getAttribute("data-max-width") || "500"

    const [open, setOpen] = useState(true)

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };

    return (
        <Snackbar open={open} autoHideDuration={autoHide}
                  onClose={handleClose}
                  anchorOrigin={{vertical, horizontal}}
        >
            <Box
                sx={{
                    bgcolor: 'background.paper',
                    boxShadow: parseInt(borderShadow),
                    borderRadius: parseInt(borderRadius),
                    p: 2,
                    minWidth: parseInt(minWidth),
                    maxWidth: parseInt(maxWidth)
                }}
            >
                <Box sx={{padding: 1}}>
                    {title && <Typography variant="h5" style={{color: "black"}}>{title}</Typography>}
                    {message && <Typography style={{color: "black"}}>{message}</Typography>}
                </Box>

                {ctaLabel && <Box sx={{
                    display: "flex",
                    justifyContent: "center",
                    padding: 1
                }}>
                    {ctaLabel && <Button variant={"contained"} href={ctaLink} style={{margin: "0 5px"}}>
                        {ctaLabel}
                    </Button>}
                    {cancelLabel && <Button variant={"outlined"} onClick={handleClose}>
                        {cancelLabel}
                    </Button>}
                </Box>}

            </Box>
        </Snackbar>
    );
}

export default App;
```

You can also use other overlays from material design like [modal](https://mui.com/material-ui/react-modal/),etc. If
material-ui is not your thing you may use any other library. It is your choice.

## Testing

You can also test the react app as regular app with `yarn start`. When the app is finished, you will have to bundle it and open
on the `index.html` in your browser and see if it loads.

### Testing bundled app file

First you will have to build the app with `yarn build:widget`. It will create
a __index.js__ file in __widget folder__. 

To test if your app works as micro-app paste the bundled file `widget/index.js` into a regular HTML page. 

!!! Tip 

    You do not have to create index.html by your self. We have one created for you in the repo in the
    public directory. It is called `index.html`. Paste the __script__ tag together with the configuration inside 
    the __body__ of the `index.html` and open the file. 

```html title="This is an example public/index.html from one of our micro-apps"
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    
    <!-- (1) -->
    <div class="tracardi-uix-cta-message"
         data-title="title"
         data-message="message"
         data-cta="visit" data-cancel=""
         data-auto-hide="50000"
    ></div>
    
    <!-- (2) -->
    <script src="../widget/index.js"></script>
  </body>
</html>
```

1. The app container with the configuration in data attributes. __Please notice__ that the class of the `div` must be
   the same as the application name defined in the `index.js` file.
2. The bundled app script

Now open the __index.html__ in the browser, and it should load your app and display it on top of the existing
index.html. If the index.html does not have any html then it will be empty as in our example.

## How Tracardi injects the app

Tracardi loads the app the same as we did it in the test example above. That means with a __script__ tag and a div
container. It appends the needed tags at the bottom of the page. Like this.

```html title="This is the example form index.html"

<div class="tracardi-uix-your-name" data-attribute="my-attribute"></div>
<script src="widget/index.js"></script>
```

## Passing data from Tracardi to micro app

The micro app may need configuration. For example the pop-up message app needs message and maybe location of the pop-up
window. To configure the app and pass data from Tracardi use `data attributes`. It can be done in `src/App.js`

=== "src/App.js"

    ```javascript
    import React from 'react';
    import "regenerator-runtime/runtime";  // (3)
    
    function App({domElement}) {
    
        const attribute1 = domElement.getAttribute("data-attribute-1") || "I am test attribute 1"  // (1)
        const attribute2 = domElement.getAttribute("data-attribute-2") || "I am test attribute 2"  // (2)
        return <h1>"Hello world " + {attribute}</h1>
    
    }
    
    export default App;
    
    ```

    1. This is your app input data. Read it like this, and then you can use `attribute1` variable in you app. See index.html on how to pass data.
    2. This is your app input data. Read it like this, and then you can use `attribute2` variable in you app.
    3. This import may be needed when you use async functions. See Trouble-shooting below.

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <div class="tracardi-uix-your-name" 
             data-attribute-1="my-attribute-1"
             data-attribute-2="my-attribute-2"></div>
        <script src="widget/index.js"></script>
    </body>
    </html>
    ```

## Troubleshooting

If you use async functions in your app (what is very probable) you may encounter the problem that the app does not build
when build with `yarn build:widget`. Then follow the tip below.

!!! Error "regeneratorRuntime is not defined error"

    When you see "__regeneratorRuntime is not defined__" that means you have to
    add `import "regenerator-runtime/runtime";` to your component.

