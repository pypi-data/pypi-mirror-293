from setuptools import setup

setup(
    name='gmlutil-geo-models',
    version='2.0.3',    
    description='General Machine Learning Utility Package for Geospatial Models',
    url='https://github.com/Phillip1982/gmlutil_geo_models',
    author='Phillip Kim',
    author_email='phillip.kim@ejgallo.com',
    license='BSD 2-clause', ## Change this
    packages=['gmlutil_geo_models'],
    install_requires=[ # package>=0.2,<0.3
        'numpy==1.26.4',
		'pandas>2.1.0,<=2.2.2',
        'geopandas>=1.0.0',
        'scikit-learn>=1.3.2',
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
