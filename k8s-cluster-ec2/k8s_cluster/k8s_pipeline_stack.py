from aws_cdk import core
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from aws_cdk import pipelines


class K8SPipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(self, "{}-pipeline".format(id),
                                pipeline_name="{}-pipeline".format(id),
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.git_hub(
                                                    "donnieprakoso/tutorial-cdk-eks-ec2", "main",
                                                    authentication=core.SecretValue.secrets_manager(
                                                        "github-token")
                                                ),
                                                commands=["npm install -g aws-cdk",
                                                          "npm install -g cdk8s-cli",
                                                          "cd k8s-cluster-ec2",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                )
                                )
