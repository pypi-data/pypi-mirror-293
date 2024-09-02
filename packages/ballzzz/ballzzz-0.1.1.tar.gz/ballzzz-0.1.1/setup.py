from setuptools import setup, find_packages

setup(
    name='ballzzz',
    version='0.1.1',
    py_modules=['gameee'],  # Use py_modules if your project is a single file
    install_requires=[
        'pygame',  # Only third-party packages
    ],
    entry_points={
        'console_scripts': [
            'ballzzz=gameee:main',  # Command 'ballzzz' maps to 'main' function in 'gameee.py'
        ],
    },
    author='Harshini',
    author_email='harshini8564@gmail.com',
    description='A simple moving-to-destination game',
    long_description=open('README.md').read(),  # If you have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/hars884/balz.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)

