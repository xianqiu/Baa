# Baa

Sending warning by email.


Installation
---------------

Use one of the following method:

* pip install
```bash
pip --install baa
pip --install baa --upgrade
```
* clone repository and install with:
```bash
python setup.py install
```

Usage
-----

1. Create `sender.json` and fill the sender account information.

```json
{
  "sender": "baa@163.com",
  "password": "your password",
  "server": "smtp.163.com",
  "port": 465
}
```

2. Put `sender.json` in "main" folder and run the following:

```python
import baa


if __name__ == '__main__':
    b = baa.Baa()
    b.add_receiver('zhangsan@163.com')
    b.send("Hello, world!")
```