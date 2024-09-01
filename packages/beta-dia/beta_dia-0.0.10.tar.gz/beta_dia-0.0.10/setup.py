from setuptools import setup, find_packages

setup(
    name='beta_dia',
    version='0.0.10',
    packages=find_packages(),
    description='A cool project that does something awesome on diaPASEF data.',
    include_package_data=True,
    author='Song Jian',
    license='MIT',
    install_requires=[
        'h5py',
        'matplotlib',
        'networkx',
        'numba',
        'numpy<2.0.0',
        'pandas',
        'pyzstd',
        'scikit-learn',
        'scipy',
        'statsmodels',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'beta_dia_test=beta_dia.dist.main:main',
        ],
    },
)
