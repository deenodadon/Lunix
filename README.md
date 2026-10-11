# Madara · Crimson Susanoo

A Naruto / Madara inspired rice for **Nobara + Niri + DankMaterialShell (DMS)**.
Obsidian surfaces, crimson focus rings, icy blue secondary controls, rounded
windows, soft shadows, and a matching Kitty terminal. Includes an original
generated Madara wallpaper with dark space on the left for windows.

| Role | Color |
| --- | --- |
| Background | `#090a0f` |
| Panel | `#16151e` |
| Sharingan crimson | `#ef4454` |
| Susanoo blue | `#65b8ff` |
| Text | `#eeeaf0` |

## Install on your Nobara computer

This bundle assumes Niri and DMS are already installed. If needed, follow the
[official Dank Linux installation documentation](https://danklinux.com/docs).
Keep your existing Nobara desktop available while setting up your Niri session.
The installer uses Python 3 and does not install system packages or change your
display manager. Kitty is optional; install it through Nobara's package manager
if you want the matching terminal.

Download/extract the bundle, open a terminal in this directory, then run:

```sh
python3 install.py --dry-run
python3 install.py
```

Run as your normal user, without sudo. It honors `XDG_CONFIG_HOME` and
`XDG_DATA_HOME`. Changed files are backed up under
`~/.local/share/madara-rice/backups/` (or your XDG data directory). Existing Niri
configuration and DMS settings are preserved; symlink destinations are refused
so managed dotfiles can be integrated manually. Identical assets are left alone.

## Activate the look

1. In DMS Settings, open the theme/colors section, choose **Custom**, and select
   `~/.config/DankMaterialShell/themes/madara.json`. Select **dark mode**. Use
   the custom theme rather than wallpaper-generated colors to keep this palette.
2. In DMS's wallpaper picker select
   `~/.local/share/madara-rice/madara.png`. Use a fill/crop fit. DMS handles the
   wallpaper, panel, launcher, notifications, and lock screen; no Waybar,
   swaybg, or separate notification daemon is needed for this rice.
3. Recommended DMS styling: one floating top bar, about 36 px tall, 12 px edge
   padding, rounded corners, dark panel background at roughly 95% opacity.
   Place workspaces and launcher left, clock center, audio/network/battery right.
   Disable the dock for a clean look, or keep a small auto-hiding dock.
   These are preferences to set in the UI, not settings overwritten by the installer.
4. If you already have `~/.config/niri/config.kdl`, merge the properties inside
   this bundle's `niri/style.kdl` **into your existing `layout` block**. Replace
   the old focus-ring, border, and shadow values. Add the supplied `window-rule`
   once, or merge its two properties into your general window rule. Preserve
   existing monitor, input, keybindings and DMS generated includes. If a generated
   DMS Niri colors include overrides these colors, disable that generated color
   integration in DMS or remove only its colors include after making a backup.
   Do not append a duplicate layout block. For a fresh setup, the installer
   creates a minimal config which includes the style file.
5. Ensure DMS starts exactly once: keep your existing DMS session/service setup,
   or add `spawn-at-startup "dms" "run"` to Niri if it isn't started elsewhere.
   The fresh example includes it. Open a new Kitty window to see the terminal
   theme. Disable DMS automatic Kitty theme generation if it replaces this palette.

Use the corresponding XDG paths if yours differ. The fresh example uses
Super+Enter for Kitty, Super+D for the DMS launcher, Super+Q to close,
Super+arrow keys to focus, Super+Page Up/Down for workspaces,
Super+F to maximize, Super+Shift+F for fullscreen, and Super+Tab for overview.

## Validate and undo

Before switching sessions, validate on your Nobara machine:

```sh
niri validate --config "$HOME/.config/niri/config.kdl"
```

If your config directory differs, pass its actual path. Niri reloads configuration
automatically after saving. Check window focus, launcher, wallpaper, terminal,
sound controls, and lock-screen readability in your Niri session.

To undo, restore changed files from the timestamped backup directory to the
original paths (the backup mirrors each absolute path). Remove newly created
theme/style/wallpaper files if desired. If Kitty had no config before installation,
remove the created `kitty.conf`; otherwise restore its backup. Re-select your old
DMS theme and wallpaper. If the installer created a fresh Niri config, remove it
only when you have an alternative config or session ready.

The JSON keys and Niri options were checked against upstream DMS and Niri source.
Installer behavior and KDL syntax were checked in the cloud workspace. This
workspace has no Nobara graphical session, so live compositor, DMS rendering,
GPU behavior and your installed version's compatibility must be checked locally.
