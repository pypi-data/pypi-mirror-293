from setuptools import setup, find_packages
from dcs_code_injector import VERSION

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

data_files_to_include = ["*.png", "*.jpg", "*.xml"]

setup(
    name='dcs-code-injector',
    version=VERSION,
    packages=find_packages(),
    package_data={
        "": data_files_to_include,
    },
    url='https://www.github.com/nielsvaes/dcs_code_injector',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ez-icons", "PySide6>6.7.0", "ez_qt", "ez_settings", "ez_utils", "qt_material", "pygtail", "requests"],
    license='GNU v3',
    author='Niels Vaes',
    author_email='nielsvaes@gmail.com',
    description='A REPL to use with Digital Combat Simulator to execute code while a mission is running.',

    entry_points={'console_scripts': ['dcs-code-injector=dcs_code_injector.app:main']},
    python_requires='>=3.9',
    platforms=['win32', 'nt', 'Windows'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Utilities',
    ],
)
