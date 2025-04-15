# Terraform EC2 Deployment

Este proyecto crea una instancia EC2 en AWS usando Terraform como herramienta de Infraestructura como Código (IaC).

## 🎯 Requisitos de la práctica

- Usar AMI `Cloud9ubuntu22`
- Clave SSH: `vockey`
- Puertos abiertos: 22 (SSH) y 80 (HTTP)
- Disco de 20 GB
- Tipo de instancia: `t2.micro`
- Ejecutar desde la MV Desarrollo con rol `LabRole`
- Crear o actualizar el archivo `/home/ubuntu/.aws/credentials` (opcional si se usa rol)

## 📄 Archivos

- `main.tf`: define la infraestructura
- `.gitignore`: evita subir archivos no necesarios

## ✅ Cómo ejecutar (desde la MV Desarrollo)

```bash
git clone https://github.com/tu-usuario/terraform-ec2.git
cd terraform-ec2
terraform init
terraform apply
