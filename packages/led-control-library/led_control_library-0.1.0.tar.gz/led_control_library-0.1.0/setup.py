from setuptools import setup, find_packages

setup(
    name='led_control_library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
    author='Yessmine Chabchoub',
    author_email='yessmine.chabchoub@ipk.fraunhofer.de',
    description='A Python library to control LED brightness using Arduino',
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.cc-asp.fraunhofer.de/yes08184/dimmer/-/tree/main/code/lib/led_control_library',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)
