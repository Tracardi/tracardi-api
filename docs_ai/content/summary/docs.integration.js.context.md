The documentation text provides information about how to configure the context data in Tracardi, which is used to pass
additional information such as browser metadata, system variables, etc. It is configured on the tracker level and will
be attached to each event. The context data consists of browser data, screen data, page data, cookies, and local storage
data. It is possible to extend the context data with performance metrics, which will be sent as event context.
Additionally, the tracking script has the capability to include the current profile ID, session ID, and source ID in the
URL parameter, allowing for consistent profile ID persistence across domains that utilize the same Tracardi system. This
feature is available from version 0.8.1 up. It is also possible to respect the Do Not Track (DNT) browser setting, which
will prevent the tracking script from loading if the user sets DNT. To enable this functionality, you can add
the `respectDoNotTrack: true` setting in the tracker options.