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


to mention:
- helm
- terraform
- rbac

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

### Deploy first service

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
```
> kubectl port-forward service/cloud-app-service 5000:5000 -n cloud

// Now request the service and you should get correct response
>  curl http://localhost:5000/
Hello, World!
```

Bonus: there is an option to expose [running service publicly](https://kubernetes.io/docs/tutorials/kubernetes-basics/expose/expose-intro/). For purposes of this tutorial we will skip this setup.