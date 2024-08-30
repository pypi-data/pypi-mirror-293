from setuptools import setup, find_packages

setup(
    name="zap-installer",
    version="0.1.1",
    author="Udit",
    author_email="uditrajsingh815@example.com",
    description="A script to download and install OWASP ZAP",
    long_description="This package provides a command-line tool to download and install OWASP ZAP.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.25.1",  # Requests package to handle the download
    ],
    entry_points={
        'console_scripts': [
            'install-zap=zap_installer.zap:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
