from setuptools import setup, find_packages
from setuptools import Command


# read version from version.py file in olvid module
version = {}
with open("olvid/version.py") as fd:
    exec(fd.read().strip(), version)


class VersionCommand(Command):
    description = "Print olvid module version"
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version['__version__'])


setup(
    name='olvid-bot',
    version=version["__version__"],
    description="Module to communicate with Olvid daemon project",
    author="olvid.io",
    author_email="bot@olvid.io",
    url="https://olvid.io",
    keywords=["olvid"],
    packages=find_packages(
        include=[
            "olvid",
            "olvid.core",
            "olvid.listeners",
            "olvid.datatypes",
            "olvid.internal", "olvid.internal.admin", "olvid.internal.commands", "olvid.internal.notifications", "olvid.internal.types",
            "olvid.tools"
        ]
    ) + [
        "olvid.protobuf", "olvid.protobuf.olvid", "olvid.protobuf.olvid.daemon",
        "olvid.protobuf.olvid.daemon.services", "olvid.protobuf.olvid.daemon.services.v1",
        "olvid.protobuf.olvid.daemon.admin", "olvid.protobuf.olvid.daemon.admin.v1",
        "olvid.protobuf.olvid.daemon.command", "olvid.protobuf.olvid.daemon.command.v1",
        "olvid.protobuf.olvid.daemon.datatypes", "olvid.protobuf.olvid.daemon.datatypes.v1",
        "olvid.protobuf.olvid.daemon.notification", "olvid.protobuf.olvid.daemon.notification.v1"
    ],
    package_data={'olvid.core.calls.aiortc.codecs': ['*.pyi', "*.so"]},
    include_package_data=True,
    python_requires=">=3.10, <4",
    install_requires=[
        "grpcio==1.65.4", "grpcio-tools==1.65.4", "protobuf==5.27.3",
        # cli
        "asyncclick==8.1.7.2", "anyio==4.4.0", "uvloop==0.19.0"
    ],
    cmdclass={
        "version": VersionCommand,
    },
)
