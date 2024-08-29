from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PowerWrapper',
  version='0.0.6',
  description='A powerful library that wraps advanced functions.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='SapphireKR',
  author_email='sapphirekr11@protonmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['python', 'wrapper'], 
  packages=find_packages(),
  install_requires=[''] 
)