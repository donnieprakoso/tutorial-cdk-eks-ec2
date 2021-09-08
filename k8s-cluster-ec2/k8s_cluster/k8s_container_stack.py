from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
import yaml

class K8SContainerStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cdk_eks_vpcAz = cdk.Fn.import_value("cdkEksVpcAz").split(",")
        cdk_eks_vpcId = cdk.Fn.import_value("cdkEksVpcId")
        cdk_eks_clusterName = cdk.Fn.import_value("cdkEksClusterName")
        cdk_eks_kubectlRoleArn = cdk.Fn.import_value("cdkEksKubectlRoleArn")
        cdk_eks_securityGroupId = cdk.Fn.import_value("cdkEksSgId")
        cdk_eks_oidcProviderArn = cdk.Fn.import_value("cdkEksOidcProviderARN")

        vpc = ec2.Vpc.from_vpc_attributes(
            self, "{}-vpc".format(construct_id), vpc_id=cdk_eks_vpcId, availability_zones=cdk_eks_vpcAz)

        eks_cluster = eks.Cluster.from_cluster_attributes(
            self, "cluster",
            cluster_name=cdk_eks_clusterName,
            open_id_connect_provider=eks.OpenIdConnectProvider.from_open_id_connect_provider_arn(
                self, "{}-oidcProvider".format(construct_id),
                open_id_connect_provider_arn=cdk_eks_oidcProviderArn
            ),
            kubectl_role_arn=cdk_eks_kubectlRoleArn,
            vpc=vpc,
            kubectl_security_group_id=cdk_eks_securityGroupId,
        )

        file_app_deployment = open("../cdk8s/dist/cdk8s-deployment.k8s.yaml", 'r')
        yaml_app_deployment = yaml.load(
            file_app_deployment, Loader=yaml.FullLoader)
        file_app_deployment.close()

        file_app_service = open("../cdk8s/dist/cdk8s-service.k8s.yaml", 'r')
        yaml_app_service = yaml.load(
            file_app_service, Loader=yaml.FullLoader)
        file_app_service.close()
        
        eks_cluster.add_manifest(
            "{}-app-deployment".format(construct_id), yaml_app_deployment)

        eks_cluster.add_manifest(
            "{}-app-service".format(construct_id), yaml_app_service)

