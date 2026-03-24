#!/usr/bin/env python3
"""Convert video to optimized GIFs using palette generation."""
import argparse, shutil, subprocess, tempfile
from pathlib import Path

def require(x):
    if shutil.which(x) is None: raise SystemExit(f'Missing required binary: {x}')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input'); p.add_argument('output'); p.add_argument('--fps',type=int,default=12); p.add_argument('--width',type=int,default=480); p.add_argument('--dry-run',action='store_true')
    a=p.parse_args(); require('ffmpeg')
    palette=str(Path(tempfile.gettempdir())/'palette.png')
    c1=['ffmpeg','-y','-i',a.input,'-vf',f'fps={a.fps},scale={a.width}:-1:flags=lanczos,palettegen',palette]
    c2=['ffmpeg','-y','-i',a.input,'-i',palette,'-lavfi',f'fps={a.fps},scale={a.width}:-1:flags=lanczos[x];[x][1:v]paletteuse',a.output]
    print(' '.join(c1)); print(' '.join(c2))
    if not a.dry_run: subprocess.check_call(c1); subprocess.check_call(c2)
if __name__ == '__main__': main()
