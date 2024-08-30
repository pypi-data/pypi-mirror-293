from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Social_LIWC',
    version='1.2.2',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['fastapi', 'liwc', 'pandas'],
    packages=['api', 'dados'],
    # packages=find_packages(where="Social_LIWC"),
    include_package_data=True,
    package_dir={"":"Social_LIWC"},
    package_data={
        '': ['*.dic'],
    }
)