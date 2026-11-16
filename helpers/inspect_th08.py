"""Read-only PBGZ inspection, including unencrypted entry payloads.

Archive/decryption algorithm adapted from thpatch/thtk (BSD-style license,
see THIRD_PARTY_NOTICES.md). Plain-entry fallback follows TH08's
FileSystem::TryDecryptFromTable, not a modification to the source archive.
Never writes to the game directory. Extracted content is private research data.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path


def decrypt(data, key, step, block, limit):
    out = bytearray(data)
    size = len(out)
    size = 0 if size < block // 4 else size - (size % block if size % block < block // 4 else 0) - size % 2
    limit = ((limit + block - 1) // block) * block
    end = min(size, limit)
    for start in range(0, end, block):
        count = min(block, end - start)
        increment = (count + 1) // 2
        source = out[start:start + count]
        target = count - 1
        for index in range(count // 2):
            out[start + target] = source[index] ^ key
            out[start + target - 1] = source[index + increment] ^ ((key + step * increment) & 255)
            target -= 2
            key = (key + step) & 255
        if count % 2:
            out[start] = source[count // 2] ^ key
            key = (key + step) & 255
        key = (key + step * increment) & 255
    return bytes(out)


def unlzss(data, size):
    if not 0 <= size <= 64 * 1024 * 1024:
        raise ValueError('Unreasonable decompressed size')
    cursor = 0
    ring = bytearray(8192)
    head = 1
    out = bytearray()

    def bits(count):
        nonlocal cursor
        value = 0
        for _ in range(count):
            if cursor >= len(data) * 8:
                raise ValueError('Truncated LZSS stream')
            value = (value << 1) | ((data[cursor // 8] >> (7 - cursor % 8)) & 1)
            cursor += 1
        return value

    while len(out) < size:
        if bits(1):
            values = [bits(8)]
        else:
            offset = bits(13)
            if offset == 0:
                break
            length = bits(4) + 3
            values = None
        for i in range(len(values) if values is not None else length):
            value = values[i] if values is not None else ring[(offset + i) & 8191]
            out.append(value)
            if len(out) > size:
                raise ValueError('LZSS output exceeds declared size')
            ring[head] = value
            head = (head + 1) & 8191
    if len(out) != size:
        raise ValueError(f'LZSS size mismatch: {len(out)} != {size}')
    return bytes(out)


CRYPT = [(0x4D,0x1B,0x37,0x40,0x2800),(0x54,0x51,0xE9,0x40,0x3000),
         (0x41,0xC1,0x51,0x1400,0x2000),(0x4A,0x03,0x19,0x1400,0x7800),
         (0x45,0xAB,0xCD,0x200,0x1000),(0x57,0x12,0x34,0x400,0x2800),
         (0x2D,0x35,0x97,0x80,0x2800),(0x2A,0x99,0x37,0x400,0x1000)]


def read_archive(archive):
    if archive[:4] != b'PBGZ':
        raise ValueError('Not a TH08 PBGZ archive')
    count, offset, size = struct.unpack('<III', decrypt(archive[4:16], 0x1B, 0x37, 12, 0x400))
    count, offset, size = count - 123456, offset - 345678, size - 567891
    if not 0 < count < 100000 or not 16 <= offset < len(archive):
        raise ValueError('Invalid PBGZ header')
    table = unlzss(decrypt(archive[offset:], 0x3E, 0x9B, 0x80, 0x400), size)
    entries = []
    cursor = 0
    for _ in range(count):
        end = table.index(0, cursor)
        name = table[cursor:end].decode('ascii')
        entry_offset, entry_size, extra = struct.unpack_from('<III', table, end + 1)
        entries.append(dict(name=name, offset=entry_offset, size=entry_size, extra=extra))
        cursor = end + 13
    for index, entry in enumerate(entries):
        entry['stored'] = (entries[index + 1]['offset'] if index + 1 < len(entries) else offset) - entry['offset']
    return entries


def extract(archive, entry):
    raw = unlzss(archive[entry['offset']:entry['offset'] + entry['stored']], entry['size'])
    if raw[:3] != b'edz':
        return raw, 'plain payload (engine fallback)'
    for tag, key, step, block, limit in CRYPT:
        if raw[3] == tag:
            return decrypt(raw[4:], key, step, block, limit), 'edz encrypted payload'
    return raw, 'unknown tag (engine fallback)'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    parser.add_argument('--entry', action='append', default=[])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    archive_path = args.archive.resolve()
    archive = archive_path.read_bytes()
    entries = read_archive(archive)
    report = dict(archive=str(archive_path), sha256=hashlib.sha256(archive).hexdigest(), entry_count=len(entries), samples=[])
    if args.entry and not args.out:
        parser.error('--out is required for entry extraction')
    if args.out:
        out = args.out.resolve()
        if out == archive_path.parent or archive_path.parent in out.parents:
            parser.error('Output must be outside the original game directory')
        out.mkdir(parents=True, exist_ok=True)
    for name in args.entry:
        if Path(name).name != name or '/' in name or '\\' in name:
            parser.error('Only flat entry names are supported')
        entry = next(e for e in entries if e['name'] == name)
        data, mode = extract(archive, entry)
        destination = out / name
        if destination.exists():
            parser.error(f'Refusing to overwrite {destination}')
        destination.write_bytes(data)
        report['samples'].append(dict(name=name, size=len(data), mode=mode, sha256=hashlib.sha256(data).hexdigest()))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
