from setuptools import setup

package_name = 'robot_arm_v3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='seojin',
    maintainer_email='seojin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'serial_reader = robot_arm_v3.serial_reader_and_pub:main',
            'serial_sub = robot_arm_v3.serial_data_subscriber:main',
            'node = robot_arm_v3.my_first_node:main',
        ],
    },
)
