from setuptools import setup, find_packages

setup(
    name='office_cracker',              # Package name
    version='0.1.0',                   # Version number
    packages=find_packages(),           # Automatically find packages
    install_requires=[                  # List your dependencies
        # Add any dependencies your script needs
    ],
    author='agent 047',                 # Your name
    author_email='khalidziraoui6@gmail.com@example.com', # Your email
    description='advance office 365 cracker ', # Brief description
    long_description=open('README.md').read(), # Read long description from README
    long_description_content_type='text/markdown', # Specify content type
    url='https://t.me/UnkownxArmy', # Project URL
    classifiers=[                       # Optional classifiers
        'Programming Language :: Python :: 2.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=2.6',           # Specify Python version
)
