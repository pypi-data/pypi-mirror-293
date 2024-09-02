from cbr_shared.aws.s3.S3_DB_Base import S3_DB_Base
from osbot_aws.AWS_Config import aws_config
from osbot_utils.decorators.methods.cache_on_self import cache_on_self


BUCKET_NAME__CBR = "{account_id}-cyber-boardroom"

class S3_DB__CBR(S3_DB_Base):

    @cache_on_self
    def s3_bucket(self):
        return BUCKET_NAME__CBR.format(account_id=aws_config.account_id())

