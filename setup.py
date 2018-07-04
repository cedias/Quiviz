from setuptools import setup

setup(name='quiviz',
      version='0.0',
      description='wannabe xp-logger',
      url='http://github.com/cedias/Quiviz',
      author='cedias',
      author_email='me@mymail.com',
      license='MIT',
      packages=['quiviz'],
      install_requires=["wrapt", "visdom"],
      zip_safe=False)
