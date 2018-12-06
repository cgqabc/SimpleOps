#! /usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
# Create your views here.
def hash_code(code,salt='mysalt'):
    h = hashlib.sha256()
    code += salt
    h.update(code.encode()) #update方法只接受bytes类型
    print h.hexdigest()
hash_code('123456')