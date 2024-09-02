#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
import shutil

class InstallCommand(_install):
    """Custom installation for creating folders and files."""

    def run(self):
        # Run the standard install process
        _install.run(self)

        # Custom post-installation steps
        self.create_command_file()

    def create_command_file(self):
        dir_path = os.path.expanduser('~/Desktop/MonthlyReport1/')
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)

        fpath = os.path.join(dir_path, 'Click_me_Twice2.command')
        with open(fpath, 'w') as hellofile:
            hellofile.write('''#!/usr/bin/env python3
import hfmonthlyreportALL
hfmonthlyreportALL.default()
            ''')

        # Make the file executable (macOS)
        if os.name == 'posix':
            os.chmod(fpath, 0o744)
        print("Done Creating file")

# Read the contents of your README file
with open("README.txt", "r") as f:
    long_description = f.read()

setup(
    name='hfmonthlyreportALL',
    version='0.2',
    description='Send monthly file count only to monthly report server',
    long_description=long_description,
    long_description_content_type='text/plain',  # Use 'text/markdown' if using Markdown
    author='VishalJain_NIOT',
    author_email='vishaljain9516@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.22.0',
        'pyperclip==1.8.2',
        'qrcode>=6.1'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        'install': InstallCommand,
    },
)
