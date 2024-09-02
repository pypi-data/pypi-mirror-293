from setuptools import setup, find_packages

setup(
    name='Mensaje-CEGM',
    version='7.0',
    description='Un paquete de saludos y despedidas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Carolina Gómez Muñoz',
    author_email='cgomez33@ucol.mx',
    url='',
    licence_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',

    ]
)


