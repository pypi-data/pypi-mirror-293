from distutils.core import setup
from os import path

try:
  this_directory = path.abspath(path.dirname(__file__))
  with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()
except:
  long_description = "A python library for interacting with Straful quantum computing API backbone."

setup(
  name = 'straful-python',
  packages = ['straful_python'],  
  version = '0.1.2',
  license='MIT',
  description = 'A python library for interacting with Straful quantum computing API backbone.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Radu Marginean',
  author_email = 'radu.marginean@transilvania-quantum.com',
  url = 'https://transilvania-quantum.com/',
  download_url = 'https://github.com/Transilvania-Quantum/straful-python/releases/tag/v0.1.1',
  keywords = ['quantum', 'computing', 'API backbone'],  
  install_requires=[            
          'click',
          'pyyaml'
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
