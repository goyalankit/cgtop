from setuptools import setup
#from cgtop import __version__

setup(
    name='cgtop',
    version=0.0,
    description='A cgroup resource viewer',
    long_description=open('README.md').read(),
    keywords='top for cgroups',
    author='Ankit Goyal',
    author_email='ankit3goyal@gmail.com',
    url='https://github.com/goyalankit/cgtop',
    license='MIT',
    download_url= 'https://github.com/goyalankit/cgtop/archive/master.zip',
    packages=['cgtop'],
    install_requires=[
        "brownie>=0.5.1"
    ],
    entry_points={
        'console_scripts': ['cgtop = cgtop.main:top']
    },

)

