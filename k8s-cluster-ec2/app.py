#!/usr/bin/env python3
from aws_cdk import core as cdk

from k8s_cluster.k8s_cluster_stack import K8SClusterStack
from k8s_cluster.k8s_container_stack import K8SContainerStack

AWS_ACCOUNT_ID = cdk.Aws.ACCOUNT_ID
AWS_REGION = cdk.Aws.REGION
STACK_NAME = "cdk8s-eks-ec2"

app = cdk.App()
cluster = K8SClusterStack(app, STACK_NAME,
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION),
    )

container = K8SContainerStack(app, "{}-container".format(STACK_NAME))
container.add_dependency(cluster)
app.synth()
