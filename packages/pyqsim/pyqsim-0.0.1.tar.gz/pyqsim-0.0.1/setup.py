
from setuptools import setup, find_packages

setup(
    name='pyqsim',
    version='0.0.1',
    description='Interactive quantum computing simulator',
    author='cykim8811',
    author_email='cykim8811@snu.ac.kr',
    url='https://github.com/cykim8811/pyqsim',
    packages=find_packages(include=['pyqsim']),
    install_requires=['numpy'],
    keywords=['quantum', 'simulator', 'quantum computing'],
    python_requires='>=3.6',
    package_data={}
)
