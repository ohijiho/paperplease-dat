#!/usr/bin/env python3
import sys


def read_int(buf, offset):
    i = offset
    for i in range(offset, len(buf)):
        if not ('0' <= tostr(buf[i]) <= '9'):
            break
    else:
        i += 1
    return int(tostr(buf[offset: i])), i - offset


def tostr(x):
    if type(x) == int:
        return chr(x)
    if type(x) == bytes:
        return x.decode('utf-8')
    return x


def parse(buf, offset, context=None):
    if context is None:
        context = {'R': []}
    i = offset
    c = tostr(buf[i])
    i += 1
    if c == 'R':
        x, n = read_int(buf, i)
        return context['R'][x], i - offset + n
    if c == 'a':
        y = []
        while True:
            c = tostr(buf[i])
            if c == 'h':
                return y, i - offset + 1
            x, n = parse(buf, i, context)
            i += n
            y.append(x)
    if c == 'c':
        y = []
        while True:
            c = tostr(buf[i])
            if c == 'g':
                return (y[0], {y[j]: y[j + 1] for j in range(1, len(y), 2)}), i - offset + 1
            x, n = parse(buf, i, context)
            i += n
            y.append(x)
    if c == 'i':
        x, n = read_int(buf, i)
        return x, i - offset + n
    if c == 'o':
        y = []
        while True:
            c = tostr(buf[i])
            if c == 'g':
                return {y[j]: y[j + 1] for j in range(0, len(y), 2)}, i - offset + 1
            x, n = parse(buf, i, context)
            i += n
            y.append(x)
    if c == 'w':
        y = []
        for _ in range(3):
            x, n = parse(buf, i, context)
            i += n
            y.append(x)
        return tuple(y), i - offset
    if c == 'y':
        x, n = read_int(buf, i)
        i += n
        assert tostr(buf[i]) == ':', 'no \':\''
        i += 1
        import urllib.parse
        y = urllib.parse.unquote(tostr(buf[i: i + x]))
        context['R'].append(y)
        return y, i - offset + x
    if c == 'z':
        return 0, 1
    if c == ':':
        x, n = read_int(buf, i)
        return f':{x}', i - offset + n
    raise RuntimeError(i, c)


def dump(tree):
    for row in tree:
        print(row)


def zipbody(obj, body):
    def it():
        i = 0
        for x in obj:
            sz = x['size']
            yield x['name'], body[i: i + sz]
            i += sz
#        assert sz == len(body), 'body not exhausted'
    return it()


def tosize(x, n):
    if type(x) == str:
        x = x.encode('utf-8')
    return x + bytes(n - len(x))


def cattobytes(__iterable):
    return b''.join(x.encode('utf-8') if type(x) == str else x for x in __iterable)


def tarball_header(name, mode, uid, gid, size, mtime, typeflag, linkname, uname, gname, devmajor, devminor, prefix):
    header = tosize(cattobytes([
        tosize(name, 100),
        f'{mode:07o}\0',
        f'{uid:07o}\0',
        f'{gid:07o}\0',
        f'{size:011o}\0',
        f'{mtime:011o}\0',
        '        ',
        typeflag,
        tosize(linkname, 100),
        'ustar  \0',
        tosize(uname, 32),
        tosize(gname, 32),
        tosize(devmajor, 8),
        tosize(devminor, 8),
        tosize(prefix, 155),
    ]), 512)
    chksum = sum(header) & ((1 << (3 * 6)) - 1)
    return header[:148] + f'{chksum:06o}\0 '.encode('utf-8') + header[156:]


def tarball(entries):
    from time import time
    def it():
        yield tarball_header('assets/', 0o755, 1000, 1000, 0, int(time()), '5', '',
            'jiho', 'jiho', '', '', '')
        for name, data in entries:
            yield tarball_header(name, 0o644, 1000, 1000, len(data), int(time()), '0', '',
                'jiho', 'jiho', '', '', '')
            yield data + bytes(-len(data) % 512)
        yield bytes(10240)
    return b''.join(it())


def main(exe, file='Art.dat.dec', dst='dst'):
    if file.endswith('.json'):
        import json
        with open(file) as f:
            data = json.load(f)['assets']
        y, n = parse(data, 0)
        assert n == len(data), 'not exhausted'
        dump(y)
    elif file.endswith('.dat') or file.endswith('.dat.dec'):
        with open(file, 'rb') as f:
            data = f.read()
        n = int.from_bytes(data[:2], byteorder='little')
        header = data[2: 2 + n].replace(b'\n', b'')
        body = data[2 + n:]
        y, n = parse(header, 0)
        assert n == len(header), 'not exhausted'
        dump(y)
        z = zipbody(y, body)
        with open(dst, 'wb') as f:
            f.write(tarball(z))
    else:
        with open(file, 'rb') as f:
            data = f.read().replace(b'\n', b'')
        y, n = parse(data, 0)
        assert n == len(data), 'not exhausted'
        dump(y)


if __name__ == '__main__':
    main(*sys.argv)
