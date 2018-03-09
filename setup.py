from setuptools import setup


setup(name='nicehash_api',
      version='0.1',
      description='API for nicehash',
      keywords='nicehash mine',
      url='https://github.com/edilio/nicehash_api',
      author='DEGConnect',
      author_email='info@degconnect.com',
      license='MIT',
      packages=["nicehash_api", ],
      install_requires=[
          'requests==2.18.1',
      ],
      zip_safe=False
      )

