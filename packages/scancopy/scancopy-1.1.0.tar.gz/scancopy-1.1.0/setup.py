# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

 
setup(
    name="scancopy",
    version="1.1.0",
    author="jiaobenxiaozi",
    author_email="183732521@qq.com",
    description="scancopy",
 
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'tkinter ' 
    ],
 
    python_requires='>=3.6',
    # entry_points={
    #     'console_scripts': [
    #         'dp = DrissionPage.commons.cli:main',
    #     ],
    # },
)
