from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    CfnTag
)
from constructs import Construct


class MVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Truco: Usar parámetros SSM preconfigurados en AWS Academy
        vpc_id = ssm.StringParameter.value_for_string_parameter(
            self, "/aws/service/vpc/id"
        )

        subnet_id = ssm.StringParameter.value_for_string_parameter(
            self, "/aws/service/subnet/public/id"
        )

        # Security Group usando L1 (no requiere permisos especiales)
        sg = ec2.CfnSecurityGroup(
            self, "SG",
            group_description="Permitir SSH y HTTP",
            vpc_id=vpc_id,
            security_group_ingress=[
                {"ipProtocol": "tcp", "fromPort": 22, "toPort": 22, "cidrIp": "0.0.0.0/0"},
                {"ipProtocol": "tcp", "fromPort": 80, "toPort": 80, "cidrIp": "0.0.0.0/0"}
            ],
            tags=[CfnTag(key="Name", value="SG-Tarea")]
        )

        # Instancia EC2 directa (sin roles)
        ec2.CfnInstance(
            self, "Instancia",
            instance_type="t2.micro",
            image_id="ami-043cbf1cf918dd74f",
            key_name="vockey",
            subnet_id=subnet_id,
            security_group_ids=[sg.ref],
            block_device_mappings=[{
                "deviceName": "/dev/xvda",
                "ebs": {"volumeSize": 20, "volumeType": "gp2"}
            }],
            tags=[CfnTag(key="Name", value="MV-Desarrollo")]
        )