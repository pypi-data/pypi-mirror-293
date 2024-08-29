# encoding: utf-8
from setuptools import setup, find_packages


setup(
    name='openrouter',
    version='1.0',
    packages=find_packages(),
    license='MIT',
    author='vboxvm512',
    author_email='vboxvm512@gmail.com',
    description='Unofficial OpenRouter Chatbot AI Library',
    long_description="README.md",
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests',
	'urllib3'
    ]
)
