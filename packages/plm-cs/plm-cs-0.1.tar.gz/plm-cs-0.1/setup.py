from setuptools import setup, find_packages

setup(
    name='plm-cs',
    version='0.1',
    description='Protein chemical shift prediction based on Protein Language Model',
    author='Zhu He',
    author_email='2260913071@qq.com',
    url='https://github.com/doorpro/predict-chemical-shifts-from-protein-sequence.git',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'plm-cs = CS_predict:main'
        ]
    },
    install_requires=[
        'pandas',
        'torch',
        'esm',
    ],
)