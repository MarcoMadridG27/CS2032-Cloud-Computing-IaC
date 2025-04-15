# app.py
#!/usr/bin/env python3
import aws_cdk as cdk
from mv_stack import MVStack

app = cdk.App()
MVStack(app, "MVDesarrollo")
app.synth()
