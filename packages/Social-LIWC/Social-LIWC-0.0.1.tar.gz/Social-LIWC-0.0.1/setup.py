from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Social-LIWC',
    version='0.0.1',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['liwc', 'pandas'],
    packages=['Social_LIWC/dados', 'Social_LIWC'],
    include_package_data=True,
    package_data={
        '': ['*.dic','*.csv'],
    }
)