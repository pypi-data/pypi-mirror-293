from setuptools import setup, find_packages
import subprocess

# Function to install the SpaCy model
def install_spacy_model():
    subprocess.check_call(["python", "-m", "spacy", "download", "en_core_web_sm"])


# Call the function during setup
install_spacy_model()
setup(
    name="FENICE",
    version="0.1.4",
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
)
