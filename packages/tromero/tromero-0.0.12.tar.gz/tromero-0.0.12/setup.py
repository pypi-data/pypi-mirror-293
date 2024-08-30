from setuptools import setup, find_packages

setup(
    name="tromero",  # Replace with your package name
    version="0.0.12",  # Replace with your package's version
    author="Tromero",  # Replace with your name
    author_email="admin@tromero.ai",  # Replace with your email address
    description="Python client for Tromero Cloud Platform!",  # Provide a short description
    long_description=open('README.md').read(),  # This will read your long description from README.md
    long_description_content_type='text/markdown',  # Indicates that the long description is in Markdown
    url="https://www.tromero.ai/",  # Replace with the URL to your package's homepage
    license="MIT",  # Replace with your chosen license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Automatically find all packages and subpackages
    include_package_data=True,
    install_requires=[
        "annotated-types==0.6.0",
        "anyio==4.3.0",
        "certifi==2024.7.4",
        "charset-normalizer==3.3.2",
        "distro==1.9.0",
        "h11==0.14.0",
        "httpcore==1.0.5",
        "httpx==0.27.0",
        "idna==3.7",
        "openai==1.16.1",
        "pydantic==2.6.4",
        "pydantic_core==2.16.3",
        "requests==2.32.2",
        "setuptools==70.0.0",
        "sniffio==1.3.1",
        "tqdm==4.66.3",
        "typing_extensions==4.10.0",
        "urllib3==2.2.2",
        "fire",
    ],
     entry_points={
        'console_scripts': [
            'tromero=tromero.cli:main'
        ]
    },
    python_requires='>=3.6',  # Specify the minimum version of Python required
)
