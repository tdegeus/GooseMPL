
import os

from setuptools                 import setup
from setuptools.command.install import install

# --------------------------------------------------------------------------------------------------

class PostInstallCommand(install):

  def run(self):

    try:

      import GooseMPL

      GooseMPL.copy_style()

      install.run(self)

    except:

      import goosempl

      goosempl.copy_style()

      install.run(self)

# --------------------------------------------------------------------------------------------------

if os.path.isdir('GooseMPL'): packages = ['GooseMPL']
else                        : packages = ['goosempl']

# --------------------------------------------------------------------------------------------------

setup(
  name              = 'GooseMPL',
  version           = '0.2.6',
  author            = 'Tom de Geus',
  author_email      = 'tom@geus.me',
  url               = 'https://github.com/tdegeus/GooseMPL',
  keywords          = 'matplotlib, style',
  description       = 'Style and extension functions for matplotlib',
  long_description  = '',
  license           = 'MIT',
  install_requires  = ['matplotlib>=2.0.0', 'numpy>=1.0.0'],
  packages          = packages,
  cmdclass          = {'install': PostInstallCommand},
)

# --------------------------------------------------------------------------------------------------
