#!/usr/bin/python
# This patch works around a null pointer dereference in Dragon when custom commands are used with verbose logging.

import hashlib
import sys
import os

sha256 = '5751b887c3515ab050e6262be182b68b32535bcf2339e663e55eda7a213a1706'
patched_sha256 = '15084a5bd7e65e03d8607283041e4a1bdb79a536851cce35197fbbecc8595189'
# jumps around the crashing debug call
patch = (0x001F50F1, '90E9')

dragon = default = '/Applications/Dragon.app/Contents/MacOS/Dragon'
if len(sys.argv) == 2:
    dragon = sys.argv[1]

if not os.path.exists(dragon):
    print('Error: Dragon executable not found at {}'.format(dragon))
    print('Run script again like with a path to Dragon.app/Contents/MacOS/Dragon')
    print('Example: {} {}'.format(sys.argv[0], sys.argv[1]))
    exit(1)

if not os.access(dragon, os.R_OK | os.W_OK):
    print('Error: do not have read+write access to {}. Perhaps run as root?')
    print('Example: sudo {}'.format(' '.join(sys.argv)))
    exit(1)

with open(dragon, 'r+b') as f:
    data = f.read()
    h = hashlib.sha256(data).hexdigest()
    if h == sha256:
        print('[+] Dragon matches 6.0.8 hash')
        for i in xrange(100000):
            path = '{}.bak.{}'.format(dragon, i)
            if not os.path.exists(path):
                print('[+] Backing up to {}'.format(path))
                with open(path, 'wb') as backup:
                    backup.write(data)
                os.chmod(path, 0755)
                print('[+] Backup finished')
                break
        else:
            print('[!] Error: Could not back up Dragon binary, refusing to patch')
            exit(1)
        print('[+] Patching {:#08x} -> {}'.format(*patch))
        addr, b = patch
        b = b.decode('hex')
        f.seek(addr, os.SEEK_SET)
        f.write(b)
        print('[+] Patch complete')
    else:
        if h == patched_sha256:
            print('[!] Error: Dragon already patched.')
        else:
            print('[!] Error: Dragon executable does not match SHA256 hash: found {}, expecting {}'.format(h, sha256))
            print('[!] You must be using an unpatched Dragon 6.0.8 binary')
        exit(1)

with open(dragon, 'r') as f:
    h = hashlib.sha256(f.read()).hexdigest()
    if h == patched_sha256:
        print('[+] Patched file matches correct hash, all done here.')
    elif h == sha256:
        print('[!] Error: The resulting file hash is unchanged, so the patch did not write successfully')
    else:
        print('[!] Critical error: patched file hash is incorrect, perhaps restore the backup:')
        print('[!] Backup: {}'.format(path))
