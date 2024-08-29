from setuptools import setup
import os

from incversion import read_version, increment_version

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

package_data = []
codepath = os.path.join(os.getcwd(), "eskmo")
for root, dirs, files in os.walk(codepath):
    for file in files:
        if not file.endswith(".py"):
            package_data.append(os.path.join(root, file))

prev_version = read_version("VERSION")
version = increment_version(prev_version)

setup(
    name = "eskmo",
    version = version,
    packages=["eskmo"],
    package_data={'eskmo': package_data},
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = "eskmo",
    author_email="fatfingererr@gmail.com",
    description="eskmo",
    url="https://github.com/ProjectEskmo/eskmo",                                         
    keywords=[],    
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Natural Language :: Chinese (Traditional)",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: Microsoft :: Windows",
    ],
    platforms=["Windows"],
    python_requires=">=3.9",
    install_requires=[
        'chardet>=5.2.0',
        'colorama>=0.4.6',
        'comtypes>=1.1.10',
        'psutil>=5.9.5',
        'python-dotenv>=1.0.0',
        'pywin32>=300',
        'pyzmq>=22.0.3',
    ]
)