from setuptools import setup, find_packages

setup(
    name='VineyardUtils',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'simplekml',
        'alphashape',
    ],
    entry_points={
        'console_scripts': [
            'datasampler = vineyardutils.datasampler:main',
            'elevation = vineyardutils.elevation:main',
            'kmlutils = vineyardutils.kmlutils:main',
        ],
    },
    python_requires='>=3.6',
    author='Pierluigi Rossi',
    author_email='pierluigi.rossi@unitus.it',
    description='A Python package for digital agriculture in vineyard-related activities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pierluigirossi86/VineyardUtils',
    license='MIT',
)
