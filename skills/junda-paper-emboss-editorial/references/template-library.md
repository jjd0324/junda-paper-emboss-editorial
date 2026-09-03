# Paper Emboss Editorial Template Library

Use this library when a user asks for a repeatable layout rather than a one-off
art direction. Select one template whose use case matches the request; do not
blend template structures unless the user explicitly asks for a hybrid. State
the selected template key in the delivery notes.

## Shared production rules

- Generate an **unlettered artboard**. It must contain no readable or
  pseudo-readable copy, logo, watermark, signature, or text-shaped ornament.
  The named `title zone` is an intentionally empty area, not an instruction to
  render a title. Exact titles, subtitles, and index labels belong in a real
  editable text layer after image generation.
- Each template has exactly one visual metaphor. A rule, dot, or small color
  marker may support it, but must not introduce a second symbolic object.
- Keep the substrate visibly uncoated and fibrous. Relief is shallow and
  paper-bound: soft, single-direction side light, restrained edge highlights,
  and almost no cast shadow. Never turn a cut, path, or window into a thick
  3D object, a plastic render, or a floating sculpture.
- Use the paper base plus one or two colors with distinct jobs. Keep the
  specified title zone quiet enough for the later text layer.
- When a reference image is supplied, apply
  [the reference-image workflow](reference-image-workflow.md) before using a
  template. A reference may influence only the features allowed by its
  contract; it never overrides the template's no-text and single-metaphor
  constraints.

## `wave-recessed-field` — 3:4

### Use when

Creating a calm article cover, book concept, reflective social post, or
culture-and-ideas poster about time, attention, memory, recovery, or a gradual
change. It works best when the user needs a spacious, contemplative result.

### Design fingerprint

One set of broad, nested recessed waves travels across a mostly empty paper
field. The waves are the sole metaphor: an after-effect moving through a quiet
surface. Their origin sits near one edge or corner; the opposite upper third
stays open as the title zone. Use tone-on-tone debossing, or one darker ink
inside the deepest channel, with a single 35–55-degree side light.

### User-replaceable parameters

| Parameter | Default | Valid variation |
| --- | --- | --- |
| `paper_base` | warm ivory, uncoated | cool white, light stone, muted dyed stock |
| `wave_origin` | lower-left corner | any one edge or corner |
| `wave_density` | 4–6 broad arcs | 3–8 arcs; never a busy pattern |
| `ink_role` | deep blue in recesses | one restrained dark or earth tone |
| `title_zone` | upper-right third | any continuous quiet third of the frame |
| `mood` | reflective | calm, patient, intimate, measured |

### Compact image-prompt skeleton

> Unlettered 3:4 editorial paper artboard for `[theme]`: `[paper_base]` uncoated fibrous paper, one field of `[wave_density]` broad nested **recessed** waves beginning at `[wave_origin]`, the waves as the only metaphor for `[mood]`; `[ink_role]` used only to clarify the deepest recesses; quiet blank `[title_zone]` reserved for a later editable text layer; shallow millimetre-scale paper relief, 35–55-degree soft side light, restrained shadows, premium independent-magazine restraint, no letters, no glyphs, no logos, no watermarks, no extra symbols, no thick 3D.

### Acceptance points

- At thumbnail size, the waves read as one calm field rather than a decorative
  pattern or topographic map.
- The edge light proves a shallow depression; no band looks like a raised tube
  or a deep canyon.
- The title zone is visibly empty and sufficiently even for a text overlay.
- There is one wave system only—no sun, door, icon, object, or second motif.

## `threshold-cut-poster` — 3:4

### Use when

Creating a decision, transition, launch, exhibition, or book-cover concept in
which the central idea is crossing into a new state. It is suited to sharper,
more decisive editorial energy than `wave-recessed-field`.

### Design fingerprint

A single diagonal paper seam creates a threshold between two unequal paper
fields. It is a narrow die-cut or shallow recessed split, not a literal room
or a solid 3D doorway. A restrained backing color is visible only inside the
seam. Keep a clear field on the wider side as the title zone; the threshold
itself is the only metaphor.

### User-replaceable parameters

| Parameter | Default | Valid variation |
| --- | --- | --- |
| `paper_base` | soft warm white | pale grey, bone, muted colored stock |
| `seam_angle` | upper-middle to lower-right | 15–35-degree diagonal, never horizontal |
| `seam_width` | slim continuous split | one narrow or medium paper seam |
| `backing_color` | oxidized red | one deliberate contrast color |
| `title_zone` | wider right field | wider left field or top margin |
| `mood` | resolute | poised, tense, hopeful, transitional |

### Compact image-prompt skeleton

> Unlettered 3:4 editorial paper artboard for `[theme]`: `[paper_base]` uncoated paper divided by one slim `[seam_width]` diagonal paper threshold running `[seam_angle]`, with `[backing_color]` visible only inside its shallow cut or recess; the threshold alone represents `[mood]`; an empty quiet `[title_zone]` for a later editable text layer; crisp paper-cut edge pressure, shallow depth, single soft side light, asymmetrical book-cover composition, no letters, no glyphs, no logos, no watermarks, no figures, no second icon, no heavy 3D doorway.

### Acceptance points

- The seam is visibly part of one sheet, with thin paper edges and shallow
  depth—not a tunnel, architectural room, or extruded frame.
- The two fields are intentionally unequal, and the title zone remains quiet.
- The backing color has one job: reveal the crossing point; it does not spread
  into unrelated decoration.
- The threshold is the only object and only metaphor.

## `signal-path-hero` — 16:9

### Use when

Creating a website hero, product narrative header, event landing visual, or
wide editorial banner about direction, progress, transmission, or a single
clear process. Use it when the text overlay needs a stable horizontal reading
area.

### Design fingerprint

One continuous shallow recessed paper path crosses a wide field from one side
toward one endpoint, with at most two deliberate turns. It acts as the single
metaphor for a signal finding direction. The path occupies a lower or far-side
band, leaving the opposing half quiet for live website copy. One small flat
color marker may indicate its endpoint without becoming another object.

### User-replaceable parameters

| Parameter | Default | Valid variation |
| --- | --- | --- |
| `paper_base` | cool white | warm white, pale blue-grey, muted brand stock |
| `path_action` | lightly recessed | tone-on-tone raised only when still paper-bound |
| `path_entry` | lower edge just right of the copy zone | either lower edge or side edge outside the copy zone |
| `endpoint` | right third | any one distant edge or third |
| `path_turns` | two measured turns | 0–2 intentional turns |
| `accent_marker` | one muted orange dot | one dot, short bar, or none |
| `copy_zone` | left 44% of the artboard, x: 8–48%, y: 12–88% | the opposing 44% with the same edge margins |
| `mood` | clear and forward | precise, patient, quietly optimistic |

### Compact image-prompt skeleton

> Unlettered 16:9 editorial website-hero artboard for `[theme]`: `[paper_base]` uncoated finely fibrous paper, one continuous `[path_action]` paper path entering at `[path_entry]` and resolving at `[endpoint]`, with `[path_turns]`; the path alone represents `[mood]`; optional single `[accent_marker]` only at its endpoint; keep `[copy_zone]` completely free of paths, markers, texture clusters and decorative rules for a later live text layer, and keep the path outside that zone; shallow emboss/deboss, restrained 35–55-degree side light, calm premium editorial spacing, no letters, no glyphs, no logos, no watermarks, no maps, no arrows, no extra objects, no thick 3D.

### Acceptance points

- The path can be followed in one glance and has no branches, network nodes,
  more than two turns, or map-like complexity.
- The copy zone occupies about 44% of the width, respects the named edge
  margins, and is free of paths, markers, texture clusters and decorative rules.
- Any accent appears once and only at the endpoint.
- Relief remains a paper detail rather than a raised cable or sculptural track.

## `index-window-cover` — 1:1

### Use when

Creating a square podcast cover, social series cover, content category tile,
or compact editorial identity image about focus, framing, selection, or a
single point of view. It is designed to survive small avatar-like placements.

### Design fingerprint

One inset square or rounded-rectangle paper window sits slightly off-centre in
a nearly monochrome field. It is the single metaphor for selective attention:
a bounded opening into one controlled color plane or closely related paper
surface. A sparse, unlettered pressure-dot grid may live inside the window as
its functional index texture; it must not become a second illustration. A
single hairline rule may support the editorial frame, but no index characters
appear in the generated artboard. Reserve a clear outer band or corner for an
editable title layer.

### User-replaceable parameters

| Parameter | Default | Valid variation |
| --- | --- | --- |
| `paper_base` | natural white | cream, pale grey, muted brand stock |
| `window_shape` | softened square | square or rounded rectangle only |
| `window_position` | slightly upper-left | any off-centre quadrant |
| `inner_plane` | deep ink blue | one quiet contrast or tone-on-tone plane |
| `index_marks` | 4×4 shallow pressure-dot grid | none or one sparse unlettered dot grid |
| `frame_detail` | one hairline edge rule | none, one rule, or two rules |
| `title_zone` | lower outer band | one outer side band or corner |
| `mood` | focused | collected, deliberate, curious, private |

### Compact image-prompt skeleton

> Unlettered 1:1 editorial cover artboard for `[theme]`: `[paper_base]` uncoated fibrous paper, one shallow inset `[window_shape]` at `[window_position]` revealing a flat `[inner_plane]` plane; this one window alone represents `[mood]`; optional `[index_marks]` stay inside the window as a subdued functional texture, and `[frame_detail]` may support the outer editorial frame without characters; reserve empty `[title_zone]` for a later editable text layer; tone-on-tone paper pressure, soft single-direction side light, restrained square-cover composition, no letters, no numbers, no glyphs, no logos, no watermarks, no second motif, no heavy 3D frame.

### Acceptance points

- The window is recognisable immediately at small size and remains one clean
  form, not a grid, collage, or literal scene.
- The inner plane is flat or nearly flat; it does not become a photographic
  landscape, a product, or a second narrative.
- Index marks and crop rules, when used, are purely non-verbal and subordinate
  to the window.
- The title zone has no generated microtype or decorative marks that would
  conflict with the editable overlay.

## Template delivery record

For every output based on this library, record: template key, ratio, one
metaphor, paper action, color roles, reserved text zone, and reference mode.
For strict-text work, also state that the generated file is an unlettered art
base and identify the separate editable overlay required for final copy.
