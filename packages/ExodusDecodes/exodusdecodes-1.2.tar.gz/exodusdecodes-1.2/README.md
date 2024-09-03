# ExodusDecode
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Decode seed.seco file from Exodus, and crack by password ~ to Mnemonic phrase (seed)

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install pycryptodome
pip install Cipherbcrypt
pip install Mnemonic
```
## Using

```Python
from ExodusDecode import ExodusWalletReader
w1 = ExodusWalletReader('wallets\\seed.seco')
data = w1.decrypt('Password')
print(ExodusWalletReader.extract_mnemonic(data))

```

## License
MIT
**Encode Cipherbcrypt group**