import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "aegis",
    version = "0.0.1",
    author = "Govind Gnanakumar",
    author_email = "govind@automorphic.ai",
    description = ("Aegis is a self-hardening firewall for large language models."
                   " Protect your models from adversarial attacks: prompt injections, prompt and PII leakage, toxic language, and more."),
    license = "MIT",
    keywords = "llm, language model, security, adversarial attacks, prompt injection, prompt leakage, PII detection, self-hardening, firewall",
    # url = "http://packages.python.org/an_example_pypi_project",
    packages=['aegis'],
    install_requires=['requests'],
    long_description=read('README.md'),
)
