from setuptools import setup, find_packages

setup(
    name='customexcelread_1',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    author='Aravind',
    author_email='aravind@gmail.com',
    description='A brief description of my library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/my_library',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
