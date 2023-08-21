from setuptools import setup


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]


setup(
    name='perdict',
    version='0.1.0',
    description='Persistent dictionary',
    license='MIT',
    packages=['perdict'],
    package_dir={'perdict': 'src'},
    install_requires=get_requirements(),
    package_data={'': ['license']}
)
