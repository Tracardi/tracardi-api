# Why I have this error: Invalid data reference. Dot notation `event@...` could not access data?

The error message "Invalid data reference. Dot notation event@... could not access data" typically indicates that there
is an issue with the dot notation used to access data. Here are a few possible reasons for this error:

1. Typo in the dot notation: Double-check the dot notation used to access the data and ensure that there are no typos or
   syntax errors. Even a small mistake, such as a misspelled property name or an incorrect key, can result in this
   error.

2. Data does not exist: Verify that the data you are trying to access actually exists. E.g. If the data is not present in the
   event properties, you won't be able to access it using dot notation. Make sure the data you are referencing has been
   properly set or assigned before attempting to access it.

3. Invalid index or key: If the data you are trying to access is an array or an object, respectively, ensure that the
   index or key you are using is valid. For arrays, the index should be within the bounds of the array (e.g., 0 to
   length-1). For objects, the key should be a valid property of the object.

To troubleshoot this error, you can review your code or configuration and compare it with the documentation or examples
provided by the framework or tool you are using. Pay attention to the syntax and make sure the data you are referencing
exists and is accessible at the given location in the event.