import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simscore',
    version='28.08.001',
    author='Sai Ram Reddy Shabeena Kamuluri Tejashri Kothapalli',
    author_email='sairamrdya@gmail.com',
    description='This software is being developed at the Madanapalle Institute of Technology & Science.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/sairamarava/MITS_AIBIRDS',
    license='GPLv3',
    install_requires=['numpy', 'scipy'],
    extras_require={
        'gpu':  ['cupy', 'pycuda'],
        'spark': ['pyspark'],
        'dev': ['twine', 'setuptools', 'build'],
        'docs': [ 'sphinx>=3.0.0']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Intended Audience :: Science/Research'
    ],
    python_requires='>=3.5',
)