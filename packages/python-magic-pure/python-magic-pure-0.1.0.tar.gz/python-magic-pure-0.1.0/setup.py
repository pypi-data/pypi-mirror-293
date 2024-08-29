from setuptools import setup, find_packages

setup(
    name='python-magic-pure',
    version='0.1.0',
    description='Pure python replacement for python-magic.',
    url='https://github.com/jkapelner/python-magic-pure',
    author='Jordan Kapelner',
    author_email='',
    license='MIT',
    packages=find_packages(),
		python_requires='>=3.7',
    install_requires=[
        'puremagic >= 1.27'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    zip_safe=False
)
