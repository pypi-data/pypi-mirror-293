from setuptools import setup, find_packages

setup(
    name='amazon_dsp_sdk',  # Replace with the name of your SDK
    version='0.1.0',  # Update with your version number
    description='A Python SDK for Amazon DSP API',  # Short description of your SDK
    author='Thota Mohan Reddy',  # Your name as the author
    author_email='thotamohanreddy993@gmail.com',  # Your email address
    url='https://github.com/yourusername/your_sdk_repo',  # URL to your project's repository
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        'requests',  # List your dependencies here
        'azure-core'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update with the appropriate license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
    entry_points={
        'console_scripts': [
            'your_sdk_command=your_module:main_function',  # Replace with any command-line scripts
        ],
    },
)
