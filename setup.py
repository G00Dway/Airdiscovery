from setuptools import setup

setup(name='airdiscover',
      version='0.2',
      description='Network discovery & Deauth attacks',
      url='https://github.com/G00Dway/Airdiscovery',
      author='G00Dway',
      license='MIT',
      python_requires='>=3.7.0',
       install_requires=[
          'packaging', 'pyyaml', 'requests', 'paramiko',
          'adb-shell', 'pyngrok', 'urllib3'
      ]
)