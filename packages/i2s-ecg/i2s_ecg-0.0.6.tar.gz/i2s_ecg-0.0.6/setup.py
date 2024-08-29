import setuptools
import os
import io

# 读取README.md文件的内容
def read_readme(file_path):
    if os.path.exists(file_path):
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    return 'Add a fallback short description here'

# 确定README文件的路径
readme_path = os.path.join('ecgi2s123', 'README.md')
long_description = read_readme(readme_path)

# 从requirements.txt文件读取依赖
if os.path.exists("requirements.txt"):
    with io.open("requirements.txt", encoding="utf-8") as f:
        install_requires = [line.strip() for line in f if line.strip()]
else:
    install_requires = []

setuptools.setup(
    name="i2s-ecg",
    version="0.0.6",
    author="zou linzhuang",
    license='MIT License',  
    author_email="zoulinzhuang2204@hnu.edu.cn",
    description="ecgi2s123",
    long_description=long_description,
    long_description_content_type="text/markdown",  # 使用Markdown格式
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,  # 自动打包文件夹内所有数据
    # 如果需要包含多个文件可以单独配置 MANIFEST.in
    
    # 如果需要支持脚本方法运行，可以配置入口点
)
