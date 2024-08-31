from setuptools import setup, find_packages

setup(
    name='ballz2',  # This will be the name of your package
    version='0.1',
    packages=find_packages(),  # Automatically finds all packages in the directory
    install_requires=[
        # List your dependencies here (if any), e.g., 'numpy', 'requests',
    ],
    entry_points={
        'console_scripts': [
            'ballz2=ballz2.ballz2:main',  # This makes your script callable from the command line
        ],
    },
    author='Harshini',
    author_email='harshini8564@gmail.com',
    description='hope you enjoy it ',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Adjust to your Python version requirements
)
'''long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',  # Link to your repository (if any)'''