from setuptools import setup, find_packages

install_requires = ['pymarc']

classifiers = """
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: BSD License
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Development Status :: 4 - Beta
"""

setup(
    name = 'worldcat',
    version = '0.2.5',  # remember to update worldcat/__init__.py on release!
    url = 'http://matienzo.org/project/worldcat',
    author = 'Mark A. Matienzo',
    author_email = 'mark@matienzo.org',
    license = 'GPL/BSD',
    packages = find_packages(),
    install_requires = install_requires,
    description = 'Interact with OCLC\'s WorldCat Affiliate APIs',
    classifiers = filter(None, classifiers.split('\n')),
)
