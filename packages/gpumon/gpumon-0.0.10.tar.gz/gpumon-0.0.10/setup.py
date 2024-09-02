from setuptools import setup, find_packages

setup(
    name="gpumon",  # New package name
    version="0.0.10",
    packages=find_packages(),
    include_package_data=True,
    description="A simple GPU monitoring tool.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/abdkhanstd/GpuMonitor",
    author="ABD",
    author_email="abdkhan@163.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "psutil",
        "gputil"
    ],
    entry_points={
        'console_scripts': [
            'gpumon=gpumon:main',  # Update to reflect the new package name and entry point
        ],
    },
)
