from setuptools import setup, find_packages

setup(
    name='MQTTSimpleClient',
    version='0.2.0',
    description='A custom MQTT library for interaction with an MQTT broker',
    author='Riccardo Filomena',
    author_email='filomena.riccardo@gmail.com',
    url='https://github.com/filoriccardo/MQTTSimpleClient',
    packages=find_packages(),
    package_data={
        'MQTTSimpleClient': ['cfg/conf.xml'],
    },
    include_package_data=True,
    install_requires=[
        'paho-mqtt',
        'lxml',
        'setuptools'
        # aggiungi altre dipendenze qui
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
