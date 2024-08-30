from setuptools import setup, find_packages

setup(
    name="django_api_request_logging",
    version="0.2.0",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    python_requires=">=3.6",
    description="A Django module for logging incoming requests",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)