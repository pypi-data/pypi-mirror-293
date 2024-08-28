from setuptools import setup, find_packages

setup(
    name='ObfusGuard',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
    include_package_data=True,
    description='A multi-layered encryption and hashing algorithm.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rajnish Tripathi',
    author_email='rajnishtripathi2001@gmail.com',
    url='https://github.com/RajnishXCode/ObfusGuard',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
