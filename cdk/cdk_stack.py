from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear VPC con subnet pública
        vpc = ec2.Vpc(self, "VPC",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ],
            nat_gateways=0
        )

        # Obtener una subred pública de la VPC
        public_subnet = vpc.public_subnets[0]

        # Grupo de seguridad
        sg = ec2.SecurityGroup(
            self, "SG",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # AMI Ubuntu (la que mencionaste antes)
        ami_id = "ami-03c983b9d7cd45421"  # Cloud9ubuntu22

        # Instancia EC2 con CfnInstance
        ec2.CfnInstance(self, "Instancia",
            image_id=ami_id,
            instance_type="t2.micro",
            key_name="vockey",
            subnet_id=public_subnet.subnet_id,
            security_group_ids=[sg.security_group_id],
            block_device_mappings=[{
                "deviceName": "/dev/xvda",
                "ebs": {
                    "volumeSize": 20,
                    "volumeType": "gp2"
                }
            }],
            tags=[{
                "key": "Name",
                "value": "MVDesarrollo"
            }]
        )
