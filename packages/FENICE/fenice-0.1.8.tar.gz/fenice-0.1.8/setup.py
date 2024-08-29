from setuptools import setup, find_packages
import subprocess
from setuptools.command.install import install
import sys
import os

# Function to install the SpaCy model
class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print("here1")
        install.run(self)
        print("here2")
        script_path = os.path.join(
            os.path.dirname(__file__), "metric", "post_install.py"
        )
        print("here3")
        subprocess.check_call([sys.executable, script_path])
        print("here4")


# Call the function during setup
setup(
    name="FENICE",
    version="0.1.8",
    author="Alessandro Scirè",
    author_email="scire@diag.uniroma1.it",
    description="This package contains the code to execute FENICE, a factuality-oriented metric for summarization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Babelscape/FENICE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "torch",
        "tqdm",
        "spacy==3.7.4",
        "fastcoref==2.1.6",
        "transformers~=4.38.2",
        "sentencepiece==0.2.0",
        "scikit-learn==1.5.0",
    ],
    entry_points={
        "console_scripts": [
            # If you have command line scripts, list them here.
            # For example: 'my-script=my_package.module:function',
        ]
    },
    cmdclass={"install": PostInstallCommand},
)
