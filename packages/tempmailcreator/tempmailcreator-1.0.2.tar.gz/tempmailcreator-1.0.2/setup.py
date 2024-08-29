from setuptools import setup, find_packages

setup(
    name='tempmailcreator',
    version='1.0.2',
    description='A flexible and customizable library for bypassing Google reCAPTCHA v3 challenges, with both synchronous and asynchronous support.',
    author='70L0-0j0',
    author_email='70L0-0j0@lamia.xyz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/70L0-0j0/Mailer',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
