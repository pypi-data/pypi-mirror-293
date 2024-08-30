from setuptools import setup

setup(
    name='gmlutil-ts-models',
    version='2.0.3',    
    description='General Machine Learning Utility Package for Timeseries Models',
    url='https://github.com/Phillip1982/gmlutil_ts_models',
    author='Phillip Kim',
    author_email='phillip.kim@ejgallo.com',
    license='BSD 2-clause', ## Change this
    packages=['gmlutil_ts_models'],
    install_requires=[
		'numpy==1.26.4',
		'pandas>2.1.0,<=2.2.2',
        'statsmodels>=0.14.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS',
		'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
