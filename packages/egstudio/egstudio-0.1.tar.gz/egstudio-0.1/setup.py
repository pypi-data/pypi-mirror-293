from setuptools import setup, find_packages

setup(
    name='egstudio',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='vrutansh',
    author_email='your.email@example.com',
    description='A brief description of your package',
    # url='https://github.com/yourusername/your-repo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify your Python version requirement
)