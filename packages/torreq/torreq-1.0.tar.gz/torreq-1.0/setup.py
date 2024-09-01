from setuptools import setup

setup(
    name='torreq',
    version='1.0',
    description='Makes HTTP requests to both the clearnet and the darknet via the Tor network',
    author='Jonah Kaufman',
    author_email='jonah@gigawatt.org',
    packages=['torreq'],
    install_requires=['requests', 'stem', 'socksipy-branch'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
