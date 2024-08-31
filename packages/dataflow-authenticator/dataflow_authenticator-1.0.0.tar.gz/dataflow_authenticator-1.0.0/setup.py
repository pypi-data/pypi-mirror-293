from setuptools import setup, find_packages

setup(
    name="dataflow_authenticator",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={},
    install_requires=[],
    author="Dataflow",
    author_email="",
    description="Dataflow authenticator",
    entry_points={
        'jupyterhub.authenticators': [
            'dataflow_authenticator = authenticator.dataflowhubauthenticator:DataflowHubAuthenticator',
        ],
    },
)