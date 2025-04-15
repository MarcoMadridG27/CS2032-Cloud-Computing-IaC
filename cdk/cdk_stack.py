from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnTag
)
from constructs import Construct

class MVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Usar la VPC por defecto (sin lookup)
        vpc = ec2.Vpc(self, "VPC",
            max_azs=1,  # Usar solo 1 AZ para minimizar permisos
            subnet_configuration=[
                {
                    "name": "Public",
                    "subnetType": ec2.SubnetType.PUBLIC,
                    "cidrMask": 24
                }
            ],
            nat_gateways=0  # Sin NAT para reducir permisos
        )

        # Security Group básico
        sg = ec2.SecurityGroup(
            self, "SG",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # Instancia EC2 con AMI específica
        ec2.Instance(
            self, "Instancia",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": "ami-043cbf1cf918dd74f"  # AMI verificada
            }),
            vpc=vpc,
            security_group=sg,
            key_name="vockey",
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20))
            ]
        )