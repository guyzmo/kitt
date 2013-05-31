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

%(README.rst)s

""" % read('README.rst')

setup(name='KiTT',
      version='1.1',
      description="Kivy Touch Tool",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: Unix',
      ],
      keywords='multitouch gesture management tool',
      author='Bernard `Guyzmo` Pratz',
      author_email='kitt@m0g.net',
      url='http://m0g.net/kitt/',
      license='GPLv3',
      packages=['kitt'],
      zip_safe=False,
      data_files=[('config', ['etc/kitt_config.json',
                              'etc/kitt_gestures.json'])],
      install_requires=[
          'kivy',
          'python-xlib',
          'pyudev',
          #'PyGTK',
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

Please install wnck package if you plan on using the wnck plugin:

    `apt-get install python-wnck`

And don't forget to add kitt to your .xsession/.xinit file!

"""
