from unittest import TestCase

from cbr_shared.aws.s3.Minio_As_S3 import Minio_As_S3
from cbr_shared.aws.s3.S3 import S3
from osbot_utils.testing.Hook_Method import Hook_Method


class TestCase__Minio(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hook_method = Hook_Method(S3, 'client')     # todo: see if we also need to hook the main S3 class (from osbot_aws)
        cls.hook_method.mock_call = cls.minio_as_s3__client
        cls.hook_method.wrap()

    @classmethod
    def tearDownClass(cls):
        cls.hook_method.unwrap()

    def minio_as_s3__client(self):
        return Minio_As_S3().s3_client()