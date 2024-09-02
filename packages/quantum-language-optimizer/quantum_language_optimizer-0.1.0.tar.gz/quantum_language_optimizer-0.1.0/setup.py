from setuptools import setup, find_packages

# 读取README文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantum_language_optimizer",  # 包名
    version="0.1.0",  # 版本号
    author="C.C.K Leon",  # 作者姓名
    author_email="ckchau1@asu.edu",  # 作者邮箱
    description="A PyPI plugin to optimize large language models using Quantum Neural Networks",  # 简短描述
    long_description=long_description,  # 长描述，从README文件中读取
    long_description_content_type="text/markdown",  # 长描述的内容类型
    url="https://github.com/yourusername/quantum_language_optimizer",  # 项目主页
    packages=find_packages(),  # 自动发现所有的包和子包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python版本要求
    install_requires=[
        "qiskit>=0.29.0",
        "numpy>=1.19.2",
        "torch>=1.7.0",
    ],  # 依赖包
    include_package_data=True,  # 包含数据文件
    entry_points={
        'console_scripts': [
            'quantum_language_optimizer=quantum_language_optimizer.cli:main',
        ],
    },  # 可选：命令行工具入口
)
