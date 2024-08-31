from setuptools import find_packages, setup


def read_long_description():
    with open('pkg_api.md') as f:
        return f.read()


setup(
    name='binned-hawkes-multilayer',
    version='0.0.5',
    author='Matthew Sit',
    author_email='matthew.sit22@imperial.ac.uk',
    description='A binned Hawkes process for dynamic multilayer graphs.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
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
