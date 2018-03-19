from setuptools import setup, find_packages
setup(name='dxl-data',
      version='0.0.1',
      description='Data Processing Library.',
      url='https://github.com/Hong-Xiang/dxdata',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=['dxl.data'],
      package_dir = {'': 'src/python'},
      install_requires=[],
      scripts=[],
    #   namespace_packages = ['dxl'],
      zip_safe=False)
