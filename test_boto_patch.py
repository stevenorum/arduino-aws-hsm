#!/usr/bin/env python3

from arduinohsm.auth import make_hsm_signing_default
make_hsm_signing_default()
import boto3

cf = boto3.client("cloudformation", region_name="us-east-1")
print(cf.list_exports())
