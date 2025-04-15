from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class MVStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self,
            "MinimalVPC",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )

        sg = ec2.SecurityGroup(
            self,
            "SG",
            vpc=vpc,
            description="Permitir acceso SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        ec2.Instance(
            self,
            "Instancia",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.lookup(name="Cloud9ubuntu22"),
            key_name="vockey",
            vpc=vpc,
            security_group=sg,
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20))
            ]
        )