from setuptools import setup, find_packages

setup(
    name='cysec_sample_package',
    version='0.0.2',
    packages= find_packages(),
    install_requires=[
        # 'azure-storage-blob',
        # 'azure-storage-queue',
        # 'google-cloud-storage'
    ],
    python_requires=">=3.10",
)