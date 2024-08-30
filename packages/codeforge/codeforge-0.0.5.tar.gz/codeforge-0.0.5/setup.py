from setuptools import setup, find_packages

setup(
    name="codeforge",  # 应用版本
    version="0.0.5",  # 版本号
    packages=find_packages(),  # 包括在安装包内的 Python 包
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)
