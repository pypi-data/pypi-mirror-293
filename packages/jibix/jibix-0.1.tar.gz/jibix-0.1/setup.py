from setuptools import setup, find_packages

setup(
    name='jibix',
    version='0.1',
    packages=find_packages(),
    description='Easy to handle json database manager',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dr3xxine',
    author_email='dr3xxine@gmail.com',
    install_requires=[],  # List any dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)