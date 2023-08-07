from setuptools import find_packages, setup
import glob
import os

package_name = 'color_pose_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/utils', glob.glob(os.path.join('utils', '*.ply'))),
        ('share/' + package_name, ['package.xml']),
        ('share/color_pose_detection/launch',
            glob.glob(os.path.join('launch', '*launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='annameer',
    maintainer_email='anna-maria.meer@ipa.fraunhofer.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'color_pose_estimation = color_pose_detection.color_pose_estimation:main',
            'color_pose_estimation_unique = color_pose_detection.color_pose_estimation_unique:main',
        ],
    },
)
