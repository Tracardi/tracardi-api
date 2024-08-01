# How can the "Address already in use" issue in Tracardi be resolved?

To resolve the "Address already in use" issue in Tracardi, you can remap the port that Tracardi is running on. By
changing the port mapping in the Docker run command, you can assign a different port for Tracardi to use, such as
changing from 8686 to 8888. Additionally, if you are using Tracardi's GUI, you will also need to update the API URL to
reflect the new port.