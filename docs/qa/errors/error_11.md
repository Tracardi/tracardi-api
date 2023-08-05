# Error "The GUI version 0.8.0 does not match the API version"

The error message "The GUI version 0.8.0 does not match the API version" suggests that there is a mismatch between the
versions of the Tracardi GUI and API. To resolve this issue, you can follow the steps below:

1. Check the versions: Click on the Tracardi name in the menu to view the versions of the GUI and API. Ensure that both
   versions API and GUI are displayed and note down the numbers. The number should be the same.

2. Verify Docker versions: Make sure that the Docker versions (tags) of both the GUI and API are the same. 

3. Update Docker images: If the Docker versions are not the same, update the Docker images for both the GUI and API to
   match the desired version. This can typically be done using Docker commands or through a Docker management tool.

4. Restart the services: After updating the Docker images, restart the Tracardi GUI and API services to apply the
   changes and ensure that they use the correct versions.

By ensuring that the GUI and API versions are in sync and using the same Docker images, you should be able to resolve
the error message and have a consistent Tracardi environment. 
