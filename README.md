# Kubernetes for dummies

## [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
![Kubernetes Components](components-of-kubernetes.svg)
<p align="center">
    Kubernetes Components, source: https://kubernetes.io/docs/concepts/overview/components/
</p>

## Local Kubernetes installation
Choose one:
1. Install [Minikube](https://minikube.sigs.k8s.io/docs/start/)
1. Install [MicroK8s](https://microk8s.io/)

## Kubernetes crash course (1 hour)

## TODO Describe scenario here
In this tutorial we will use pre-built docker images published on Dockerhub to ease the job. For further details how to define and build docker images please see Docker documentation.

**You will learn**
- How to deploy application with several replicas and access it via Service.
- Deploy second service in a separated namespace and establish communication between two services.


TODO to mention:
- helm
- terraform
- rbac
- replace \ with /

### Create namespaces
[Kubernetes supports multiple virtual clusters backed by the same physical cluster. These virtual clusters are called namespaces.](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

```
> kubectl create ns cloud
> kubectl create ns edge
> kubectl create ns jobs
```

List creates namespaces. Note that some "system" namespaces already did exist.
```
> kubectl get namespaces
```

### Deploy first service Cloud APP
Deployments docs: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

TODO: describe YAML file key points here

Deployment of the app with 3 replicas together with a related Service.
```
> kubectl apply -f cloud-app/cloud-app-deployment.yaml
```

List pods to see, if app was deployed. _Note: see `-n` argument to list pods from a given namespace._
```
> kubectl get pods -n cloud

NAME                                    READY   STATUS              RESTARTS   AGE
cloud-app-deployment-76c4547875-7mxbr   0/1     ContainerCreating   0          81s
cloud-app-deployment-76c4547875-ftwml   0/1     ContainerCreating   0          81s
cloud-app-deployment-76c4547875-vvndf   0/1     ContainerCreating   0          81s

// After couple of minutes pods should be running
NAME                                    READY   STATUS    RESTARTS   AGE
cloud-app-deployment-76c4547875-7mxbr   1/1     Running   0          2m22s
cloud-app-deployment-76c4547875-ftwml   1/1     Running   0          2m22s
cloud-app-deployment-76c4547875-vvndf   1/1     Running   0          2m22s
```

See, if we can communicate with the deployed app in the Kubernetes cluster. To do that, we need to access `cloud-app` related service named `cloud-app-service`. To do that, we can use port forwarding feature of the Kubernetes.
Port forwarding docs: https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/
```
> kubectl port-forward service/cloud-app-service 5000:5000 -n cloud

// Now, you can request the service and get the correct response.
>  curl http://localhost:5000/
Hello, World!
```

Bonus: there is an option to expose [running service publicly](https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/). For purposes of this tutorial we will skip this setup.

### Deploy second service Edge APP
Edge app will be deployed in the separated namespace `edge` and communication between `cloud-app` and `edge-app` across namespaces will be established.

Deploy the application and service
```
> kubectl apply -f edge-app/edge-app-deployment.yaml
```

List pods to see, if app was deployed. _Note: see `-n` argument to list pods from a given namespace._
```
> kubectl get pods -n edge

NAME                                   READY   STATUS              RESTARTS   AGE
edge-app-deployment-6f7bc44796-98ndm   0/1     ContainerCreating   0          9s
edge-app-deployment-6f7bc44796-d7t9f   0/1     ContainerCreating   0          9s
edge-app-deployment-6f7bc44796-s5klz   0/1     ContainerCreating   0          9s

// After couple of minutes pods should be running
NAME                                   READY   STATUS    RESTARTS   AGE
edge-app-deployment-6f7bc44796-98ndm   1/1     Running   0          114s
edge-app-deployment-6f7bc44796-d7t9f   1/1     Running   0          114s
edge-app-deployment-6f7bc44796-s5klz   1/1     Running   0          114s
```

We will not expose or port-forward `edge-app`, because it can be accessed via `cloud-app`. Let's see how that works.

### Establishing communication between two services across namespaces
Port forwarding docs: https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/

First, let's expose `cloud-app`, so we can query it directly
```
> kubectl port-forward service/cloud-app-service 5000:5000 -n cloud

> curl http://localhost:5000/
Hello, World!
```
Port-forwarding seems to be working just fine.

Now, let's try to query `edge-app` via `cloud-app` by requesting `/edge` endpoint.
```
> curl http://localhost:5000/edge/stateless
Starting stateless job
```

Notice that `EDGE_API_URL` environment variable needs to be correctly set to the `'http://edge-app-service.edge.svc.cluster.local:5000/job'` which is Kubernetes internal DNS resolution of the `edge-app-service` running in the `edge` namespace. If this variable was incorrectly set, communication between services would not work.

### Start a stateless Job with Ephemeral storage and see how it works
Volumes docs: https://kubernetes.io/docs/concepts/storage/volumes/

Start the stateless job (could be any stateless application, e.g. data processing task, API, etc.)
```
> kubectl create -f .\job-app-manual.yaml
job.batch/job-app-hhxf4 created
```

Now list the pods within the namespace and copy newly created pod name to obtain logs.
```
> kubectl logs -f job-app-hhxf4-4sfw4 -n jobs
Working hard on stateless
Before disk write: []
After disk write: ['9227465.txt']
```
As you can see, attached disk location (`/mnt/storage`) was empty, but file could be written on disk. Any files written on an ephemeral storage lives there only during lifetime of the pod.

Let's try to run the same job again and see whether disk location is empty.
```
> kubectl create -f .\job-app-manual.yaml
job.batch/job-app-z4gdr created

> kubectl logs -f job-app-z4gdr-tjbkf -n jobs
Working hard on stateless
Before disk write: []
After disk write: ['9227465.txt']
```
Disk location was empty as expected. To preserve files saved on a disk location we need to use Persistent Volumes, which are described below.

### Start a stateful Job with Persistent Volume claim disk attached
Persistent Volumes docs: https://kubernetes.io/docs/concepts/storage/persistent-volumes/

Start job with a Persistent Volume claim
```
> kubectl create -f .\job-app-manual-persistent.yaml

// See the logs
> kubectl logs -f job-app-c2d5r-vgvd6 -n jobs
Working hard on stateful
Before disk write: []
After disk write: ['35.txt']
```

Start the same job again. Now, the calculated number will be loaded from a persistent disk.
```
> kubectl create -f .\job-app-manual-persistent.yaml

// See the logs
> kubectl logs -f job-app-25ztg-2b6gp -n jobs
Working hard on stateful
Before disk write: ['35.txt']
Reading pre-calculated fib number from file /mnt/storage/35.txt
```


### Exec into the running pod
```
> kubectl exec -it <copy pod name here> -n cloud -- /bin/bash
```
