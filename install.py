#!/usr/bin/env python3
"""Install theme assets locally; preserve existing compositor configuration."""
import argparse
import os
from pathlib import Path
import shutil
import datetime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    home = Path.home()
    config = Path(os.environ.get('XDG_CONFIG_HOME') or home / '.config')
    data = Path(os.environ.get('XDG_DATA_HOME') or home / '.local/share')
    backup = data / 'madara-rice/backups' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    mappings = [
        ('themes/madara.json', config / 'DankMaterialShell/themes/madara.json'),
        ('niri/style.kdl', config / 'niri/madara-style.kdl'),
        ('kitty/madara.conf', config / 'kitty/madara.conf'),
        ('fastfetch/madara.jsonc', config / 'fastfetch/madara.jsonc'),
        ('fastfetch/sharingan.txt', config / 'fastfetch/sharingan.txt'),
        ('fastfetch/madara-kitty.jsonc', config / 'fastfetch/madara-kitty.jsonc'),
        ('fastfetch/sharingan.png', config / 'fastfetch/sharingan.png'),
        ('wallpapers/madara.png', data / 'madara-rice/madara.png'),
    ]

    def write(destination, contents):
        if destination.is_symlink():
            raise SystemExit(f'Refusing to overwrite symlink: {destination}')
        if destination.exists():
            if destination.read_bytes() == contents:
                print(f'Unchanged: {destination}')
                return
            saved = backup / str(destination).lstrip('/')
            print(f'Backup: {destination} -> {saved}')
            if not args.dry_run:
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, saved)
        print(f'Install: {destination}')
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contents)

    # Check all destinations before performing writes.
    destinations = [p for _, p in mappings] + [config / 'kitty/kitty.conf', config / 'niri/config.kdl']
    for destination in destinations:
        if destination.is_symlink() or any(p.is_symlink() for p in destination.parents):
            raise SystemExit(f'Refusing symlink destination; integrate manually: {destination}')
    for relative, destination in mappings:
        write(destination, (source / relative).read_bytes())

    kitty = config / 'kitty/kitty.conf'
    existing = kitty.read_text() if kitty.exists() else ''
    if 'include madara.conf' not in existing.splitlines():
        write(kitty, (existing.rstrip() + '\n\n# Madara rice\ninclude madara.conf\n').encode())
    niri = config / 'niri/config.kdl'
    if not niri.exists():
        write(niri, (source / 'niri/config.kdl').read_bytes())
    else:
        print('Existing Niri config preserved. Merge niri/style.kdl as explained in README.md.')
    print(f'In DMS select custom theme: {config / "DankMaterialShell/themes/madara.json"}')
    print(f'In DMS select wallpaper: {data / "madara-rice/madara.png"}')
    print('See README.md for activation, validation and rollback.')


if __name__ == '__main__':
    main()
