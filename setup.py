from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'moving_cart_example'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
    ],
    install_requires=[
        'setuptools'
    ],
    zip_safe=True,
    maintainer='Sanjana Kumari',
    maintainer_email='sanjana@virtuslabs.in',
    description='Moving cart example code',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_controls_gui = moving_cart_example.teleop_controls_gui:main',
        ],
    },
)