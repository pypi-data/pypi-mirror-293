from setuptools import setup, find_packages
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LoggerManager',
    version='0.1.2',
    description='A module that extends the standard Python logging module.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Amgarak',
    author_email='painkiller_97@mail.ru',
    url='https://vk.com/zloboglaz',
    packages=find_packages(),
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='logging, python, logger',
    license='MIT',
)
