from setuptools import setup, find_packages

setup(
    name="li-robot-parameter-change-monitor-source",
    version="0.2.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
    
    ],
    author="Juncheng Zhang",
    author_email="zhangjunchengbh@163.com",
    description="A package for industrial robot parameter change monitoring using ZDT API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.example.com/your-group/robot-parameter-change-monitor-source",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)