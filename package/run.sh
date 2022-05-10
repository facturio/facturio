#!/bin/bash

export APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/local/bin/:$APPDIR/usr/bin/:$PATH"
export LD_LIBRARY_PATH="$APPDIR/usr/lib:$APPDIR/usr/lib/x86_64-linux-gnu:$PATH"
export XDG_DATA_DIRS="$APPDIR/usr/share/:/usr/share/:$XDG_DATA_DIRS"
export PYTHONPATH="$PYTHONPATH:$APPDIR/usr/local/lib/python3.10/dist-packages:$APPDIR/usr/lib/python3/dist-packages"
export GI_TYPELIB_PATH="$APPDIR/usr/lib/x86_64-linux-gnu/girepository-1.0"

facturio "$@"
