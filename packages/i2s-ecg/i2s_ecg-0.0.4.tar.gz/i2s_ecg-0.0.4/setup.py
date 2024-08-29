import setuptools
import os
import requests
import io
# 将markdown格式转换为rst格式
# def md_to_rst(from_file, to_file):
#     r = requests.post(url='http://c.docverter.com/convert',
#                       data={'to':'rst','from':'markdown'},
#                       files={'input_files[]':open(from_file,'rb')})
#     if r.ok:
#         with open(to_file, "wb") as f:
#             f.write(r.content)


# md_to_rst("README.md", "README.rst")


if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()
else:
	long_description = 'Add a fallback short description here'
	
if os.path.exists("requirements.txt"):
    install_requires = io.open("requirements.txt").read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name="i2s-ecg",
    version="0.0.4",
    author="zou linzhuang",
    license = 'MIT License',  
    author_email="zoulinzhuang2204@hnu.edu.cn",
    description="ecgi2s123",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(),
    install_requires=[
        'streamlit',
        'Pillow',
        'numpy',
        'scikit-image',
        'matplotlib',
        'scikit-learn',
        'joblib',
        'pandas',
        'natsort',
        'scipy',
        'unzip'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    
    # include_package_data=True,  # 自动打包文件夹内所有数据
    # 如果需要包含多个文件可以单独配置 MANIFEST.in
    
    # 如果需要支持脚本方法运行，可以配置入口点
)

