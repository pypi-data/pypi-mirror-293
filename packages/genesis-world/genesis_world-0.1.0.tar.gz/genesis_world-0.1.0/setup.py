from setuptools import setup, find_packages

setup(
    name='genesis_world',
    version='0.1.0',
    description='A simple example package for genesis-world',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # author='Your Name',
    # author_email='your.email@example.com',
    # url='https://github.com/yourusername/examplepackage',
    packages=find_packages(),
    install_requires=[
        # list your package dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
