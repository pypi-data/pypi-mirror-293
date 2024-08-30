from setuptools import setup, find_packages

setup(
    name='trufflehog.1',
    version='1.0',  # Update to the desired version
    description='TruffleHog - Find secrets in your code',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add other dependencies as required by TruffleHog
    ],
    entry_points={
        'console_scripts': [
            'install-trufflehog=trufflehog_installer.trufflehog:main',  # Update this if the entry point differs
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
