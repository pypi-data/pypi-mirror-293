from setuptools import find_packages, setup

setup(
    name='binned-hawkes-multilayer',
    version='0.0.1',
    author='Matthew Sit',
    author_email='matthew.sit22@imperial.ac.uk',
    description='A binned Hawkes process for dynamic multilayer graphs.',
    long_description='A binned Hawkes process for dynamic multilayer graphs.',
    long_description_content_type='text/plain',
    packages=find_packages('binned_hawkes_multilayer'),
    install_requires=[
        'matplotlib==3.6.0',
        'numpy==1.22.4',
        'scipy==1.7.3',
        'typing',
        'nptyping',
        'networkx==2.8.6',
        'pytype',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    license='Apache-2.0',
)
