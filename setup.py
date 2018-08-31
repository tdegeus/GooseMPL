
from setuptools                 import setup
from setuptools.command.install import install

# --------------------------------------------------------------------------------------------------

class PostInstallCommand(install):

  def run(self):

    import goosempl
    goosempl.copy_style()

    install.run(self)

# --------------------------------------------------------------------------------------------------

__version__ = '0.2.3'

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
)

# --------------------------------------------------------------------------------------------------
