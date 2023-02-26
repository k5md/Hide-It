import PyInstaller.__main__
import os
import shutil
import platform
import contextlib
from src.hide_it.__about__ import (
    __version__,
    __title__,
)

project_name = __title__

approot = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(approot, 'src')
build_dir = os.path.join(approot, 'build')
dist_dir = os.path.join(approot, 'dist')

"""
    NOTE: to understand reasons of multiple ugly builds being present instead of one,
    check 7 y.o issues with pyinstaller multi-executable builds support, starting from
    https://github.com/pyinstaller/pyinstaller/issues/167
"""

data = [
    (os.path.join(src_dir, project_name, 'locales'), os.sep.join(['locales'])),
    (os.path.join(src_dir, project_name, 'assets'), os.sep.join(['assets'])),
    ]
data_zipped = [ ('--add-data', os.pathsep.join(entry)) for entry in data ] # https://pyinstaller.readthedocs.io/en/stable/spec-files.html#adding-data-files
data_flat = [ item for sublist in data_zipped for item in sublist ]

builds = [
    {
        'entry': os.path.join(src_dir, project_name, '__main__.py'),
        'name': project_name,
        'data': data_flat,
        'console': '--noconsole',
        'icon': os.path.join(src_dir, project_name, 'assets', '%s.ico' % project_name),
    }
]

for build in builds:
    arguments = [
        build['entry'],
        '--name', build['name'],
        build['console'],
        '--onedir',
        '--distpath', dist_dir,
        '--clean',
        '--noconfirm',
        '--icon', build['icon']
    ]
    if 'data' in build: arguments += build['data']

    PyInstaller.__main__.run(arguments)

    artifact_dir = os.path.join(approot, 'artifacts')
    archive_name = '_'.join([build['name'], platform.system(), __version__]).lower()
    archive_file = '%s.zip' % archive_name
    archive_path = os.path.join(artifact_dir, archive_file)
    archive_path_temp = os.path.join(approot, archive_file)

    if not os.path.exists(artifact_dir): os.mkdir(artifact_dir)
    if os.path.exists(archive_path): os.remove(archive_path)
    if os.path.exists(archive_path_temp): os.remove(archive_path_temp)

    shutil.make_archive(archive_name, 'zip', os.path.join(dist_dir, build['name']))
    shutil.move(os.path.join(approot, archive_file), artifact_dir)
