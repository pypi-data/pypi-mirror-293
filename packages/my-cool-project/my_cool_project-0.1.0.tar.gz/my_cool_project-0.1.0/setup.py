from setuptools import setup, find_packages

setup(
    name='my_cool_project',  # Your package name
    version='0.1.0',         # Initial version
    packages=find_packages(),# Automatically find packages in your directory
    install_requires=[],     # List your dependencies here
    description='A simple hello world package from vrutansh...',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/my_cool_project',  # Replace with your repo URL
    author='Vrutansh',
    author_email='vrutansh@test.com',
    license='MIT',  # License of your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
