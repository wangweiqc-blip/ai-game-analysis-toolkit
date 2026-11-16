"""Offline command dispatcher. All paths resolve from the delivered folder."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import webbrowser

ROOT = Path(__file__).resolve().parent
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def registry():
    return json.loads((ROOT / 'toolkit.json').read_text(encoding='utf-8'))

def environment(data):
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    env['DOTNET_ROOT'] = str(ROOT / 'runtime/dotnet')
    env['DOTNET_CLI_HOME'] = str(ROOT / 'work/dotnet-home')
    env['DOTNET_CLI_TELEMETRY_OPTOUT'] = '1'
    env['DOTNET_SKIP_FIRST_TIME_EXPERIENCE'] = '1'
    env['NUGET_PACKAGES'] = str(ROOT / 'cache/nuget')
    env['DOTNET_BUNDLE_EXTRACT_BASE_DIR'] = str(ROOT / 'work/dotnet-bundle')
    paths = [str(ROOT / 'runtime/dotnet'), str(ROOT / 'runtime/python'), str(ROOT / 'runtime/python/Scripts')]
    java = data.get('java_home')
    if java:
        env['JAVA_HOME'] = str(ROOT / java)
        paths.insert(0, str(ROOT / java / 'bin'))
    env['PATH'] = os.pathsep.join(paths + [env.get('PATH', '')])
    return env

def command(entry):
    return [arg.replace('{root}', str(ROOT)) for arg in entry.get('command', [])]

def ai_config():
    return json.loads((ROOT / 'ai-config.json').read_text(encoding='utf-8'))

def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))

def automation(entry, config):
    spec = config['tools'].get(entry['id'], {'kind': 'unclassified'})
    result = {**config['kinds'].get(spec['kind'], {}), **spec}
    result['local_docs'] = [str(ROOT / p) for p in spec.get('local_docs', [])]
    return result

def file_check(entry, data):
    paths = [ROOT / p for p in entry.get('check_paths', [])]
    paths.extend(Path(p) for p in command(entry) if Path(p).is_absolute())
    # The dispatcher configures these bundled runtimes for their respective tools.
    ident = entry['id']
    if ident in ('ghidra', 'ghidra-headless', 'jadx', 'jadx-gui', 'apktool'):
        paths.append(ROOT / data['java_home'] / 'bin/java.exe')
    if ident in ('ilspy', 'ilspycmd', 'mesen', 'cue4parse', 'dotnet'):
        paths.append(ROOT / 'runtime/dotnet/dotnet.exe')
    missing = sorted({str(p) for p in paths if not p.exists()})
    return {'files_present': bool(paths) and not missing, 'missing_paths': missing,
            'scope': 'entry-files-and-known-runtimes-only'}

def ai_entry(entry, data, config, detail=False):
    evidence = entry.get('verification', {})
    result = {key: entry.get(key) for key in ('id', 'name', 'platform', 'version')}
    result.update({
        'automation': automation(entry, config),
        'availability': file_check(entry, data),
        'verification': {key: evidence.get(key) for key in ('test', 'passed', 'summary')},
    })
    if detail:
        result = {**entry, **result,
                  'verification': evidence,
                  'resolved_command': command(entry),
                  'invoke_argv': [str(ROOT / 'runtime/python/python.exe'), str(ROOT / 'toolkit.py'),
                                  'run', entry['id'], '--'] if entry.get('command') else [],
                  'working_directory': str(ROOT / entry.get('cwd', 'work/' + entry['id'])),
                  'local_folder': str(ROOT / entry['folder']) if entry.get('folder') else None}
    return result

def launch(entry, extra, data):
    cmd = command(entry)
    if not cmd or not Path(cmd[0]).is_file():
        print('该条目没有可运行入口。请查看 info 中的本地说明。')
        return 2
    if extra and extra[0] == '--':
        extra = extra[1:]
    cmd += extra
    cwd = ROOT / entry.get('cwd', 'work/' + entry['id'])
    cwd.mkdir(parents=True, exist_ok=True)
    if Path(cmd[0]).suffix.lower() in ('.bat', '.cmd'):
        # Batch files run via cmd.exe; reject shell metacharacters in user arguments.
        if any(any(c in a for c in '&|<>^%!\r\n') for a in extra):
            raise ValueError('批处理参数含 shell 特殊字符；请改用不含这些字符的工作副本路径。')
    options = {}
    if os.name == 'nt' and os.environ.get('GAME_TOOLKIT_HIDDEN') == '1':
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
        options['startupinfo'] = startup
    return subprocess.call(cmd, cwd=cwd, env=environment(data), **options)

def main():
    parser = argparse.ArgumentParser(description='本地游戏解析工具库；查询、调用均无需联网。')
    parser.add_argument('action', choices=['catalog', 'route', 'check', 'list', 'info', 'run', 'doctor', 'verify-cache', 'open', 'menu'], nargs='?', default='catalog')
    parser.add_argument('target', nargs='?')
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    data = registry()
    entries = data['tools']
    if args.action in ('catalog', 'route', 'check', 'info'):
        config = ai_config()
        if args.action in ('catalog', 'route'):
            query = (args.target or '').strip().casefold()
            routes = [r for r in config['routes'] if not query or any(
                query in str(r[k]).casefold() for k in ('id', 'platform', 'keywords'))]
            if args.action == 'route':
                emit({'schema_version': 1, 'root': str(ROOT), 'routes': routes,
                      'note': '平台候选路线；先核对实际文件与版本，不是游戏格式自动识别结果。'})
                return 0
            routed_ids = {ident for route in routes for ident in route['tools']} if query else set()
            selected = [e for e in entries if not query or e['id'] in routed_ids or any(
                query in str(e.get(k, '')).casefold() for k in ('id', 'name', 'platform', 'use'))]
            emit({'schema_version': 1, 'root': str(ROOT), 'query': query,
                  'tools': [ai_entry(e, data, config) for e in selected]})
            return 0
        if args.action == 'check':
            selected = [e for e in entries if not args.target or e['id'] == args.target]
            if not selected:
                emit({'error': 'unknown_tool', 'id': args.target})
                return 2
            checks = [{'id': e['id'], **file_check(e, data)} for e in selected]
            emit({'schema_version': 1, 'checks': checks,
                  'note': '只检查本地文件，不启动软件；不代表已验证目标游戏或自动化接口。'})
            return int(any(not e['files_present'] for e in checks))
        entry = next((e for e in entries if e['id'] == args.target), None)
        if entry is None:
            emit({'error': 'unknown_tool', 'id': args.target})
            return 2
        emit(ai_entry(entry, data, config, detail=True))
        return 0
    if args.action == 'open':
        webbrowser.open((ROOT / 'index.html').as_uri())
        return 0
    if args.action == 'menu':
        choices = [x for x in entries if x.get('command')]
        print('本地游戏解析工具库\n')
        for i, item in enumerate(choices, 1):
            print(f'{i:2}. {item["name"]} [{item["id"]}]')
        print(' 0. 退出')
        try:
            selected = int(input('\n输入编号：'))
        except (ValueError, EOFError):
            return 0
        if 1 <= selected <= len(choices):
            return launch(choices[selected-1], [], data)
        return 0
    if args.action == 'list':
        query = (args.target or '').casefold()
        for item in entries:
            if not query or query in json.dumps(item, ensure_ascii=False).casefold():
                print(f'{item["id"]:18} {item["name"]} | {item["platform"]} | {item["status"]}')
        return 0
    if args.action == 'doctor':
        missing = []
        for item in entries:
            paths = item.get('check_paths', [])
            ok = bool(paths) and all((ROOT / p).exists() for p in paths)
            print(('OK   ' if ok else 'MISS ') + item['id'] + ' — ' + item['status'])
            if not ok:
                missing.append(item['id'])
        print(f'\n目录：{ROOT}\n文件检查缺失：{len(missing)}。功能验证记录见 logs/verification.json。')
        return 1 if missing else 0
    if args.action == 'verify-cache':
        bad = []
        for item in data.get('downloads', []):
            path = ROOT / 'cache' / item['name']
            if not path.exists():
                print('缓存已移除 ' + item['name'])
                continue
            with path.open('rb') as f:
                digest = hashlib.file_digest(f, 'sha256').hexdigest()
            if digest != item['actual_sha256']:
                bad.append(item['name'])
        print(json.dumps({'mismatched': bad}, ensure_ascii=False))
        return int(bool(bad))
    entry = next((x for x in entries if x['id'] == args.target), None)
    if entry is None:
        parser.error('请先用 list 查看工具 ID。')
    return launch(entry, args.arguments, data)

if __name__ == '__main__':
    sys.exit(main())
