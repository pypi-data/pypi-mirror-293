import setuptools
import re
import requests
from bs4 import BeautifulSoup
 
package_name = "pingpkg"
package_version = '0.0.1'
 
def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()
 
    setuptools.setup(
        name=package_name,
        version=package_version,
        author="xizhao_li",  # 作者名称
        author_email="hard_rock_l@163.com", # 作者邮箱
        description="Used to ping network devices", # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://pypi.org/project/pingpkg/", # 库的官方地址
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"], # pingpkg库依赖的其他库
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )
 
 
def main():
    try:
        upload()
        print("Upload success , Current VERSION:", package_version)
    except Exception as e:
        raise Exception("Upload package error", e)
 
 
if __name__ == '__main__':
    main()