import setuptools
import shutil
import subprocess
import os

from glob import glob
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

sourcefiles  = ['src/ShmReader.cc']
headerfiles  = ['ShmReader.hh']
compile_opts = [ '-Iinc',  '-fPIC']#, '-Wall', '-g', '-fabi-version=3', '-std=gnu++98']
linker_opts = []

compiler_kwargs = {
    'sources': sourcefiles,
    'extra_compile_args': compile_opts,
    'extra_link_args': linker_opts,
    'language': 'c++'
}

class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        self.build_dir = Path(self.build_lib)
        self.root_dir = Path(__file__).parent
        self.target_dir = self.build_dir if not self.inplace else self.root_dir
        self.copy_init('condatest')

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return
        shutil.copyfile(str(source_dir / path), str(destination_dir / path))

    def copy_init(self, module_folder: str):
        if not os.path.exists(self.target_dir / module_folder):
            os.makedirs(self.target_dir / module_folder)
        self.copy_file(Path(module_folder) / '__init__.py', self.root_dir, self.target_dir)

def glob_without_init(module_path: str):
    match =  os.path.join(module_path, '*.py')
    return [x for x in glob(match) if '__init__.py' not in x]


ext = [ Extension('condatest.reader_api', **compiler_kwargs) ]

setup(
    name='condatest',
    author='blub',
    version='0.1',
    py_modules=['condatest.rdb'],
    packages=[],
    cmdclass={'build_ext': MyBuildExt},
    ext_modules=ext
)