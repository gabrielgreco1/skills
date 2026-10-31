#!/bin/bash
# reveal.sh PATH... — show files/folders in the desktop file manager, on any OS.
#   macOS            -> open -R (highlights the file in Finder)
#   Windows          -> explorer.exe (git-bash / MSYS / Cygwin)
#   WSL              -> wslview when present
#   Linux            -> xdg-open on the containing folder
# NO_OPEN=1 does nothing (headless boxes, CI, remote shells).
[ -n "$NO_OPEN" ] && exit 0
[ $# -gt 0 ] || { echo "usage: reveal.sh PATH..." >&2; exit 2; }
OS=$(uname -s)
for p in "$@"; do
  [ -e "$p" ] || { echo "reveal: no such path: $p" >&2; continue; }
  if [ -d "$p" ]; then target=$p; else target=$(dirname "$p"); fi
  case "$OS" in
    Darwin) open -R "$p" ;;
    MINGW*|MSYS*|CYGWIN*)
      if command -v cygpath >/dev/null; then w=$(cygpath -w "$p"); else w=$p; fi
      explorer.exe "$w" >/dev/null 2>&1 ;;
    Linux)
      if command -v wslview >/dev/null; then wslview "$target" >/dev/null 2>&1
      elif command -v xdg-open >/dev/null; then xdg-open "$target" >/dev/null 2>&1
      else echo "reveal: install xdg-utils (xdg-open) to open a file manager; path: $p" >&2; fi ;;
    *) echo "reveal: unsupported platform '$OS'; path: $p" >&2 ;;
  esac
done
exit 0
