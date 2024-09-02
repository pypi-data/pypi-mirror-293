from setuptools import setup, find_packages

setup(
    name='tineye-python',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
            'requests',
            'json'
    ],
    author='hackerman1337',
    author_email='chuk@chuk.dev',
    description='A Python library for Tineye',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chukfinley/tineye-python',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
