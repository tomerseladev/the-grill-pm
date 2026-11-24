# Design reference

The visual system, so contributors build consistently.

## Surfaces (60 / 30 / 10)

| Token | Value | Use |
|---|---|---|
| `surface-0` | `#0F1117` | 60% of the screen: page background |
| `surface-1` | `#1C202B` | 30%: cards and panels, always with a 1px border `rgba(255,255,255,0.07)` |
| `surface-2` | `#262B38` | Hover and active states |

## Accents (one meaning each)

| Token | Value | Meaning |
|---|---|---|
| `mint` | `#2DD4BF` | The user acts |
| `violet` | `#A78BFA` | The AI speaks or judges |

## Heat

`ember` `#FB923C` is used only for the last 2 minutes, pushback, and "missing" feedback.

## Text

- Primary: `#F5F7FA`
- Secondary: `#9AA3B2`
- On any filled accent: `#0F1117`

## Fonts

- Space Grotesk: headings
- Inter: body
- JetBrains Mono: timer and scores

## The interviewer's face: VoiceBars

7 violet pill bars.

- States: `idle`, `thinking`, `speaking`, `pushback` (ember), `listening`.
- Gestures: `nod`, `tilt`, `lean`, `brow`, `shake`, `approve`. At most one per reply.

## Motion

All motion honours `prefers-reduced-motion`.
