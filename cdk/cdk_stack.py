from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class MVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC básica
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

        # Security Group
        sg = ec2.SecurityGroup(
            self, "SG",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # Par de claves (nuevo método recomendado)
        key_pair = ec2.KeyPair.from_key_pair_name(self, "Vockey", "vockey")

        # Instancia EC2 sin rol IAM
        ec2.Instance(
            self, "Instancia",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": "ami-043cbf1cf918dd74f"
            }),
            vpc=vpc,
            security_group=sg,
            key_pair=key_pair,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20)
                )
            ],
            # Muy importante: evita que CDK cree un rol IAM
            role=None
        )
