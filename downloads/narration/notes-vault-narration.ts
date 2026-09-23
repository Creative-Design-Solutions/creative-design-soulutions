/**
 * The voiceover for downloads/notes-vault-demo.mp4.
 *
 * EVERY LINE IS ALREADY ON SCREEN. These are the demo's own captions, word for
 * word, so the voiceover says nothing the video does not already say. They were
 * read back off the rendered frames — the clip was built in a session scratchpad
 * on 2026-08-17 and that source is long gone, so the video itself is the source of
 * truth for its own words now.
 *
 * `start` is where each caption appears, found by watching the caption band for
 * changes rather than by eye. It is what places each clip in the mix; the renderer
 * itself ignores it.
 *
 * ONE TAKE. Rendered with --one-take and cut on the pauses, because twelve separate
 * calls are twelve readings and it sounds like a set of clips rather than a person.
 * Same voice as the AYA film — Achernar.
 *
 * Two rules this shape has to follow, both learned the hard way:
 *   - single quotes on every `say`; a double-quoted line silently renders the NEXT
 *     entry's words under this one's filename
 *   - `k:` is the first line inside every `{`; any comment between them and the
 *     entry vanishes with no error and no clip
 *
 * "Command K", not "⌘K": a symbol has to be a word in a spoken line. Acronyms stay
 * written plainly — "CSV", never "C S V" — which is what keeps them sounding human.
 *
 * Re-render:  ./render.sh
 */
export const NARRATION = [
  {
    k: 'nv-01',
    start: 0.0,
    say: 'A phrase opens it. Or Touch ID.',
  },
  {
    k: 'nv-02',
    start: 4.0,
    say: 'Every password and private note, in one encrypted file.',
  },
  {
    k: 'nv-03',
    start: 8.0,
    say: 'Two-factor codes and expiry dates alongside them.',
  },
  {
    k: 'nv-04',
    start: 12.0,
    say: 'Search filters the list as you type.',
  },
  {
    k: 'nv-05',
    start: 17.75,
    say: 'Narrow, as a panel beside your work.',
  },
  {
    k: 'nv-06',
    start: 21.75,
    say: 'Wide, when you\'re digging through it.',
  },
  {
    k: 'nv-07',
    start: 25.75,
    say: 'Or folded down to its title bar, out of the way.',
  },
  {
    k: 'nv-08',
    start: 29.75,
    say: 'Command K jumps straight to anything.',
  },
  {
    k: 'nv-09',
    start: 38.75,
    say: 'Bring your old passwords over from any CSV. Groups come across.',
  },
  {
    k: 'nv-10',
    start: 45.75,
    say: 'Light or dark, whichever you keep.',
  },
  {
    k: 'nv-11',
    start: 55.75,
    say: 'And in the menu bar, wherever you are.',
  },
  {
    k: 'nv-12',
    start: 60.0,
    say: 'Click the lock, and walk away.',
  },
] as const;
