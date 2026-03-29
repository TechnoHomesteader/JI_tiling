# Jake's Exploration Plan

This branch is for experimental development around external control, live voice processing, and outbound musical control. The goal is to keep `main` stable while the new interaction and synthesis ideas are prototyped in `codex/jakes-exploration`.

## Current baseline

- `tiling.scd` already supports tile selection from the SuperCollider window and a single inbound OSC message: `'/Tile'`.
- Outbound OSC is not implemented yet.
- MIDI setup exists only as commented scaffolding and is not part of the playback path.
- Live input exists in vocoder mode, but there is no pitch tracking, repitching, or pitch-derived harmonization layer.
- `~playTile` is the central execution point: it computes four JI frequencies from the selected tile and sends them straight to the current synth path.
- The UI currently exposes only the lattice-parameter button, so most new behavior should be designed as state-driven control rather than embedded directly in window callbacks.

## Exploration goals

1. Add richer external control over tile selection, pitch behavior, and timbral shaping.
2. Support both inbound control and outbound musical data for TouchDesigner, Ableton, and other clients.
3. Add pitch-motion behaviors such as glide, cross-pitch transitions, and alternate target-pitch strategies.
4. Introduce voice-driven harmonization and repitching from live audio input.
5. Add controllable overtone enhancement, wavefolding, or harmonic distortion.
6. Keep the system modular enough that tile logic, playback, and external messaging can evolve independently.

## Proposed architecture direction

The current file works, but almost all behavior converges into `~playTile`. The first structural step should be to split that path into smaller stages:

1. Tile analysis
   - read tile geometry
   - derive ratios, frequencies, amplitudes, and metadata
2. Collection resolution
   - apply span/width rules
   - choose pitch targets
   - decide shift mode and glide policy
3. Playback
   - update persistent synths or spawn transient ones
   - apply overtone or distortion controls
   - manage voice input harmonization
4. External emission
   - send OSC state updates
   - send MIDI note data
   - mirror relevant values to control surfaces

This keeps "what the tile means" separate from "how the sound moves" and "what gets transmitted externally."

## Control state to introduce

A shared state object should hold anything that can be changed by UI, OSC, or MIDI. In SuperCollider this can start as an `Event` or dictionary-style environment, for example:

```supercollider
~controlState = (
    shiftMode: \nearest,
    glideTime: 0.0,
    collectionSpan: 4,
    overtoneBlend: 0.0,
    foldAmount: 0.0,
    outboundOscEnabled: true,
    outboundMidiEnabled: false,
    voiceTrackingEnabled: false,
    voiceHarmonizeEnabled: false,
    pitchSource: \tile,
    randomizeSeed: nil
);
```

This gives all new features one stable home instead of scattering globals across callbacks.

## Pitch-behavior workstream

These are the pitch controls implied by the exploration notes:

- Shift target mode
  - nearest pitch
  - furthest pitch
  - randomized pitch
  - explicit cross-pitch mode for exaggerated transitions
- Glide / portamento time
  - global control first
  - per-voice variation later if musically useful
- Pitch collection span / width
  - control how far the collection reaches from the selected tile or derived center
- Collection mapping rules
  - decide whether the collection is ordered by ratio, spatial relation, proximity to current pitch, or some hybrid rule

One open design question needs to be settled early: in "cross-pitch" mode, does each voice target the opposite extreme of the new collection, or do all voices follow a shared remapping rule? That choice will affect both the sound and the MIDI export behavior.

## Voice-derived harmonization workstream

There is already a live-input path through the vocoder, so the next experimental layer can build on that:

1. Add pitch tracking from live input.
2. Derive either a single detected fundamental or a smoothed pitch estimate.
3. Use that detected pitch to:
   - retune the tile collection around the voice
   - harmonize the voice with selected JI ratios
   - drive partial layers or overtone reinforcement
4. Add smoothing and confidence gating so unstable pitch detection does not cause chatter.

For a first pass, `Pitch.kr` is a practical starting point. If tracking quality is not good enough, it can later be swapped for a more specialized detector without changing the rest of the architecture.

## Timbral-processing workstream

The current code already hints at richer carrier design through triangle waves, folded carriers, and overtone layering. The exploration branch should make those musically controllable:

- overtone blend
- wavefold or harmonic distortion amount
- optional separate controls for dry tone vs processed tone
- compatibility with both normal playback and vocoder/harmonizer paths

The important constraint is to avoid burying these controls inside one SynthDef. A small set of named parameters that all playback paths can honor will be easier to expose over OSC and MIDI.

## External control and output workstream

### Inbound control

Expand beyond `'/Tile'` to a namespaced OSC scheme that can be extended without collisions, for example:

- `'/tile/select'`
- `'/control/shiftMode'`
- `'/control/glideTime'`
- `'/control/collectionSpan'`
- `'/control/overtoneBlend'`
- `'/control/foldAmount'`
- `'/voice/harmonize'`
- `'/transport/panic'`

TouchOSC can then map buttons, faders, and toggles to these controls directly.

### Outbound OSC

Add OSC emission for visual and downstream-control clients such as TouchDesigner:

- selected tile index
- tile center position
- tile vertices
- active ratios
- resolved frequencies
- shift mode / glide state

Suggested outbound messages:

- `'/tile/selected'`
- `'/tile/position'`
- `'/tile/vertices'`
- `'/collection/ratios'`
- `'/collection/frequencies'`
- `'/state/control'`

### Ableton integration

Use MIDI first for note-driven instruments, while keeping OSC available for richer metadata:

- send pitch collections as note sets
- track note-on / note-off cleanly when the tile changes
- define whether Ableton receives:
  - all voices
  - only the root plus metadata
  - separate channels per voice
- decide whether glide is represented as note retrigger, pitch bend, or only internal SuperCollider motion

The likely split is:

- MIDI for playable note data into Ableton instruments
- OSC for tile geometry, ratios, and non-MIDI parameters

## Recommended implementation phases

### Phase 1: Refactor the playback path

- extract helpers from `~playTile`
- create a function that returns tile metadata without playing sound
- create a function that resolves the final pitch collection
- create a function that handles playback only

### Phase 2: Introduce shared control state

- add `~controlState`
- route current button and OSC input through that state
- keep old behavior as defaults so nothing breaks

### Phase 3: Add outbound messaging

- emit tile position and pitch data over OSC
- build a small MIDI output wrapper with active-note bookkeeping
- make external output optional behind flags

### Phase 4: Add pitch motion behavior

- implement shift modes
- add glide time
- prototype cross-pitch remapping
- test behavior when rapidly changing tiles

### Phase 5: Add voice tracking and harmonization

- detect live pitch
- smooth and gate the detector
- map voice pitch into tile-based harmonization
- test interaction with vocoder mode

### Phase 6: Add timbral controls

- expose overtone blend and fold amount
- unify parameter names across SynthDefs
- connect those parameters to OSC and UI controls

## Immediate next tasks in this branch

1. Refactor `~playTile` into data-first helper functions without changing current sound.
2. Add a shared control state with defaults for shift mode, glide time, collection span, and timbral controls.
3. Implement outbound OSC for tile position and pitch collection data.
4. Re-enable MIDI output behind a flag and add note bookkeeping.
5. Define the first TouchOSC page around:
   - tile selection
   - shift mode
   - glide time
   - collection span
   - overtone / fold controls
6. Prototype one voice-derived harmonization path before scaling to all voices.

## Design questions to resolve during implementation

- What is the exact rule for "cross-pitch" mapping?
- Should randomized pitch selection be repeatable from a seed or free-running?
- Should collection span be measured in lattice distance, ratio order, or voice count?
- Should Ableton receive raw frequency-derived MIDI notes, quantized notes, or both?
- Should outbound OSC transmit only selected-tile data, or continuous pointer position as well?

## Definition of success for the branch

This branch will be in a strong exploratory state when it can do all of the following:

- select tiles from local UI, OSC, or MIDI
- reshape pitch behavior with shift-mode and glide controls
- send tile and collection data outward to visual and DAW clients
- drive Ableton instruments with stable note output
- derive harmonization behavior from a live incoming voice
- expose overtone or folding controls as real-time performance parameters
