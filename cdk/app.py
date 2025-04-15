#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack import MVStack

app = cdk.App()
MVStack(app, "MVDesarrollo",
    env=cdk.Environment(account="584758245304", region="us-east-1")
)
app.synth()
