#!/usr/bin/env python3
"""Lay the twelve clips against the demo and mux the result.

Each clip starts when its caption appears — the `start` values in
notes-vault-narration.ts, which were found by watching the caption band change
rather than by eye.

The video stream is copied, never re-encoded. It is a 1.9 MB h264 file that is
already on the site and already looks right; re-encoding it to add a sound track
would cost quality for nothing.
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOWNLOADS = HERE.parent
SRC = DOWNLOADS / 'notes-vault-demo.mp4'
OUT = DOWNLOADS / 'notes-vault-demo.mp4'
TMP = HERE / 'muxed.mp4'

spec = (HERE / 'notes-vault-narration.ts').read_text()
clips = [
    {'k': k, 'start': float(start)}
    for k, start in re.findall(r"k: '([\w-]+)',\s*\n\s*start: ([\d.]+),", spec)
]
assert len(clips) == 12, f'found {len(clips)} clips in the script, expected 12'

dur = lambda p: float(subprocess.run(
    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
    capture_output=True, text=True, check=True).stdout)

video_len = dur(SRC)
print(f'{SRC.name}  {video_len:.2f}s')

# Report anything that runs into the next caption. Not fatal — a voice finishing
# half a second after a caption changes is how real narration behaves — but it
# should be a decision rather than a surprise.
for i, c in enumerate(clips):
    c['dur'] = dur(HERE / f"{c['k']}.mp3")
    limit = clips[i + 1]['start'] if i + 1 < len(clips) else video_len
    over = c['start'] + c['dur'] - limit
    flag = f'  ← runs {over:.2f}s past the next caption' if over > 0.05 else ''
    print(f"  {c['k']}  {c['start']:6.2f}s + {c['dur']:4.2f}s{flag}")

inputs = []
for c in clips:
    inputs += ['-i', str(HERE / f"{c['k']}.mp3")]

delays = ''.join(
    f"[{i + 1}:a]adelay={int(c['start'] * 1000)}|{int(c['start'] * 1000)}[d{i}];"
    for i, c in enumerate(clips)
)
mix = ''.join(f'[d{i}]' for i in range(len(clips)))
# normalize=0: amix otherwise divides every voice by the number of inputs and the
# whole track comes back at a twelfth of its level.
# apad, then -shortest. The last clip ends at 62.6s against a 65.5s video, so
# without the pad the audio is the shorter stream and -shortest trims the VIDEO
# down to it — the demo lost its closing 2.9 seconds that way once. Padded, the
# audio is the longer stream and -shortest does what it is there for.
graph = f'{delays}{mix}amix=inputs={len(clips)}:normalize=0,apad[a]'

subprocess.run(
    ['ffmpeg', '-loglevel', 'error', '-y', '-i', str(SRC), *inputs,
     '-filter_complex', graph, '-map', '0:v', '-map', '[a]',
     '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', str(TMP)],
    check=True)

print(f'\n{TMP.name}  {dur(TMP):.2f}s  {TMP.stat().st_size / 1_048_576:.1f} MB')
print(f'Listen, then:  mv {TMP} {OUT}')
