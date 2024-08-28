from setuptools import setup, find_packages
import toml

def readme():
    with open('README_en.md', encoding='utf-8') as f:
        return f.read()

def parse_pipfile(filename):
    """Load requirements from a Pipfile."""
    with open(filename, 'r') as pipfile:
        pipfile_data = toml.load(pipfile)

    requirements = {
        'full': []
    }
    for package, details in pipfile_data.get('packages', {}).items():
        if isinstance(details, dict):
            requirements['full'].append(f"{package}")
            # requirements['full'].append(f"{details['git']}#egg={package}")
        elif '*' not in details:
            requirements['full'].append(f"{package}=={details}")
        else:
            # Handle the case where details are just a version string
            requirements['full'].append(f"{package}")

    return requirements

setup(
    name='moapy',
    version='0.8.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'moapy': ['dgnengine/dll/*.*'],  # your_package/libs/ 디렉토리 내의 모든 .dll 파일을 포함
    },
    description='Midas Open API for Python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='bschoi',
    url='https://github.com/MIDASIT-Co-Ltd/engineers-api-python',
    install_requires=['mdutils', "numpy", "matplotlib"],
    extras_require=parse_pipfile('Pipfile'),
)