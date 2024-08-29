from setuptools import setup, find_packages

setup(
    name="cspframework",  # 包名，在PyPI上应该是唯一的，且通常全部小写
    version="0.1.0",  # 版本号，遵循语义化版本控制
    author="qinzhong.wangqz",
    author_email="qinzhong.wangqz@antgroup.com",
    description="A CSP framework on Maya platform for algorithm deployment and inference.",
    long_description=open("README.md").read(),  # 读取README文件内容
    long_description_content_type="text/markdown",  # 指定README的格式
    url="https://code.alipay.com/algo_project/xframework",  # 项目主页
    packages=find_packages(),  # 自动发现所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 指定Python版本要求
    install_requires=[  # 依赖列表，根据requirements.txt生成更佳
        # 'requests',
        # 'numpy',
    ],
)
