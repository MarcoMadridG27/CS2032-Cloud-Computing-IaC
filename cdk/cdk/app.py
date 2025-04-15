# app.py
#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_stack import MVStack

app = cdk.App()
MVStack(app, "MVDesarrollo")
app.synth()
