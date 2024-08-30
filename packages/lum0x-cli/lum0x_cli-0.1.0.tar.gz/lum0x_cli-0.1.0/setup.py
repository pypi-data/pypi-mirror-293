from setuptools import setup, find_packages

setup(
    name='lum0x-cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'boto3',
        'requests',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'lum0x=lum0x.cli:cli',
        ],
    },
    package_data={
        'lum0x': ['lum0xhandler.js'],  # 핸들러 파일을 패키지에 포함시킵니다.
    },
    author='lum0x',
    author_email='dev@lum0x.com',
    description='A CLI tool for deploying and managing functions for Lum0x Infrastructure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
