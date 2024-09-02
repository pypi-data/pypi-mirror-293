from setuptools import setup, find_packages

setup(
    name="ArabicTagger",  
    version="0.1.1b1",
    packages=find_packages(),
    install_requires=["tensorflow==2.10.0",\
                      "keras==2.10.0",\
                      "pickle", "bpemb", "numpy"],
    author="Eslam Tarek Farouk",
    description="A BI-LSTM & CRF model implemented in Keras & Arabic Tagger",
    url="https://github.com/yourusername/my_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
