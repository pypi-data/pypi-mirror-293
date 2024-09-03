# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  setup.py                                                                             #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='csi_genai_lib',
    version="0.1.34",
    description='Caber GenAI Chat Capture Library',
    author='Rob Quiros',
    author_email='dev@caber.com',
    package_dir={
        "csiMVP": "../csiMVP"
    },
    packages=find_packages(),
    py_modules=[
        'csiMVP.Common.init',
        'csiMVP.Common.sequence',
        'csiMVP.Common.remote_open',
        'csiMVP.Common.tf_config_load',
        'csiMVP.Dependencies.elastic_search_init',
        'csiMVP.Toolbox.consolidate',
        'csiMVP.Toolbox.filenames',
        'csiMVP.Toolbox.aws_init',
        'csiMVP.Toolbox.goodies',
        'csiMVP.Toolbox.json_encoder',
        'csiMVP.Toolbox.retry',
        'csiMVP.Toolbox.obo',
        'csiMVP.Toolbox.sqs_init',
        'csiMVP.Toolbox.supabase'
    ],
    package_data={
        '.Common': [
            'config.json'
        ]
    },
    install_requires=[
        'pandas==1.5.3',
        'numpy==1.26.4',
        # 'packaging==23.2',
        'boto3>=1.18.1',
        'smart-open[s3]>=5.1.0',
        'requests>=2.26.0',
        # 'requests_aws4auth>=1.1.1',
        'urllib3>=1.25.11',
        # 'frozendict',
        # 'dnspython==2.4.0',
        # 'netifaces2>=0.0.18',
        # 'python-nmap>=0.7.1'
    ],
)
