from pkg_resources import parse_version
from configparser import ConfigParser
import setuptools

# assert parse_version(setuptools.__version__) >= parse_version("36.2")

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]
requirements = cfg.get("requirements", "").split()

setuptools.setup(
    name="codeforge",  # 应用版本
    version="0.0.11",  # 版本号
    packages=setuptools.find_packages(),  # 包括在安装包内的 Python 包
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
