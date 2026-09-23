#!/usr/bin/env bash
set -euo pipefail

# Render the Notes Vault narration and prove it before keeping it.
#
# One take, cut on the pauses — twelve separate calls are twelve readings and it
# sounds like a set of clips rather than a person. Same voice as the AYA film.
#
# Two things can go wrong and only one of them is visible:
#   - the cut does not land on twelve pieces. The renderer says so and writes nothing.
#   - the model quietly skips a line. The cut still finds twelve pieces, every clip
#     is a good mp3, and one of them is missing half its words. That happened on
#     2026-09-22: clip one lost "A phrase opens it." and only verify.py found it.
#
# So: render, read every clip back with Whisper, and re-roll until they match.

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"
renderer="/Volumes/Mac Work/VS Studio Master/workdesk/scripts/render-narration.mjs"
python3_aya="/Applications/AYA.app/Contents/Resources/runtime/bin/python3"
style="Read this conversationally, at a natural everyday pace, warm and direct, like telling a friend about something you are pleased with"

set -a; . "/Volumes/Mac Work/VS Studio Master/AIS-OS/.env"; set +a

# Render into a scratch directory and only move clips into place once they have
# been read back and match. The first version of this loop deleted the existing
# clips at the top of each attempt, then hit the daily quota on attempt two — and
# took eleven good clips with it. Never destroy a take you have not replaced.
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT

# The quota is PER MODEL per day, even on a paid key, so flash running out does not
# mean the key is finished. pro is the same voice, and the two do not sound
# identical — which matters only if clips from both end up side by side. A one-take
# render is all-or-nothing, so they cannot.
for attempt in 1 2 3 4 5 6; do
  model=$([ "$attempt" -le 3 ] && echo gemini-2.5-flash-preview-tts || echo gemini-2.5-pro-preview-tts)
  echo "── take $attempt · $model ──"
  rm -f "$scratch"/nv-*.mp3
  if ! GOOGLE_TTS_KEY="$CDS_GEMINI_API_KEY" node "$renderer" \
      --source notes-vault-narration.ts --out "$scratch" --voice Achernar --one-take \
      --model "$model" --style "$style"
  then
    echo "  the cut did not land. Again."
    continue
  fi
  if "$python3_aya" verify.py "$scratch"; then
    mv "$scratch"/nv-*.mp3 .
    echo
    echo "Twelve clips, one performance, every word checked."
    python3 build-mix.py
    exit 0
  fi
  echo "  a clip lost words. Again."
done

echo "Six takes and none of them clean. Listen to the raw take before changing anything."
exit 1
