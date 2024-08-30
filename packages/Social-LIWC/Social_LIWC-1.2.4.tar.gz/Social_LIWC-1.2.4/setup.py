from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Social_LIWC',
    version='1.2.4',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['fastapi', 'liwc', 'pandas'],
    packages=['Social_LIWC/api', 'Social_LIWC/dados', 'Social_LIWC'],
    # packages=find_packages(where="Social_LIWC"),
    include_package_data=True,
    package_dir={"":"src"},
    package_data={
        '': ['*.dic'],
    }
)