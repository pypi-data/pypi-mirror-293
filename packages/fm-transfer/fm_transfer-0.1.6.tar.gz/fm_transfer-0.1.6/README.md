# FM-Transfer

---
![PyPI - Status](https://img.shields.io/pypi/status/fm-transfer)
![PyPI - License](https://img.shields.io/pypi/l/fm-transfer?color=blue)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fm-transfer)

## A graphical front-end for gg-transfer and quiet-transfer
`fm-transfer` is a graphical front-end written in Python that allows you to send and receive files through a transceiver.
It is designed to directly control the push-to-talk button of devices equipped with a Kenwood connector used by
many Baofeng, Quansheng and many other transceivers.

The PTT conrol happens via a serial interface, by raising/lowering the `DSR` or the 
`RTS` serial signals. A simple circuit can read the status of one of this signals and trigger the PTT.

This hardware is **NOT** mandatory, so you can use this tool without any transceiver: it can be used to 
send/receive data through audio (es. a cable connecting default sound port output to default sound input).

Transmission and reception are performed using two other python packages:
1) `gg-transfer` (https://github.com/matteotenca/gg-transfer) which uses `C/C++` library
[ggwave](https://github.com/ggerganov/ggwave/) (using `pip` a fork of mine is required/installed, [ggwave-wheels](https://github.com/matteotenca/ggwave-wheels/))
2) `quiet-transfer` (https://github.com/matteotenca/quiet-transfer), 
which uses `C/C++` library [quiet-lib](https://github.com/quiet/quiet)

The former implements FSK modulation, the latter implements a lot of modulation algorithms, including GMSK and QAM.

### Installation

The simplest way to install `fm-transfer` and all the needed tools is via `pip`.

#### Windows

The [Microsoft Visual C++ Redistributales](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022) must be installed too.

#### All platforms

Some pre-compiled wheels are provided for `ggwave-wheels` and `quiet-transfer`.

```bash
pip install fm-transfer
```
This will install all the needed dependecies: while `fm-transfer` is pure-Pyton, dependencies are not, and may require
a `C/C++` compiler.

