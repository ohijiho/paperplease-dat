#!/usr/bin/env python3
import sys


def gen(obj, context=None):
    if context is None:
        context = {'R': {}}
    if type(obj) == dict:
        return 'o' + ''.join(gen(k, context) + gen(v, context) for k, v in obj.items()) + 'g'
    if type(obj) == list:
        return 'a' + ''.join(gen(x, context) for x in obj) + 'h'
    if obj == 0:
        return 'z'
    if type(obj) == int:
        return f'i{obj}'
    if type(obj) == str:
        if obj in context['R']:
            return f'''R{context['R'][obj]}'''
        context['R'][obj] = len(context['R'])
        import urllib.parse
        x = urllib.parse.quote(obj, safe='')
        return f'y{len(x)}:{x}'
    raise RuntimeError(obj)

    if c == 'c':
        y = []
        while True:
            c = tostr(buf[i])
            if c == 'g':
                return (y[0], {y[j]: y[j + 1] for j in range(1, len(y), 2)}), i - offset + 1
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
    if c == ':':
        x, n = read_int(buf, i)
        return f':{x}', i - offset + n


def read_tarball(tar):
    from time import time
    def it():
        i = 0
        while True:
            header = tar[i: i + 512]
            i += 512
            if not any(header):
                if not any(tar[i: i + 512]):
                    return
                continue
            name = header[:100].rstrip(b'\0').decode('utf-8')
            size = int('0o' + header[124:135].decode('utf-8'), 0)
            data = tar[i: i + size]
            i += size + (-size % 512)
            if header[156] in b'0\0':
                yield name, data
    return it()


def main(exe, file='Art-.tar', dst='Art-.dat.dec'):
    with open(file, 'rb') as f:
        entries = list(read_tarball(f.read()))
    header = [{'name': name, 'size': len(data)} for name, data in entries]
    encoded_header = gen(header).encode('utf-8')
    with open(dst, 'wb') as f:
        f.write(len(encoded_header).to_bytes(2, byteorder='little'))
        f.write(encoded_header)
        for name, data in entries:
            f.write(data)


if __name__ == '__main__':
    main(*sys.argv)
