from setuptools import setup, find_packages

setup(
    name='payloader',
    version='0.3.0',
    description='A simple HTTP client for making GET and POST requests',
    author='samhuelt',
    packages=find_packages(),
    python_requires='>=3.6',
    long_description='updated for better importing',
    long_description_content_type='text/plain',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
