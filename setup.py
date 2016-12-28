
from distutils.core import setup

setup(name='kiskadee',
      version='0.1',
      description='continuous static analysis tool \
                which writes the analyses \
                results into a Firehose database',
      author='Athos Ribeiro, David Carlos',
      author_email='athoscr@fedoraproject.org, ddavidcarlos1392',
      url='https://github.com/LSS-USP/kiskadee',
      install_requires = [
          'fedmsg',
          'docker'
          ]
     )
