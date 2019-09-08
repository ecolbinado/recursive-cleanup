#! python3
# mrdup.py - Accepts a path/directory as an argument and deletes all duplicate files within the directory and all its subdirectories.

import sys, os, hashlib

def hashing(path, size=65536):
    file = open(path, 'rb')
    hasher = hashlib.md5()
    slice = file.read(size)
    while len(slice) > 0:
        hasher.update(slice)
        slice = file.read(size)
    file.close()
    return hasher.hexdigest()

def dlookup(path):
    originals = {}
    duplicates = []
    for folder, subdirs, files in os.walk(path):
        for file in files:
            chkfile = os.path.join(folder, file)
            hashedfile = hashing(chkfile)
            if hashedfile not in originals:
                originals[hashedfile]= chkfile
            else:
                duplicates.append(chkfile)
    return originals, duplicates

if __name__ == '__main__':
    try:
        if os.path.exists(sys.argv[1]):
            origfiles, dupfiles = dlookup(sys.argv[1])
            for file in dupfiles:
                os.remove(file)
            print("Success! Duplicate files have been removed.")
            sys.exit()
        else:
            print('Please check. It seems {} is not a valid path.'.format(sys.argv[1]))
    except IndexError:
        print("mrdup.py must be used with one argument.")