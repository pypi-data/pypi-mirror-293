from setuptools import setup

setup(
    name='systemdcli',
    version='0.1.0',
    py_modules=['systemdcli'],
    install_requires=['cleo', ],
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'systemdcli = systemdcli:main'
        ]
    }
)
