from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_eks as eks


class K8SClusterStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create master role for EKS Cluster
        iam_role = iam.Role(self, id="{}-iam".format(construct_id),
                            role_name="{}-iam".format(construct_id), assumed_by=iam.AccountRootPrincipal())

        # Creating Cluster with EKS
        ec2_cluster = eks.Cluster(self, id="{}-cluster".format(construct_id), cluster_name="{}-cluster".format(
            construct_id), masters_role=iam_role, version=eks.KubernetesVersion.V1_20,
        )

        # Define outputs in order to import the Kubernetes cluster in the deployment step
        cdk.CfnOutput(
            self, id="{}-out-clusterName".format(construct_id),
            value=ec2_cluster.cluster_name,
            description="The name of the EKS Cluster",
            export_name="cdkEksClusterName"
        )

        cdk.CfnOutput(
            self, id="{}-out-oidcArn".format(construct_id),
            value=ec2_cluster.open_id_connect_provider.open_id_connect_provider_arn,
            description="The EKS Cluster's OIDC Provider ARN",
            export_name="cdkEksOidcProviderARN"
        )

        cdk.CfnOutput(
            self, id="{}-out-vpcId".format(construct_id),
            value=ec2_cluster.vpc.vpc_id,
            description="EKS VPC ID",
            export_name="cdkEksVpcId"
        )

        cdk.CfnOutput(
            self, id="{}-out-vpcAz".format(construct_id),
            value=str(ec2_cluster.vpc.availability_zones),
            description="EKS VPC Az",
            export_name="cdkEksVpcAz"
        )

        cdk.CfnOutput(
            self, id="{}-out-kubectlRoleArn".format(construct_id),
            value=ec2_cluster.kubectl_role.role_arn,
            description="The EKS Cluster's kubectl Role ARN",
            export_name="cdkEksKubectlRoleArn"
        )
        
        cdk.CfnOutput(
            self, id="{}-out-eksSgId".format(construct_id),
            value=ec2_cluster.kubectl_security_group.security_group_id,
            description="The EKS Cluster's kubectl SG ID",
            export_name="cdkEksSgId"
        )