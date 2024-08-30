import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Mits_AI_Dreamers',
    version='2024.0.1',
    author='Madhu Praneeth Lokesh',
    author_email='lokeshreddy2680@gmail.com',
    description='This is Hamming distance, Jaccard coefficient, overlap',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://github.com/madhukm2050/Mits_AI_Dreamers',
    license='',
    install_requires=[
        'psutil',
        'pandas',
        'plotly',
        'matplotlib',
        'resource',
        'validators',
        'urllib3',
        'Pillow',
        'numpy',
        'sphinx',
        'sphinx-rtd-theme',
        'discord.py',
        'networkx',
        'deprecated',
    ],
    extras_require={
        'gpu':  ['cupy', 'pycuda'],
        'spark': ['pyspark'],
        'dev': ['twine', 'setuptools', 'build'],
        'all': ['cupy', 'pycuda', 'pyspark', 'twine', 'setuptools', 'build']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
