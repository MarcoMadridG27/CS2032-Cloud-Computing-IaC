import pulumi
import pulumi_aws as aws

# Nombre del par de claves existente
key_name = "vockey"

# Crear un Security Group que permita tráfico SSH (22) y HTTP (80)
sec_group = aws.ec2.SecurityGroup("vm-sec-group",
    description="Permitir SSH y HTTP",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egress=[{
        "protocol": "-1",
        "from_port": 0,
        "to_port": 0,
        "cidr_blocks": ["0.0.0.0/0"],
    }]
)

# Obtener la AMI más reciente de Ubuntu 22.04
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["099720109477"],  # Canonical (Ubuntu)
    filters=[{
        "name": "name",
        "values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
    }]
)

# Crear una instancia EC2
instance = aws.ec2.Instance("vm-pulumi",
    instance_type="t2.micro",
    ami=ami.id,
    key_name=key_name,
    vpc_security_group_ids=[sec_group.id],
    root_block_device={
        "volume_size": 20,
        "volume_type": "gp2"
    },
    tags={
        "Name": "PulumiVM"
    }
)

# Exportar salidas
pulumi.export("instance_id", instance.id)
pulumi.export("public_ip", instance.public_ip)
