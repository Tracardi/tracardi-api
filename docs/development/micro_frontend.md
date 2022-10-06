# Micro frontend applications

Tracardi uses micro application to interact with customers. Micro-apps are regular ReactJs, or Angular, or plain
Javascript apps that can be bundled into single javascript file and injected into the webpage.

We use a ReactJs template repo for new ReactJs app.

To start developing Micro Frontend App use the tracardi-uix-template on http://github.com/tracardi/tracardi-uix-template

1. Goto http://github.com/tracardi/tracardi-uix-template
2. Click button Use this template
3. Enter the name of your repository

This will create a repo with files needed to start working on the app.

If you would like to cooperate with other contributors on this app or want the repo to be part of Tracardi organization
on the github let us know (on
our [Slack workspace](https://join.slack.com/t/tracardi/shared_invite/zt-10y7w0o9y-PmCBnK9qywchmd1~KIER2Q)). We will
create a repo that you can fork.

## Building micro frontend app

Once you have repo cloned create a regular react js component in the root src folder, import it in the App.js folder to
see the changes. Most apps triggered on the customers pages are popup apps so make sure you use some popup canvas, or a
drawer where you place your app.

!!! Info

    We use material-ui for this but this is up to you how you handle it.

When you are done, use yarn `build:widget` to generate the micro frontend JS file. The build operation should create
index.js file in a widget folder.

You can test if your app works by pasting it into a regular HTML page. We have one create for you in the repo in the
root directory. It is called `index.html`.

## How Tracardi injects the app

Tracardi loads the app with __script__ tag and appends the needed tag at the bottom of the page. Like this.

```html title="This is the example form index.html"

<div class="tracardi-uix-your-name" data-attribute="my-attribute"></div>
<script src="widget/index.js"></script>
```

!!! Info "Notice the class attribute and data attributes"

    You need to define the class attribute for your app container tag. By this attribute the app finds out when to embed 
    the app. Data attributes are used to inject data into app.

You will need to define the application placeholder. It is done in `src/index.js` file and referenced in `index.html`
when the app s loaded.

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

    1. Your app placeholder class name. Please change it for app name and prefix it with: `tracardi-uix-`. This name is a clann name for __div__ tag in `index.html`

=== "index.html"

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <div class="tracardi-uix-your-name" data-attribute="my-attribute"></div>
        <script src="widget/index.js"></script>
    </body>
    </html>
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

## Testing the app

You can test the app as regular app with `yarn start`. When it is finished, and you have bundled widget file; open
the `index.html` in your browser and see if it loads.

## Trouble-shooting

If you use async functions in your app (what is very probable) you may encounter the problem that the app does not build
when build with `yarn build:widget`. Then follow the tip below.

!!! Error "regeneratorRuntime is not defined error"

    When you see "__regeneratorRuntime is not defined__" that means you have to
    add `import "regenerator-runtime/runtime";` to your component.

