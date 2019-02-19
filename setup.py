
import os

from setuptools                 import setup
from setuptools.command.install import install

# --------------------------------------------------------------------------------------------------

class PostInstallCommand(install):

  def run(self):

    import GooseMPL

    GooseMPL.copy_style()

    install.run(self)

# --------------------------------------------------------------------------------------------------

setup(
  name              = 'GooseMPL',
  version           = '0.2.11',
  author            = 'Tom de Geus',
  author_email      = 'tom@geus.me',
  url               = 'https://github.com/tdegeus/GooseMPL',
  keywords          = 'matplotlib, style',
  description       = 'Style and extension functions for matplotlib',
  long_description  = '',
  license           = 'MIT',
  install_requires  = ['matplotlib>=2.0.0', 'numpy>=1.0.0'],
  packages          = ['GooseMPL'],
  cmdclass          = {'install': PostInstallCommand},
)

# --------------------------------------------------------------------------------------------------
