# How to install kubernetes for Tracardi

We advice to use k3s as a simple K8s cluster. 

To do so you will need at lease 3 machines or VPSes.

To install a k3s cluster with at least 3 nodes, follow these steps:

1. **Install k3s on the First Node**:
   On your main server node (Master), run the following command to install k3s:
   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```
   This will install k3s and start it as a service. To get the token required for adding agent nodes, run:
   ```bash
   sudo cat /var/lib/rancher/k3s/server/node-token
   ```

2. **Install k3s on Agent Nodes**:
   On each of the remaining nodes (agent nodes), run the following command, replacing `<SERVER_IP>` with the IP address
   of your server node and `<NODE_TOKEN>` with the token retrieved from the server node:
   ```bash
   curl -sfL https://get.k3s.io | K3S_URL=https://<SERVER_IP>:6443 K3S_TOKEN=<NODE_TOKEN> sh -
   ```

3. **Verify the Cluster**:
   After installing k3s on all nodes, verify the cluster status on the server node by running:
   ```bash
   kubectl get nodes
   ```
   This command should list all nodes in the cluster, including the master and agent nodes, showing their status as "
   Ready".

# How to manage k3s from outside the cluster

Managing a K3s (Lightweight Kubernetes) cluster from outside the cluster involves configuring `kubectl` to access the
cluster remotely. Here's a step-by-step guide on how to do this:

### 1. Set Up K3s Cluster

Make sure your K3s cluster is running and you have access to the `kubeconfig` file, which is usually located
at `/etc/rancher/k3s/k3s.yaml` on the master node.

### 2. Expose the K3s API Server

Ensure that port 6443 (default port for the Kubernetes API server) is open on your firewall and accessible from your
remote location.

### 3. Copy and modify /etc/rancher/k3s/k3s.yaml` file

Copy the remote file `/etc/rancher/k3s/k3s.yaml` (from server master node) to you local computer (best location on your
local computer is: `~/.kube/config`). Modify the file (`~/.kube/config`). Update the `server` field to use the external
IP or DNS name of the master node:

```yaml
server: https://YOUR_EXTERNAL_IP:6443
```

This will tell you computer where the k3s cluster is located.

### 4. Configure `kubectl`

1. **Set the `KUBECONFIG` Environment Variable**:

```sh
export KUBECONFIG=~/.kube/config
```

2. **Test the Connection**: Verify that you can connect to the K3s cluster from your local computer.

```sh
kubectl get nodes
```

### 4. Secure the Connection

For production environments, it is important to secure the API server:

- **Use a VPN**: Set up a VPN to securely connect to your internal network.
- **TLS Certificates**: Ensure that TLS certificates are properly configured and trusted.
- **Firewall Rules**: Restrict access to the API server to specific IP addresses.

### Example Commands

1. **Copy `k3s.yaml` to Local Machine**:

```sh
scp user@master-node:/etc/rancher/k3s/k3s.yaml ~/.kube/config
```

2. **Edit `k3s.yaml`**:

Update the `server` field to use the external IP or DNS name:

```yaml
server: https://YOUR_EXTERNAL_IP:6443
```

3. **Set `KUBECONFIG`**:

```sh
export KUBECONFIG=~/.kube/config
```

4. **Test Connection**:

```sh
kubectl get nodes
```

``` title="Example output for 3 node cluster"
NAME      STATUS   ROLES                  AGE   VERSION
node-02   Ready    <none>                 1s   v1.29.4+k3s1
node-03   Ready    <none>                 1s   v1.29.4+k3s1
node-01   Ready    control-plane,master   1s   v1.29.4+k3s1
```

5. **Your K3s cluster is ready**: Now you can use kubectl to manage the kluster from you machine.

# Other K8s Clients

We recommend OpenLens which is the open-source version of Lens, a popular Kubernetes IDE. Installing OpenLens involves
downloading the appropriate package for your operating system and setting it up. Here are the steps to install OpenLens
on different operating systems:

### For Windows

1. **Download the Installer**:
    - Go to the [OpenLens GitHub Releases page](https://github.com/MuhammedKalkan/OpenLens/releases).
    - Download the `.exe` installer for the latest version of OpenLens.

2. **Run the Installer**:
    - Double-click the downloaded `.exe` file.
    - Follow the installation prompts to complete the setup.

### For macOS

1. **Download the Installer**:
    - Go to the [OpenLens GitHub Releases page](https://github.com/MuhammedKalkan/OpenLens/releases).
    - Download the `.dmg` file for the latest version of OpenLens.

2. **Install OpenLens**:
    - Open the downloaded `.dmg` file.
    - Drag the OpenLens application to the Applications folder.

### For Linux

1. **Download the Installer**:
    - Go to the [OpenLens GitHub Releases page](https://github.com/MuhammedKalkan/OpenLens/releases).
    - Download the appropriate package for your distribution (e.g., `.AppImage`, `.deb`, or `.rpm`).

2. **Install OpenLens**:
    - For `.AppImage`:
      ```sh
      chmod +x OpenLens-x.y.z.AppImage
      ./OpenLens-x.y.z.AppImage
      ```
    - For `.deb` (Debian/Ubuntu):
      ```sh
      sudo dpkg -i OpenLens-x.y.z.deb
      ```
    - For `.rpm` (Fedora/CentOS/RHEL):
      ```sh
      sudo rpm -i OpenLens-x.y.z.rpm
      ```

### Launch OpenLens

After installation, you can launch OpenLens from your application launcher or by running `openlens` from the terminal,
depending on your operating system.

### Connecting to a Kubernetes Cluster

1. **Open OpenLens**:
    - Launch OpenLens from your installed applications.

2. **Add Cluster**:
    - Click on "Add Cluster" and follow the prompts to connect to your Kubernetes cluster. You will need
      the `kubeconfig` file for your cluster.

3. **Manage Clusters**:
    - Once connected, you can manage and monitor your Kubernetes clusters using the OpenLens interface.

