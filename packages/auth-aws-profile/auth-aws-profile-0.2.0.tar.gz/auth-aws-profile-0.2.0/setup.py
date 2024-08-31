# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auth_aws_profile']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.35.5,<2.0.0']

entry_points = \
{'console_scripts': ['auth-aws-profile = '
                     'auth_aws_profile.auth_aws_profile:main']}

setup_kwargs = {
    'name': 'auth-aws-profile',
    'version': '0.2.0',
    'description': 'Updates the configured MFA credentials for AWS services.',
    'long_description': '# auth-aws-profile\n\nMake authenticating your AWS credentials with MFA easier by using a script provided in this repository.\nDeveloped using Python 3.12 and [Poetry](https://python-poetry.org/).\nThe authentication process uses the V3 SDK for Python.\n\n## Requirements\n\n* Python `^3.12`.\n* An AWS credentials file, e.g. `~/.aws/credentials`, with one or more sections that contain the following keys.\n    * `aws_access_key_id`\n    * `aws_secret_access_key`\n    * `aws_session_token`\n* An AWS configuration file, e.g. `~/.aws/config`, with one or more `[profile *]` sections.\n    * The `[profile *]` should reference a section from `~/.aws/credentials` using `source_profile = *` and must have the `role_arn` key as well.\n\n## Example\n\nHere\'s what the script expects your AWS configuration and credentials file to look like.\n\n```\n# ~/.aws/config\n\n[default]\nregion = <my-aws-region>\noutput = yaml\n\n[profile my-role]\nrole_arn = arn:aws:iam::<my-aws-account-number>:role/my-role\nsource_profile = mfa\n```\n\n```\n# ~/.aws/credentials\n\n[default]\naws_access_key_id = foo\naws_secret_access_key = bar\n\n[mfa]\naws_access_key_id = foo\naws_secret_access_key = bar\naws_session_token = baz\n```\n\nThe AWS CLI can still find `my-role` even if you move it to `~/.aws/credentials` as long as it\'s renamed to `[my-role]` instead of `[profile my-role]`.\nHowever, this script requires `my-role` to be in `~/.aws/config` and must be passed to the script using the complete profile section name, e.g. `profile my-role`.\n\n## Usage\n\nInstall the script from PyPi and verify the version.\n\n```\npip install auth-aws-profile\nauth-aws-profile --version\n```\n\nHere\'s a simple usage example based on the files mentioned in [Example](#example).\n\n```\nauth-aws-profile "profile my-role" "arn:aws:iam::<my-aws-account-number>:mfa/john.doe"\n```\n\nSee the help documentation for details.\n\n```\nauth-aws-profile --help\n```\n\n## Development\n\n### Installation\n\n* At least Python 3.12 must be installed.\n* [Poetry](https://python-poetry.org/) is installed. See [Installation](https://python-poetry.org/docs/#installation).\n* Install the project with Poetry from the root using `poetry install`.\n\n### Installation (Dev Containers)\n\n* Docker must be installed.\n* Install the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VS Code or similar.\n',
    'author': 'kdico',
    'author_email': '8462911+kdico@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
