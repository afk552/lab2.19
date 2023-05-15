#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

if __name__ == "__main__":
    path = pathlib.Path(r"C:\test.txt")
    print(path.name)
    print(path.parent)
    print(path.exists())
