import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dshw',
    version='0.0.1',
    author='Dmytro Shuiskyi',
    author_email='darnesmeister@gmail.com',
    description='Monitor of CPU and memory utilization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/darnes',  # todo: use url of repo
    packages=['dshw', ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Fedora linux',
    ],
    python_requires='>=3.7',
    scripts=['scripts/dshw_consumer.py', 'scripts/dshw_producer.py'],
    install_requires=[
        'psutil',
    ],
)
