#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s


class DeploymentChart(Chart):
    def __init__(self, scope: Construct, id: str):
        label = {"app": "cdk8s"}
        k8s.KubeDeployment(self, 'deployment',
            spec=k8s.DeploymentSpec(
                replicas=2,
                selector=k8s.LabelSelector(match_labels=label),
                template=k8s.PodTemplateSpec(
                metadata=k8s.ObjectMeta(labels=label),
                spec=k8s.PodSpec(containers=[
                    k8s.Container(
                    name='cdk8s',
                    image='nginx:latest',
                    ports=[k8s.ContainerPort(container_port=80)])]))))

class ServiceChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        label = {"app": "cdk8s"}

        k8s.KubeService(self, 'service',
                    spec=k8s.ServiceSpec(
                    type='LoadBalancer',
                    ports=[k8s.ServicePort(port=80, target_port=k8s.IntOrString.from_number(80))],
                    selector=label))


app = App()
service_chart = ServiceChart(app, "cdk8s-service")
deployment_chart = DeploymentChart(app, "cdk8s-deployment")

app.synth()
