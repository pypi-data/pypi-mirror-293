from setuptools import setup, find_packages

setup(
    name='trufflehog.1',
    version='0.1',  # Update to the desired version
    description='TruffleHog - Find secrets in your code',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.25.1',
        'boto3>=1.17.0',
        'gitpython>=3.1.0',
        'click>=8.0.0',
        # Add other dependencies as required by TruffleHog
    ],
    entry_points={
        'console_scripts': [
            'trufflehog=trufflehog.trufflehog:main',  # Update this if the entry point differs
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
