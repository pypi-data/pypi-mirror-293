from setuptools import setup, find_packages

setup(
    name='fastapi-query-parameter-model',
    version='0.1.2',
    description='A powerful and easy-to-use model for converting camelCase query parameters into snake_case parameters of an object',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pierre DUVEAU',
    author_email='pierre@duveau.org',
    url='https://github.com/PierroD/fastapi-query-parameter-model',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["fastapi", "pydantic"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
