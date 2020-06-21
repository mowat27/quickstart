"""An AWS Python Pulumi program"""

import os
import sys
import pulumi
import re
from pulumi_aws import s3, kms

# if not 'GIT_BRANCH' in os.environ:
#     sys.exit('GIT_BRANCH must be set')
# env_name = re.sub(r'[^a-z]+', '-', os.environ['GIT_BRANCH'].lower())

stack_name = pulumi.get_stack()
print("INFO : Stack name is", stack_name)

config = pulumi.Config()
key = kms.Key(f'{stack_name}-key')
bucket = s3.Bucket(f'{stack_name}-bucket',
                   server_side_encryption_configuration={
                       "rule": {
                           'apply_server_side_encryption_by_default': {
                               'sse_algorithm': 'aws:kms',
                               'kms_master_key_id': key.id
                           }
                       }
                   })

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
