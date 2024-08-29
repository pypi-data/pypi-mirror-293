import os
import platform
import setuptools


try:
    import stackless
except ImportError:
    pass
else:
    # The only reason for this is us abusing Py_TPFLAGS reserved
    # for Stackless. That's most likely a temporary limitation.
    raise RuntimeError('memhive is not compatible with Stackless.')


# Minimal dependencies required to test immutables.
TEST_DEPENDENCIES = [
    # pycodestyle is a dependency of flake8, but it must be frozen because
    # their combination breaks too often
    # (example breakage: https://gitlab.com/pycqa/flake8/issues/427)
    'flake8~=5.0.4',
    'pycodestyle~=2.9.1',
    'mypy==0.971',
    'pytest~=6.2.4',
]

EXTRA_DEPENDENCIES = {
    'test': TEST_DEPENDENCIES,
}

CFLAGS = []
if "DEBUG_MEMHIVE" not in os.environ:
    CFLAGS.append('-O2')
else:
    CFLAGS.append('-O0')
if platform.uname().system != 'Windows':
    CFLAGS.extend(['-std=c11', '-fsigned-char', '-Wall',
                   '-Wsign-compare', '-Wconversion'])


with open(os.path.join(
        os.path.dirname(__file__), 'memhive', '_version.py')) as f:
    for line in f:
        if line.startswith('__version__ ='):
            _, _, version = line.partition('=')
            VERSION = version.strip(" \n'\"")
            break
    else:
        raise RuntimeError(
            'unable to read the version from memhive/_version.py')


if platform.python_implementation() == 'CPython':
    if "DEBUG_MEMHIVE" in os.environ:
        define_macros = []
        undef_macros = ['NDEBUG']
    else:
        define_macros = [('NDEBUG', '1')]
        undef_macros = []

    ext_modules = [
        setuptools.Extension(
            "memhive.core._core",
            [
                "memhive/core/queue.c",
                "memhive/core/track.c",
                "memhive/core/refqueue.c",
                "memhive/core/module.c",
                "memhive/core/memhive.c",
                "memhive/core/sub.c",
                "memhive/core/utils.c",
                "memhive/core/map.c",
                "memhive/core/errormech.c",
            ],
            extra_compile_args=CFLAGS,
            define_macros=define_macros,
            undef_macros=undef_macros
        )
    ]
else:
    ext_modules = []



setuptools.setup(
    name='hive',
    version=VERSION,
    description='Memory Hive',
    long_description='',
    python_requires='>=3.12',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.12',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    author='EdgeDB Inc.',
    author_email='yselivanov@gmail.com',
    url='https://github.com/edgedb/memhive',
    license='Apache License, Version 2.0',
    packages=['memhive'],
    provides=['memhive'],
    include_package_data=True,
    ext_modules=ext_modules,
    extras_require=EXTRA_DEPENDENCIES,
)
