import cli
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools import setup, find_packages

long_description = "test:registro"
requirements = parse_requirements('requirements.txt', session=False)
install_requires = [str(r.req) for r in requirements]

setup(
    name             = 'test:postulant',
    description      = 'Test:Postulant de Aptitus.',
    packages         = find_packages(),
    package_data     = {
        'cli': [
            '*.yaml',
            'templates/*.html'
        ]
    },
    author           = 'Aptitus',
    author_email     = 'aptitus [at] orbis.com.pe',
    scripts          = ['bin/cli'],
    install_requires = install_requires,
    version          = cli.__version__,
    url              = 'https://',
    license          = "MIT",
    zip_safe         = False,
    keywords         = "postulant, registro, rapido, cli, task, test",
    long_description = long_description,
    classifiers      = [
                        'Development Status :: 4 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Topic :: Software Development :: Build Tools',
                        'Topic :: Software Development :: Libraries',
                        'Topic :: Software Development :: Testing',
                        'Topic :: Utilities',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: POSIX',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 2.7',
                      ]
)
