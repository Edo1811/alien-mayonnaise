# Barium Client — Full Design & Functional Specification

## Overview

Barium is a three-layer Minecraft client for Windows:
1. **The Launcher** — mod management, profiles, version selection, game launch
2. **The In-Game Hacks Menu** — RShift-triggered tree GUI for toggling cheats
3. **The Overlay** — external OS-level window for hack status, panic button, settings

---

## Layer 1: The Launcher

### Technology
- **Framework:** Tauri (Rust core, lighter than Electron, no Chromium bloat)
- **Platform:** Windows only
- **Window style:** Frameless, custom titlebar — Barium logo left, minimize/close right. Premium feel, no native OS chrome.

### Layout
Single scrollable page. No tabs, no sidebars, no navigation.

**Above the fold (hero section):**
- Custom titlebar at top (always visible, part of the frame)
- A single **frosted glass card** centered in the hero area — this is the primary surface of the launcher. It contains, in order: the Barium logo + atomic subtitle, the version selector, and the play button. Nothing in the hero section lives outside this card except the profile sidebar.
- Profile sidebar sits on the left edge, outside the card, vertically aligned with it
- The play button is a **full-width capsule** spanning the inner width of the glass card. It is the single most important element on the page — dominant through width, not size.

**Below the fold (mod section):**
- Text search bar at top — tags are invisible metadata, not UI elements. Searching "performance" surfaces all mods tagged performance. Searching "sodium" finds Sodium directly.
- Flat mod list below the search bar. No sections, no category labels visible.
- Each mod card: name, short description, toggle switch. Toggle uses the spectrum gradient when on, dim white when off.
- Hacks mod card always pinned to the top of the list regardless of search. Has a subtle rainbow/spectrum tinted background and spectrum gradient text to distinguish it. Cannot be reordered.
- Incompatible mod cards are faded (reduced opacity), toggle disabled and dimmed, description replaced with red warning text (`⚠ incompatible: 1.20.1 → 1.21.4`). Card remains visible in the list.

### Profile Sidebar
Sits on the left edge of the launcher, vertically alongside the hero section and mod list.

- **All Active** (preset, locked, cannot be deleted or renamed) — all mods on
- **Vanilla** (preset, locked, cannot be deleted or renamed) — all mods off, hacks off
- User-created profiles below, in creation order
- **"+"** button at the bottom of the sidebar to create a new profile
- **Click** a profile to instantly apply its mod toggle states
- **Right click** a profile to rename, duplicate, or delete it (locked presets show a greyed-out delete option)
- Active profile is visually highlighted

### Version Selector
- Dropdown above the play button
- Selecting a version triggers a Modrinth API call:
  ```
  GET https://api.modrinth.com/v2/project/{id}/version
      ?game_versions=["x.xx.x"]
      &loaders=["fabric"]
  ```
- Curated mod list uses hardcoded Modrinth project IDs (permanent identifiers)
- Compatible versions auto-resolve their download URLs — zero maintenance after initial setup
- **Custom-uploaded mods** are checked against their `fabric.mod.json` minecraft version constraint
  - If incompatible: card is faded, toggle disabled and dimmed, description shows `⚠ incompatible: 1.20.1 → 1.21.4` in red
  - The mod stays visible — user remembers it exists for when they switch versions

### Play Button States

| State | Appearance | Behavior |
|---|---|---|
| **Default** | Full-width capsule, spectrum gradient border, spectrum "PLAY" text | Launches game |
| **Launching** | Disabled, log line appears directly below it inside the card | Log updates live. "Open logs" button appears nearby |
| **Running** | Transforms to "Close" button | Click = graceful shutdown, game saves |
| **Saving** | Becomes "Kill" button (red) | Click = force quit |
| **Closed** | Returns to default | Ready to launch again |

- During Launching and Running states, the last log line appears directly below the button inside the glass card, matching its width — the button and log line together read as a single unified status block
- "Open logs" button next to the log line — opens full scrollable log panel or external log file
- Launcher **minimizes** automatically when the game window opens (game stays on top)
- Future settings page will include an "automatically close launcher on game start" toggle

### Mod Upload
- "Upload mod" card always present at the bottom of the flat mod list
- Drag and drop or file picker — accepts `.jar` files
- Uploaded mods are saved to `/barium/mods/` (separate from `.minecraft/mods/`)
- Appear in the Custom section of the flat list with version compatibility checked immediately

---

## In-Game Main Menu

Barium reskins the vanilla Minecraft main menu without touching its UX. All vanilla buttons, layout, and interactions remain exactly as-is. Only the visual presentation changes.

### Background
- Replaced by a 16:9 prism beam image: a white light beam entering from the upper-left, splitting at roughly the center of the screen into a full spectrum fan (red → orange → yellow → green → blue → violet) that spreads toward the lower-right
- Rendered at ~65% opacity so the spectrum glows without washing out the white button text layered on top of it
- The split point sits slightly right of true center, giving the composition natural breathing room

### Title text
- "Minecraft: Java Edition" is replaced with two lines:
  - **"Minecraft"** — same size and position as vanilla
  - **"Barium Client"** — smaller, directly below, rendered in the spectrum gradient (`#ff6b6b → #ffd93d → #6bcb77 → #4d96ff → #c77dff`)
  - A dark text-shadow sits behind "Barium Client" to ensure readability against the spectrum background — invisible in effect, essential in function

### Splash text
- Identical to vanilla in style: same font, same size, same slight rotation
- Color changed from vanilla yellow to **white**
- Custom string pool replaces all vanilla splashes. Example strings:
  - "Hacking is bad!!1!"
  - "Playing 'Hit rocks with a stick'"
  - "Flavor with no seasoning"
  - "Try cryptoookie.net!"

### What is NOT changed
- Button layout, button styles, button behavior
- Any other vanilla GUI element
- Panorama-style background motion (if present in the target version)

---

## Layer 2: In-Game Hacks Menu

### Trigger
- **RShift** — opens/closes the menu
- Renders inside the game using Fabric/Mixin

### GUI: Interactive Tree
A radial node-branch tree rendered as an overlay on the game world (blurred and darkened background). Only accessible in-game via RShift — not available from the main menu.

**Structure:**
- Central node: "Barium" circle at screen center
- First-level branches: categories (Combat, Movement, Render/ESP, Network, Automations) radiating outward
- Clicking a category: the view smoothly pans so that category node becomes the new center, its hack nodes fan out around it with full room to breathe. Only one category open at a time.
- Clicking ESC or anywhere outside the tree: view pans back to global center, category collapses
- **Left click a hack** — toggles it on/off
- **Right click a hack** — expands into settings sub-nodes (sliders, value inputs, per-hack toggles)

**Camera behavior:**
- Global view shows the central node + all 5 category nodes, nothing cramped
- Selecting a category pans the camera so that category is centered — solves space constraints entirely
- Pan easing: ~150ms, fast and snappy. Not a slow cinematic drift.
- The central "Barium" node remains faintly visible at the edge when a category is open, preserving spatial awareness

**Visual language — nodes:**
- Every node is a plain white circle with its label text centered inside it
- Inactive nodes: dim white stroke, low opacity fill, muted label
- Active hack nodes: brighter stroke, slightly glowing, full white label
- Node size: category nodes slightly larger than hack nodes

**Visual language — branches:**
- Straight lines, never curved
- Color: white with a soft glow (`rgba(255,255,255,0.65)`, blur/glow ~9px)
- Inactive branches are dim; active hack branches are slightly brighter

**Visual language — rainbow refraction at contact points:**
- Where a branch line meets a node's circumference, the line refracts into a spectrum arc
- The arc is symmetrical around the contact point: red at the exact center of contact, bleeding outward in both directions through orange → yellow → green → blue → purple → fading back to white at the edges
- The rest of the node circumference remains plain white
- This applies to every node connection — every contact point is its own prism moment, consistent with the Barium logo visual language

**Animation:**
- When a category is clicked and its hack nodes appear, branches grow outward from the category node — fast and subtle, ~150-200ms easing
- Not a slow reveal — just enough motion to feel alive without being annoying mid-fight

### v1 Hacks (initial release)
| Category | Hacks |
|---|---|
| Combat | MultiAura, Reach |
| Movement | Speed |
| Render/ESP | XRay |

All others added in subsequent versions.

---

## Layer 3: The Overlay

### Technology
- Separate Tauri window: `always_on_top`, transparent background, click-through when idle
- Communicates with the Fabric mod via **local WebSocket** (mod opens WS server on localhost, overlay connects)
- Windows `SetWindowDisplayAffinity` — invisible to screen capture/share if implemented

### Features
- Floating HUD showing currently active hacks
- **Panic button** — one keypress (customizable), all hacks soft-disable instantly. State is fully saved.
- **Restore button** — second keypress, all hacks return exactly to their pre-panic state. No reconfiguration.
- Module status indicators update in real time via WebSocket

---

## Multi-Version Architecture

### Structure
```
barium-hacks/
├── core/           ← version-agnostic module logic (reach values, velocity math, etc.)
└── versions/
    ├── 1.21.x/     ← mixin hooks for 1.21 family
    ├── 1.20.x/
    ├── 1.19.x/
    └── ...
```

- Module logic lives in `core/` and is shared across all versions
- Only the Mixin injection targets change per version (obfuscation mappings differ)
- One artifact per minor version family — 1.21.x covers 1.21, 1.21.1, 1.21.4, etc.
- Target: all 1.21+ versions. Older versions best-effort.

---

## Communication Flow

```
Launcher (Tauri)
  └── launches MC with Fabric + Barium mod injected
        └── Barium Fabric mod (Java)
              ├── loads hack modules
              ├── opens localhost WebSocket server
              └── Overlay (Tauri window, always on top)
                    ├── reads module state via WebSocket
                    └── sends toggle/panic commands back
```

---

## File Structure

```
.minecraft/barium/
├── mods/           ← all mods managed by Barium (separate from .minecraft/mods)
├── profiles/       ← JSON profile configs
├── hacks/          ← hack module configs
└── logs/           ← game log mirror
```

---

## Branding

- **Name:** Barium (Ba, atomic number 56)
- **Logo:** "Ba" in a large, thin weight (200–300) — premium, periodic-table aesthetic. Paired with the atomic subtitle `56 · Ba · 137.33` in wide letter-spacing below.
- **Color language:** Pure black backgrounds, white as primary, spectrum/rainbow as accent. The spectrum gradient (red → yellow → green → blue → violet) appears on: active toggle switches, the play button border and text, the hacks mod card background tint and text, active hack branches in the in-game menu.
- **Typography:** Custom titlebar and UI — premium, clean, no generic system fonts. "Ba" logo in ultra-light weight. UI labels in medium (500) weight with wide letter-spacing for headings.
- **Atomic subtitle:** `56 · Ba · 137.33` used as a design motif

---

## Visual Design Language

The launcher uses a single consistent surface language across all sections.

**Glass card:** The primary surface is a frosted glass card — `rgba(255,255,255,0.03–0.05)` background, `1px rgba(255,255,255,0.09–0.12)` border, subtle top inner highlight (`inset 0 1px 0 rgba(255,255,255,0.07)`), `20px` border radius. Used for the hero card, mod cards, version selector, search bar, and profile highlights.

**Black base:** The window background and all negative space is pure black (`#000`). No grey backgrounds, no surface hierarchy beyond the glass cards.

**Spectrum accent:** A linear gradient — `#ff6b6b → #ffd93d → #6bcb77 → #4d96ff → #c77dff` — used only on interactive or active elements. Never decorative. Applied as a border, text fill, or background tint depending on context.

**Sidebar:** Sits outside all glass cards, separated by a `1px rgba(255,255,255,0.06)` divider. Profile entries are bare text; the active profile gets a glass card treatment.

**Titlebar:** Minimal. Barium wordmark left (small spectrum circle icon + "BARIUM" in wide tracking), window controls right as small dim circles.

---

## Future / v2 Features (not in scope for initial build)
- Settings page with "auto-close launcher on game start" toggle
- More hack modules beyond the v1 four
- Profile import/export
- Modrinth mod browser directly in launcher (search and add mods without leaving the app)
- Cross-version mixin coverage for pre-1.19 versions
