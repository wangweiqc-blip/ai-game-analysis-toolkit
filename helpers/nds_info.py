"""Read-only NDS file inventory, using the locally installed ndspy."""
import argparse
import json
from pathlib import Path
import ndspy.rom

ap = argparse.ArgumentParser(description='列出 NDS ROM 内部文件，不修改原始文件。')
ap.add_argument('rom', type=Path)
args = ap.parse_args()
rom = ndspy.rom.NintendoDSRom.fromFile(str(args.rom))
data = {'name': rom.name.decode('ascii', errors='replace'), 'game_code': rom.idCode.decode('ascii', errors='replace'),
        'files': [{'id': i, 'name': rom.filenames.filenameOf(i), 'bytes': len(b)} for i, b in enumerate(rom.files)]}
print(json.dumps(data, ensure_ascii=False, indent=2))
