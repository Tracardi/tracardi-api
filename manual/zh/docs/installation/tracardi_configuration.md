# Tracardi configuration

Tracardi configuration is performed via environment variables. You might want to use environment variables to change the
default system configuration, especially if you intend to run Tracardi inside a Docker container. You can find the list
of all the environment variable names below.

## Elastic configuration

* `ELASTIC_HOST` - Default: 127.0.0.1. This setting defines a IP address of elastic search instance.
  See `Connecting to elastic cluster` for more information how to connect to a cluster of servers.
* `ELASTIC_SNIFF_ON_START` - Default: None. When you enable this option, the client will attempt to execute an
  elasitcsearch sniff request during the client initialization or first usage. Search documentation for sniffing to get
  more information.
* `ELASTIC_SNIFF_ON_CONNECTION_FAIL` - Default: None. If you enable this option, the client will attempt to execute a
  sniff request every time a node is faulty, which means a broken connection or a dead node.
* `ELASTIC_SNIFFER_TIMEOUT` - Default: None, Time out for sniff operation.
* `ELASTIC_HTTP_AUTH_USERNAME` - Default: None. Elastic search username. Search for elastic authentication for more
  information on how to configure connection to elastic.
* `ELASTIC_HTTP_AUTH_PASSWORD` - Default: None. Elastic search password. Search for elastic authentication for more
  information on how to configure connection to elastic.
* `ELASTIC_SCHEME` - Default: http. Available options http, https.
* `ELASTIC_CAFILE` - Default: None. Elastic CA file. Search for elastic authentication for more information on how to
  configure connection to elastic.
* `ELASTIC_API_KEY` - Default: None. Elastic API key. Search for elastic authentication for more information on how to
  configure connection to elastic.
* `ELASTIC_CLOUD_ID` - Default: None. Search for elastic authentication for more information on how to configure
  connection to elastic.
* `ELASTIC_MAX_CONN` - Default: None. Defines max connection to elastic cluster. It defaults to elastic default value.
* `ELASTIC_HTTP_COMPRESS`- default value: None. Set compression on data when the client calls the server.
* `ELASTIC_VERIFY_CERTS` - default value: None. Verify certificates when https schema is set. Set it to no if
  certificates has no CA.
* `ELASTIC_REFRESH_PROFILES_AFTER_SAVE` - Default: no. When set to yes profile index will be forced to refresh its data
  after each update. That means that elastic will write all updates without buffering. This may slow the elastic
  significantly so be cautious with this setting.
* `INSTANCE_PREFIX` - Default: None. It defines prefix for all elastic indexes. This can be used to run multiple
  instances of Tracardi on one elastic instance.
* `ELASTIC_LOGGING_LEVEL` - Default WARNING. Sets logging level of elastic requests. It may be useful to set it to INFO
  when debugging Tracardi.

## API settings

* `USER_NAME` - Default: admin. Login to Tracardi API
* `PASSWORD` - Default: admin. Password to Tracardi API
* `DEBUG_MAKE_SLOWER_RESPONSES` - Default: 0. This variable is for testing purposes only. It sets the number of seconds
  each endpoint should be slowed in order to see the GUI responses.
* `AUTOLOAD_PAGE_SIZE` - Default: 25. Chunks of data that are loaded with one request.
* `EXPOSE_GUI_API` - Default: yes. It exposes the GUI API on the started Tracardi API instance. Available only in
  commercial version of Tracardi.

## Plugins settings

* `RESET_PLUGINS` - Default: no. If set to yes it will remove plugins index with every start of Tracardi instance. This
  setting is used in development mode only.
* `UPDATE_PLUGINS_ON_STARTUP` - Default: no. If equals `yes` it will update all installed plugins on Tracardi start.

## Cache settings

* `REDIS_HOST` - Default: redis://localhost:6379. This setting is used only when `SYNC_PROFILE_TRACKS` is equal to yes.
  This is the host URI of Redis instance that is required to synchronize profile tracks. Available only in commercial
  version of Tracardi.
* `SOURCE_TTL` - Default: 60. Each resource read is cached for given seconds. That means that when you change any
  resource data, e.g. credentials it wil be available with max 60 seconds.
* `CACHE_PROFILE` - Default: no. Profiles can be cached, but it is not recommended as this option is experimental.

## Debugging settings

* `TRACK_DEBUG` - Default: no.
* `LOGGING_LEVEL` - Default: WARNING

## Event server configuration

* `SYNC_PROFILE_TRACKS` - Default: False. Available only in commercial version of Tracardi.
* `RUN_HEARTBEAT_EVERY` - Default: 300. The time each worker reports its health.

## Storage settings

* `STORAGE_DRIVER` - Default: elastic. There is only one storage driver available at this moment, and it is elastic.


