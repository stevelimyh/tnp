import os
import glob
from setuptools import find_packages, setup

package_name = 'b1_01_john_artc'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rosi',
    maintainer_email='john_abogado@artc.a-star.edu.sg',
    description='ROS2 Basics 2025 Assessment Solutions',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'task = b1_01_john_artc.task:main'
        ],
    },
)
