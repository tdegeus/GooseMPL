
from setuptools                 import setup
from setuptools.command.install import install

# --------------------------------------------------------------------------------------------------

class PostInstallCommand(install):

  def run(self):

    import goosempl
    goosempl.copy_style()

    install.run(self)

# --------------------------------------------------------------------------------------------------

__version__ = '0.2.0'

# --------------------------------------------------------------------------------------------------

setup(
  name              = 'goosempl',
  version           = __version__,
  author            = 'Tom de Geus',
  author_email      = 'tom@geus.me',
  url               = 'https://github.com/tdegeus/GooseMPL',
  keywords          = 'matplotlib style',
  description       = 'Style and extension functions for matplotlib',
  long_description  = '',
  license           = 'MIT',
  install_requires  = ['matplotlib>=2.0.0'],
  packages          = ['goosempl'],
  cmdclass          = {'install': PostInstallCommand},
  package_data      = {'goosempl/stylelib':[
    'goosempl/stylelib/goose-latex.mplstyle',
    'goosempl/stylelib/goose-tick-in.mplstyle',
    'goosempl/stylelib/goose-tick-lower.mplstyle',
    'goosempl/stylelib/goose.mplstyle'
  ]},
)

# --------------------------------------------------------------------------------------------------
