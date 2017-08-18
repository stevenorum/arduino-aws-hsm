#!/usr/bin/env python3

import boto3
import boto3.session
import botocore.session
from botocore.client import Config
from botocore.auth import SigV2Auth, SigV3Auth, SigV4Auth, S3SigV4Auth, SigV4QueryAuth, S3SigV4QueryAuth, S3SigV4PostAuth, HmacV1Auth, HmacV1QueryAuth, HmacV1PostAuth

class HsmAuth(object):
    def __init__(self, *args, **kwargs):
        pass

    def add_auth(self, request):
        raise RuntimeError("You successfully called the HSM auth thingy!!1!")

class SigV2AuthHsm(HsmAuth, SigV2Auth):
    pass

class SigV3AuthHsm(HsmAuth, SigV3Auth):
    pass

class SigV4AuthHsm(HsmAuth, SigV4Auth):
    pass

class S3SigV4AuthHsm(HsmAuth, S3SigV4Auth):
    pass

class SigV4QueryAuthHsm(HsmAuth, SigV4QueryAuth):
    pass

class S3SigV4QueryAuthHsm(HsmAuth, S3SigV4QueryAuth):
    pass

class S3SigV4PostAuthHsm(HsmAuth, S3SigV4PostAuth):
    pass

class HmacV1AuthHsm(HsmAuth, HmacV1Auth):
    pass

class HmacV1QueryAuthHsm(HsmAuth, HmacV1QueryAuth):
    pass

class HmacV1PostAuthHsm(HsmAuth, HmacV1PostAuth):
    pass

AUTH_TYPE_TO_HSM = {
    None: 'v4-hsm',
    's3': 'v1-hsm',
    's3-query': 'v1-query-hsm',
    's3-presign-post': 'v1-post-hsm',
    'v2': 'v2-hsm',
    'v3': 'v3-hsm',
    'v3https': 'v3-hsm',
    'v4': 'v4-hsm',
    'v4-query': 'v4-query-hsm',
    's3v4': 'v4-s3-hsm',
    's3v4-query': 'v4-s3-query-hsm',
    's3v4-presign-post': 'v4-s3-post-hsm',
}

class HsmEnabledSession(botocore.session.Session):
    def create_client(self, service_name, region_name=None, api_version=None,
                      use_ssl=True, verify=None, endpoint_url=None,
                      aws_access_key_id=None, aws_secret_access_key=None,
                      aws_session_token=None, config=None):
        if config is not None:
            config_hsm = copy.deepcopy(config)
            config_hsm.signature_version = AUTH_TYPE_TO_HSM[config.signature_version]
        else:
            config_hsm = Config(signature_version=AUTH_TYPE_TO_HSM[None])
            pass
        return super().create_client(service_name, region_name=region_name, api_version=api_version,
                              use_ssl=use_ssl, verify=verify, endpoint_url=endpoint_url,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token, config=config_hsm)

def enable_hsm_signature_types():
    from botocore.auth import AUTH_TYPE_MAPS
    global AUTH_TYPE_MAPS
    AUTH_TYPE_MAPS['v1-hsm'] = HmacV1AuthHsm
    AUTH_TYPE_MAPS['v1-query-hsm'] = HmacV1QueryAuthHsm
    AUTH_TYPE_MAPS['v1-post-hsm'] = HmacV1PostAuthHsm
    AUTH_TYPE_MAPS['v2-hsm'] = SigV2AuthHsm
    AUTH_TYPE_MAPS['v3-hsm'] = SigV3AuthHsm
    AUTH_TYPE_MAPS['v4-hsm'] = SigV4AuthHsm
    AUTH_TYPE_MAPS['v4-s3-hsm'] = S3SigV4AuthHsm
    AUTH_TYPE_MAPS['v4-s3-query-hsm'] = S3SigV4QueryAuthHsm
    AUTH_TYPE_MAPS['v4-s3-post-hsm'] = S3SigV4PostAuthHsm
    pass

def make_hsm_signing_default():
    enable_hsm_signature_types()
    boto3.setup_default_session(botocore_session=HsmEnabledSession())
    pass
