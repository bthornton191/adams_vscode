# Adams CMD Object Naming Conventions

## Dot-Path Hierarchy

Adams objects live in a tree rooted at the model:

```
.MODEL_NAME
├── ground                  (always present; the fixed reference part)
│   ├── MARKER_A
│   └── MARKER_B
├── PART_1
│   ├── cm                  (center-of-mass marker, auto-created)
│   ├── M_PIN
│   └── M_TIP
└── PART_2
    ├── cm
    └── M_END
```

Full names always start with a dot: `.MODEL_NAME.PART_NAME.MARKER_NAME`

## Ground Part

- Always named `.MODEL_NAME.ground` (lowercase by Adams convention).
- Represents the inertial (fixed) reference frame.
- You can create markers on `ground` just like any other part.

## Reserved / Auto-Created Names

| Object | Auto-created marker | Notes |
|--------|--------------------|-|
| Every rigid part | `cm` | Center of mass and principal inertia axes |
| Model | `ground` | The fixed part |

Do not name your own markers `cm` — it will conflict with the auto-created marker.

## Naming Best Practices

| Practice | Example |
|----------|---------|
| Use ALL_CAPS with underscores | `M_PIN`, `LINK_A`, `REV_JOINT_1` |
| Prefix markers with `M_` | `M_PIN`, `M_TIP`, `M_BASE` |
| Prefix joints with the type | `REV_KNEE`, `TRANS_SLIDER` |
| Prefix forces with the type | `SPR_MAIN`, `BUSH_MOUNT` |
| Avoid spaces and special characters | Use `_` instead of spaces or hyphens |
| Keep names ≤ 32 characters | Longer names work but truncate in some output formats |

## adams_id vs Object Names

- `adams_id` is a positive integer used in solver dataset (`.adm`) files.
- In CMD scripting, always reference objects by their **full dot-path name**, not by ID.
- IDs are assigned sequentially per element type; Adams View manages them automatically.
- Only specify `adams_id` explicitly when round-tripping with `.adm` files or user subroutines that use ID lookups.

## Short-Form (Relative) References

When scripting within a model, you can sometimes use relative names (omitting the model prefix), but **always use the full dot-path in macros and file-based scripts** to avoid ambiguity.

```cmd
! Relative (works interactively in context of MY_MODEL)
constraint create joint revolute joint_name = REV_1 ...

! Full path (always safe in scripts)
constraint create joint revolute joint_name = .MY_MODEL.REV_1 ...
```

## See also

- [model-parts-markers.md](commands/model-parts-markers.md) — creation commands
