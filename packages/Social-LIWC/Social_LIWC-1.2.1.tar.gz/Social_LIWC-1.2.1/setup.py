from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Social_LIWC',
    version='1.2.1',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['fastapi', 'liwc', 'pandas'],
    packages=['Social_LIWC/api', 'Social_LIWC'],
    include_package_data=True,
    package_data={
        'Social_LIWC': ['../dados/*'],
    }
)