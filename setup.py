from setuptools import setup
import os


'''
Sample APP setup file, the name of the sample app should be unique
Please provide your own git repo url, description,
author name, email, please include additional packages as well for your app
'''

test_deps = [
    'pytest==5.4.3',
    'pytest-mock==3.2.0',
    'pytest-cov==2.10.0',
]
extras = {
    'test': test_deps,
}

with open(os.path.join('VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name='onboard-slack',
    version=version,
    description='Onboarding Slack Bot - Flask app',
    url='https://github.aexp.com/amex-eng/dw-onboarding',
    author='teamkronos',
    author_email='teamkronos@aexp.com',
    license='American Express',
    packages=[],
    include_package_data=True,
    tests_require=test_deps,
    extras_require=extras,
    install_requires=[
        'flask==1.1.2',
        'flask_restful==0.3.8',
        'Flask-Cors>=3.0.9',
        'gensim==3.8.3',
        'gunicorn==20.0.4',
        'boto3==1.13.8',
        'pyjwt>=2.4.0',
        'cryptography>=3.2',
        'requests==2.23.0',
        'psycopg2-binary==2.8.5',
        'Flask-Excel==0.0.7',
        'pyexcel-xls==0.5.8',
        'pyexcel-xlsx==0.5.8',
        'PyYAML>=5.4'
    ]
)