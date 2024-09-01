from setuptools import setup, find_packages

setup(
    name='custom_utilities',
    version='0.1.7',
    description='Python package consisting of custom utilities',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts':[
            'custom-utilities-hello = custom_utilities:hello'
        ]
    }
)