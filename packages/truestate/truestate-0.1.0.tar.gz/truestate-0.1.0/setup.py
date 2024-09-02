from setuptools import setup, find_packages

setup(
    name='truestate',
    version='0.1.0',
    description='A Python client for the Truestate API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='TrueState',
    author_email='support@truestate.io',
    url='https://docs.truestate.io/',
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        # List your dependencies here, e.g., 'requests', 'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
