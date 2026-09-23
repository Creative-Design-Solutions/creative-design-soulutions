#!/usr/bin/env python3
"""Check that every clip says the line it is named for.

    /Applications/AYA.app/Contents/Resources/runtime/bin/python3 verify.py

Uses AYA's own Whisper, offline. Exists because on 2026-09-22 a one-take render
came back with twelve clips, the right count, the right lengths and a clean cut —
and the first one was missing its first sentence. The model had simply not said
"A phrase opens it." Nothing in the render output could show that: the cut checks
how many pieces it made, never what is in them.

A perfectly good mp3 of the wrong words is the failure mode here, and only reading
them back catches it. Exit 1 if anything drifted, so the render loop can re-roll.
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The clips being checked may be in a scratch directory that has not been accepted
# yet — render.sh verifies before it moves anything into place.
CLIPS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
sys.path.insert(0, '/Applications/AYA.app/Contents/Resources')

import os
os.environ['HF_HOME'] = os.path.expanduser('~/Library/Application Support/AYA/models')
os.environ['HF_HUB_OFFLINE'] = '1'
import numpy as np
import mlx_whisper

spec = (HERE / 'notes-vault-narration.ts').read_text()
want = re.findall(r"k: '([\w-]+)',[\s\S]*?say: '((?:[^'\\]|\\.)*)'", spec)

# Compare on words alone. Whisper punctuates and capitalises to its own taste, and
# a hyphen or a full stop is not a wrong reading.
norm = lambda s: ' '.join(re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split())

bad = 0
for k, say in want:
    clip = CLIPS / f'{k}.mp3'
    if not clip.exists():
        print(f'MISSING {k}.mp3')
        bad += 1
        continue
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(clip),
                    '-ac', '1', '-ar', '16000', '-f', 'f32le', '/tmp/_verify.raw'], check=True)
    audio = np.fromfile('/tmp/_verify.raw', dtype=np.float32)
    got = mlx_whisper.transcribe(
        audio, path_or_hf_repo='mlx-community/whisper-large-v3-turbo')['text'].strip()
    expect = say.replace("\\'", "'")
    if norm(got) == norm(expect):
        print(f'  ok   {k}')
    else:
        bad += 1
        print(f'  DIFF {k}\n         said  {got!r}\n         wanted {expect!r}')

print(f'\n{len(want) - bad}/{len(want)} clips say what they should.')
sys.exit(1 if bad else 0)
