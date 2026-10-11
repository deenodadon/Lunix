#!/usr/bin/env python3
"""Install Madara blood-red folders and activate them for GNOME/GTK apps."""
import datetime
import os
from pathlib import Path
import shutil
import subprocess

THEME = 'Madara-Blood'
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
<path fill="#580916" d="M5 17a5 5 0 0 1 5-5h16l6 6h22a5 5 0 0 1 5 5v26a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5z"/>
<path fill="#7e1020" d="M5 23h54v26a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5z"/>
<path fill="#ae142b" d="M8 24h48a4 4 0 0 1 4 4l-3 22a4 4 0 0 1-4 4H11a4 4 0 0 1-4-4L4 28a4 4 0 0 1 4-4z"/>
<path fill="#dc3047" d="M8 24h48a4 4 0 0 1 4 4H4a4 4 0 0 1 4-4z"/>
<path fill="#670c1a" opacity=".45" d="M7 49h50l-.3 2a4 4 0 0 1-3.7 3H11a4 4 0 0 1-3.7-3z"/>
</svg>'''


def main():
    if not shutil.which('gsettings'):
        raise SystemExit('gsettings is required; run this in your Nobara desktop session.')
    current = subprocess.check_output(
        ['gsettings', 'get', 'org.gnome.desktop.interface', 'icon-theme'], text=True
    ).strip().strip("'")
    data = Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local/share')
    target = data / 'icons' / THEME
    if target.is_symlink() or any(p.is_symlink() for p in target.parents):
        raise SystemExit('Icon location is a symlink. Integrate manually instead.')
    inherits = current if current and current != THEME else 'Adwaita'
    if target.exists():
        # Preserve the original inherited theme on repeat installation.
        index = target / 'index.theme'
        if current == THEME and index.is_file():
            for line in index.read_text().splitlines():
                if line.startswith('Inherits='):
                    inherits = line.split('=', 1)[1].split(',')[0]
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        saved = data / 'madara-rice/backups' / stamp / 'Madara-Blood'
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, saved, symlinks=True)
        print(f'Previous custom icons backed up to {saved}')
    places = target / 'scalable/places'
    places.mkdir(parents=True, exist_ok=True)
    names = ['folder', 'folder-open', 'folder-visiting', 'inode-directory',
             'folder-documents', 'folder-download', 'folder-downloads',
             'folder-music', 'folder-pictures', 'folder-videos', 'folder-templates',
             'folder-publicshare', 'folder-desktop', 'folder-saved-search',
             'folder-remote', 'folder-recent', 'user-home', 'user-desktop']
    for name in names:
        file = places / (name + '.svg')
        if file.is_symlink():
            raise SystemExit(f'Refusing to overwrite symlink: {file}')
        file.write_text(SVG)
    index = target / 'index.theme'
    if index.is_symlink():
        raise SystemExit(f'Refusing to overwrite symlink: {index}')
    index.write_text(f'''[Icon Theme]
Name=Madara Blood
Comment=Blood-red folders; other icons inherit your previous theme
Inherits={inherits},hicolor
Directories=scalable/places

[scalable/places]
Size=48
Type=Scalable
MinSize=16
MaxSize=512
Context=Places
''')
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.interface', 'icon-theme', THEME], check=True)
    print('Activated blood-red folders. Restart Nautilus: nautilus -q')
    print(f'To undo: gsettings set org.gnome.desktop.interface icon-theme "{inherits}"')
    print('If DMS overrides the icon theme, choose Madara-Blood in its icon-theme settings.')


if __name__ == '__main__':
    main()
