# I can not connect to http://localhost:8686 when using docker.

You are unable to connect to localhost when using a Docker container because Docker has its own network, and when you
refer to "localhost" inside a Docker container, it points to the container's local environment, not your laptop's. To
connect to the services running on your laptop from the Docker container, you need to use your laptop's IP address
instead of "localhost."

Try this:

1. Make sure the API is working correctly. If it's accessible at http://localhost:8686/docs, that's a good sign.

2. Instead of using "localhost", find your laptop's IP address. You can do this by checking
   your laptop's network settings or using a command like `ipconfig` (on Windows) or `ifconfig` (on Linux/macOS).
   Replace "localhost" with your laptop's IP address in the URL.
3. Check http://<your-laptop-ip>:8686 in the browser. It should return `{"detals": "Not found"}`, that means it works correctly.

4. Type Tracardi API as http://<your-laptop-ip>:8686 in the GUI by using the URL with your laptop's IP address. For example, if your laptop's IP is
   192.168.1.100, you would use http://192.168.1.100:8686/.

By following these steps, you should be able to connect to your laptop's services from within the Docker container and
resolve the connection error.