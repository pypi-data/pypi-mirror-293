from setuptools import setup, find_packages

setup(
    name='bitmoro',
    version='0.1.0',
    author='Bitmoro Nepal',
    author_email='sunab@nestnepal.com.np',
    description='A package for handling messaging and OTP functionalities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bitmoro',  # Update with your GitHub URL
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)