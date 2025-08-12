from setuptools import setup
from pathlib import Path
import os
from glob import glob

package_name = 'ros2_aruco'

def get_model_data_files():
    files = []
    for path in Path('models').rglob('*'):
        if path.is_file():
            install_path = os.path.join('share', package_name, str(path.parent))
            files.append((install_path, [str(path)]))
    return files

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ] + get_model_data_files(),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='John Abogado',
    maintainer_email='john_abogado@artc.a-star.edu.sg',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'aruco_node = ros2_aruco.aruco_node:main',
            'aruco_generate_marker = ros2_aruco.aruco_generate_marker:main'
        ],
    },
)
