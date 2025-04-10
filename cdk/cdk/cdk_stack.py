from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        sg = ec2.SecurityGroup(
            self, "SecurityGroup",
            vpc=vpc,
            description="Permitir acceso SSH y HTTP",
            allow_all_outbound=True
        )

        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP")

        ami = ec2.MachineImage.generic_linux({
            "us-east-1": "ami-0fc5d935ebf8bc3bc"
        })

        instance = ec2.Instance(
            self, "MiInstancia",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ami,
            vpc=vpc,
            security_group=sg,
            key_name="vockey",
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(20)
                )
            ]
        )
