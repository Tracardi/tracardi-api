# What are event options, how the impact triggering of events from javascript?

## Introduction

This documentation is designed to clarify the concept of event options and their influence on event triggering within
JavaScript. When working with a JavaScript snippet on your webpage, you have the capability to dispatch events using
the `window.tracker.track` method, and these events can be tailored by employing a range of options. The documentation
offers insight into different event types and the options associated with each.

## Event Triggering in JavaScript

In JavaScript, you can trigger events using the following syntax:

```javascript
window.tracker.track(<event-type>, <properties>, <options>)
```

Here, `<event-type>` represents the type of event you want to trigger, `<properties>` define the specific event
properties, and `<options>` configure how the event is triggered.

## Available Event Types

### 1. Collected

The "Collected" event type is the default setting, and events of this type are collected and sent in bulk when the page
finishes loading. This type of event does not require any specific options. The default settings for "Collected" events
are as follows:

```json
{
  "fire": false,
  "asBeacon": false
}
```

### 2. Fired Immediately

The "Fired Immediately" event type sends the event immediately without waiting for the page to finish loading. This is
particularly useful for events triggered by user interactions like clicks or mouseovers. To use this type, set the
following option:

```json
{
  "fire": true
}
```

### 3. Fired Even if the Page is Unloaded

In some cases, an event needs to be sent even when a user clicks a link and gets redirected to another page. This
scenario may prevent the script from executing, but you can ensure the event is sent using the following option:

```json
{
  "asBeacon": true
}
```

### 4. Process Event Async on the Server

By default, the commercial installation of Tracardi processes events asynchronously on the server. However, the
open-source version sends events synchronously, meaning the server must complete event processing before sending a
response. In certain cases, you may need to switch from asynchronous to synchronous processing, such as when you require
the event to return data or a widget to be presented on the page. To enable synchronous processing, use the following
option:

```json
{
  "async": false
}
```
