
from setuptools import setup

setup(
        name='csvgb',
        version='0.1',
        description='CSV Utilities for Maintaining a Gradebook',
        url='http://github.com/bmccary/csvgb',
        author='Brady McCary',
        author_email='brady.mccary@gmail.com',
        license='MIT',
        packages=['csvgb'],
        install_requires=[
                'csvu',
            ],
        scripts=[
                ],
        zip_safe=False
    )
