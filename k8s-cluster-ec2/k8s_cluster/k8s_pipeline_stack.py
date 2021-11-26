from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines


class K8SPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(self, 'Pipeline',

                                         cloud_assembly_artifact=cloud_assembly_artifact,
                                         pipeline_name='cdk8s-pipeline',

                                         source_action=cpactions.GitHubSourceAction(
                                             action_name='Github',
                                             output=source_artifact,
                                             oauth_token=core.SecretValue.secrets_manager(
                                                 'github-token'),
                                             owner='donnieprakoso',
                                             repo='tutorial-cdk-eks-ec2',
                                             branch='main',
                                             trigger=cpactions.GitHubTrigger.POLL),

                                         synth_action=pipelines.SimpleSynthAction(
                                             source_artifact=source_artifact,
                                             cloud_assembly_artifact=cloud_assembly_artifact,
                                             install_command='npm install -g aws-cdk && npm install -g cdk8s-cli && cd k8s-cluster-ec2 && pip install -r requirements.txt',
                                             synth_command='cdk synth'))
