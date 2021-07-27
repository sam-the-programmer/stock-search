'''from cx_Freeze import setup, Executable

executables = [
    Executable('main.py')
]

packages = ['pandas', 'tensorflow', 'numpy', 'sklearn']
includefiles = []

setup(
    name = 'Stock Search',
    version = '0.0.1',
    description = 'This AI tool allows you to see stocks throughout time.',
    executables = executables,
    options = {
        'build_exe': {'packages':packages,'include_files':includefiles},
        'bdist_msi': {'initial_target_dir': r'[ProgramFilesFolder]\%s' % ('Stock Search')}
    }
)'''

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("main.py"),
    compiler_directives={'language_level' : "3"}
)