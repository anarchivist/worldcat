from setuptools import setup, find_packages

install_requires = []

classifiers = """
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: BSD License
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Development Status :: 3 - Alpha 
"""

setup( 
    name = 'worldcat',
    version = '0.1.4',  # remember to update worldcat/__init__.py on release!
    url = 'http://matienzo.org/project/worldcat',
    author = 'Mark A. Matienzo',
    author_email = 'mark@matienzo.org',
    license = 'GPL/BSD',
    packages = find_packages(),
    install_requires = install_requires,
    description = 'Interact with OCLC\'s WorldCat Search and xID APIs',
    classifiers = filter(None, classifiers.split('\n')),
)
