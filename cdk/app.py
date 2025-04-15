#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack import MVStack

app = cdk.App()
stack = MVStack(app, "MVDesarrollo")

# Configuración para evitar creación de roles
stack.template_options.metadata = {
    "cdk_legacy_stack": True,
    "aws:cdk:disable-iam": True
}

app.synth()