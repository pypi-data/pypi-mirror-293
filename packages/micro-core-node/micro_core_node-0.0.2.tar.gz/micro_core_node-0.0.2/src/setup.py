from setuptools import setup, find_packages

setup(
    name="micro-core-node",  
    version="0.0.1",  
    author="Usmanov",  
    author_email="usmnvk.work@gmail.com", 
    description="Is training for self",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    packages=find_packages(where="src"), 
    package_dir={"": "src"},  
    python_requires=">=3.10.0",  
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Micro-Core/MicroCore",  
    project_urls={  
        "Homepage": "https://github.com/Micro-Core/MicroCore",
        "Issues": "https://github.com/Micro-Core/MicroCore",
    },
    install_requires=[
        
        "typer>=0.3.2",  
    ],
    entry_points={ 
        "console_scripts": [
            "microcore-cli = microcore.cli.execute:app",
        ],
    },
)
