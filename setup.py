from setuptools import setup, find_packages

install_requires = []

classifiers = """
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Development Status :: 1 - Planning
"""

setup( 
    name = 'worldcat',
    version = '0.0.3',  # remember to update worldcat/__init__.py on release!
    url = 'http://svn.matienzo.org/public/python/worldcat',
    author = 'Mark A. Matienzo',
    author_email = 'mark@matienzo.org',
    license = 'GPL',
    packages = find_packages(),
    install_requires = install_requires,
    description = 'Interact with OCLC\'s WorldCat Search and xID APIs',
    classifiers = filter(None, classifiers.split('\n')),
)