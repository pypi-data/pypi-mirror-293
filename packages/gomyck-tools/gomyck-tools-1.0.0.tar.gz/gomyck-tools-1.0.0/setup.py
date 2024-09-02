from setuptools import setup, find_packages

setup(
  name="gomyck-tools",
  version="1.0.0",
  author="gomyck",
  author_email="hao474798383@163.com",
  description="A ctools for python development",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://blog.gomyck.com",
  packages=["ctools"],  # 自动发现并包含包内所有模块
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.8",  # 指定最低 Python 版本
  install_requires=[        # 你的包依赖的其他包
    "jieba==0.42.1",
    "jsonpickle==3.2.2",
    "SQLAlchemy==2.0.32",
    "paddlepaddle==2.6.1",
    "chardet==5.2.0",
    "psycopg2-binary==2.9.9"
  ],
)
