This plugin allows users to count key strings in order to increase the value of a key in a profile. It can be used for
simple statistics, such as counting how many users visited a website on a mobile device versus other devices such as a
desktop or tablet. The configuration of the plugin requires a key string to be provided, which will be used to increase
the value of the key in the profile. The key string can be provided in the form of a string or a list of strings, and
dot notation can be used to access data. Additionally, the save_in field must point to data in the profile that will
hold the information on key counts. This field should be an empty object or a key-value object, and it holds the
original data that will be incremented.

Examples of the plugin in use are provided, such as when the value in the payload is a list of strings or a list of
objects. In the former case, the key count will be equal to the number of times each string appears in the list, and in
the latter case, the key will be increased by the provided value. Additionally, an example of configuration with dot
notation in the key and save_in fields is provided.