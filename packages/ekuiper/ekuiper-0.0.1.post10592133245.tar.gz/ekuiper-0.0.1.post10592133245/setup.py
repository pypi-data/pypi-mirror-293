from setuptools import setup, find_packages

setup(
    name='ekuiper',
    version='0.0.1-10592133245',
    packages=find_packages(),
    url='https://github.com/lf-edge/ekuiper',
    license='Apache License 2.0',
    author='LF Edge eKuiper team',
    author_email='huangjy@emqx.io',
    description='Python SDK for eKuiper portable plugin',
    install_requires=["pynng==0.7.2"],
)
