from pathlib import Path
from setuptools import setup

setup_py_file = Path(__file__).resolve()
repo_root = setup_py_file.parent
requirements_path = repo_root / 'requirements.txt'
requirements = requirements_path.read_text().strip().splitlines()

setup(
    name='GLHE',
    version='0.1',
    author="Matt Mitchell",
    author_email="mitchute@gmail.com",
    packages=[
        'glhe',
        'glhe.aggregation',
        'glhe.g_function',
        'glhe.ground_temps',
        'glhe.input_processor',
        'glhe.interface',
        'glhe.output_processor',
        'glhe.profiles',
        'glhe.properties',
        'glhe.standalone',
        'glhe.topology',
        'glhe.utilities',
    ],
    license='MIT',
    install_requires=requirements,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={'console_scripts': ['glhe=glhe.standalone.plant_loop:main',]}
)
