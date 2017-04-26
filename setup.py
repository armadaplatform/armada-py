from setuptools import setup

setup(
    name='armada',
    packages=['armada'],
    version='1.1',
    description='Configuration manager for ArmadaPlatform services.',
    author='Ganymede',
    author_email='cerebro@ganymede.eu',
    url='https://github.com/armadaplatform/armada-py',
    download_url='https://github.com/armadaplatform/armada-py/tarball/1.1',
    keywords=['armada', 'hermes', 'config'],
    classifiers=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
