# _*_ coding:utf-8 _*_

from pathlib import Path
import shutil
from setuptools import setup
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

class MyBuildExt(build_ext):
	def run(self):
		build_ext.run(self)

		build_dir = Path(self.build_lib)
		root_dir = Path(__file__).parent

		target_dir = build_dir if not self.inplace else root_dir

		self.copy_file(Path('zs_backend')/'__init__.py', root_dir, target_dir)
		self.copy_file(Path('zs_backend')/'api/__init__.py', root_dir, target_dir)
		self.copy_file(Path('zs_backend')/'busi/__init__.py', root_dir, target_dir)
		self.copy_file(Path('zs_backend')/'utils/__init__.py', root_dir, target_dir)

	def copy_file(self, path, source_dir, dest_dir):
		if not (source_dir/path).exists():
			return
		shutil.copyfile(str(source_dir/path), str(dest_dir/path))

setup(
	name="admin",
	ext_modules=cythonize(
		[
			Extension("zs_backend.*", ["zs_backend/*.py"]),
			Extension("zs_backend/utils/.*", ["zs_backend/utils/*.py"]),
			Extension("zs_backend/api/.*", ["zs_backend/api/*.py"]),
			Extension("zs_backend/busi/.*", ["zs_backend/busi/*.py"]),
		],
		build_dir="build",
		compiler_directives=dict(
			always_allow_keywords=True
		)
	),
	cmdclass = dict(
		build_ext=MyBuildExt
	),
)
