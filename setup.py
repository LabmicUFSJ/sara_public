"""
Setup file
LabMic UFSJ 2021
Carlos Barbosa
"""
from setuptools import setup


def read_requirements(path_to_requires='requirements.txt'):
    """read requirements."""
    with open(path_to_requires) as arq:
        return [i.strip() for i in arq]


packages = [
    "sara",
    "sara.core",
    "sara.core.bot_model",
    "sara.core.sara_file",
    "sara.core.mongo",
    "sara.core.network_generators",
    "sara.sentimento",
    "sara.stopwords",
    "sara.stopwords.stopwords_txt",
    "sara.credentials",
    "sara.utils"
]

install_requires = read_requirements()

setup(
    name='sara',
    packages=packages,
    version='0.0.3',
    description='Sara framework to analysis online social networks',
    author='Carlos Barbosa',
    license='MIT',
    install_requires=install_requires,
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'sara=sara.main:main'
        ]
    }
)
