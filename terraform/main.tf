provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "mi_sg" {
  name        = "permitir_ssh_http"
  description = "Permitir puertos 22 y 80"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "mi_instancia" {
  ami                    = "ami-043cbf1cf918dd74f"  # Cloud9Ubuntu22 (verificada)
  instance_type          = "t2.micro"
  key_name               = "vockey"
  security_groups        = [aws_security_group.mi_sg.name]

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }

  tags = {
    Name = "InstanciaTerraform"
  }
}
