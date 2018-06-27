from setuptools import setup, find_packages
setup(
    name='dxl-data',
    version='0.0.15',
    description='Data Processing Library.',
    url='https://github.com/Hong-Xiang/dxdata',
    author='Hong Xiang',
    author_email='hx.hongxiang@gmail.com',
    license='MIT',
    namespace_packages=['dxl'],
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=['dxl-core', 'dxl-fs', 'pandas==0.20.3'],
    scripts=[],
    entry_points="""
        [console_scripts]
        dxdata=dxl.data.cli.main:dxdata
    """,
    zip_safe=False)
