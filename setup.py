from setuptools import setup


setup(name='nicehash_api',
      version='0.11',
      description='API for nicehash',
      keywords='nicehash mine',
      url='https://github.com/edilio/nicehash_api',
      author='DEGConnect',
      author_email='info@degconnect.com',
      license='MIT',
      packages=["nicehash_api", ],
      install_requires=[
          'requests>=2.13.0',
      ],
      zip_safe=False
      )

