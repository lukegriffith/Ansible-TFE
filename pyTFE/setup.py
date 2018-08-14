from setuptools import setup, find_packages


setup(name='pyTFE',
      version=0.1,
      description='Terraform Enterprise Interface for Python.',
      author='Luke Griffith',
      author_email='lukemgriffith@gmail.com',
      keywords=['HashiCorp', 'Terraform', 'Enterprise'],
      license='MIT',
      packages=find_packages(exclude=("pyTFE_tests",)),
      include_package_data=True,
      zip_safe=True,
      )