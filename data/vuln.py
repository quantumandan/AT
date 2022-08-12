"""
Simulate supply chain attack on a vulnerable python package.
"""


def download_package(package_name):
    """
    Download a package from a remote pypi server.
    """
    print("Downloading package {}".format(package_name))


def extract_requirements(package_name):
    pkg = download_package(package_name)
    # from pkg, extract requirements.py
    
