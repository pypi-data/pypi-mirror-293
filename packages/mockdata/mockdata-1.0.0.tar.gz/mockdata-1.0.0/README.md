### 项目描述

mockdata 是一个 Python 库，用于生成模拟数据。它包含各种字段，如姓名、地址、电话号码等，可以用于测试、演示和开发。

### 安装步骤
* 从pypi安装
```
pip install mockdata
```
* 从源码安装
```
https://github.com/Joyamon/mockdata.git
cd mockdata
python setup.py
```
### 项目目录说明
```
mockdata
    ├── __init__.py
    ├── fields
       │   ├── __init__.py
       │   ├── mock_address.py
       │   ├    ......
       └── setup.py
       └── README.md
       └── requirements.txt
    ├── img
      └── image.png
    ├── utils
      └── __init__.py
       └── convert.py    # base64转图片
    ├── bank.json

```

### 使用方法

```
from mockdata.fields.mock_address import MockAddress

if __name__ == '__main__':
    # 实例化
    ma = MockAddress()
    # 调用方法
    address = ma.mock_address()
    # 输出结果
    print(address)
    
```

### License

MIT

