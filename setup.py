from setuptools import setup
import os
import sys


def read(*names):
    values = dict()
    for name in names:
        if os.path.isfile(name):
            value = open(name).read()
        else:
            value = ''
        values[name] = value
    return values

long_description = """

%(README)s

""" % read('README')

setup(name='KiTT',
      version='1.0',
      description="Kivy Touch Tool",
      long_description=long_description,
      # classifiers=[],
      keywords='multitouch gesture management tool',
      author='Bernard `Guyzmo` Pratz',
      author_email='kitt@m0g.net',
      url='http://m0g.net/kitt/',
      license='GPLv3',
      packages=['kitt'],
      zip_safe=False,
      install_requires=[
          'kivy',
          'argparse',
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      kitt = kitt.kitt:run
      """,
      )

if "install" in sys.argv:
    print """
Kitt is now installed!

Please install wnck package:

    `apt-get install python-wnck`

Don't forget to add kitt to your .xsession/.xinit file!

"""
