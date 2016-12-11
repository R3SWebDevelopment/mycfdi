import sys
import hashlib
from django.core.files.uploadedfile import InMemoryUploadedFile

def collapse_white_spaces(value=None):
    value_retorned = None
    if value is not None and value.__class__ is str and value.strip():
        value_retorned = value.strip()
    return value_retorned

def hash_file(file=None):
    md5 = None
    sha1 = None
    if file is not None:
        BUF_SIZE = 65536
        if file.__class__ is InMemoryUploadedFile:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            data = file.read(BUF_SIZE)
            md5.update(data)
            sha1.update(data)
        else:
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            try:
                with open(file) as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)
                        sha1.update(data)
            except Exception,e:
                print "e: %s" % e
    #            pass
    return md5, sha1