# Adams Flex Toolkit Reference

## Table of Contents
1. [Launching the Toolkit](#launching)
2. [MNF / MD DB Browser](#browser)
3. [Optimization Utilities](#optimization)
4. [Command-Line Utilities](#cli)
   - [mnf2mtx — Convert MNF to MD DB](#mnf2mtx)
   - [mnfload — Add Load Cases to MNF](#mnfload)
5. [Load Case Syntax Reference](#loadcase-syntax)
6. [Environment Initialization](#environment)

---

## Launching the Toolkit {#launching}

**Adams View**: Tools → Adams Flex Toolkit  
**Standalone**: Start Menu → Adams → Adams Flex Toolkit (or from command line)

The toolkit GUI provides the MNF/MD DB browser, optimization tools, and transform/edit utilities.

---

## MNF / MD DB Browser {#browser}

Use the browser to inspect a flex body file before importing into Adams.

### What You Can Check
- **Node list**: all node IDs, their coordinates, and attachment flags (interface vs interior)
- **Mode shapes**: animate each mode to verify deformation character and identify spurious modes
- **Modal properties**: natural frequencies, generalized mass, generalized stiffness per mode
- **Nodal masses**: required for contour/vector plotting of modal forces in post-processing
- **Load cases**: preloads and applied loads stored in the MNF (if exported with `mnfload`)
- **Units**: confirm length, mass, force, time units match your Adams model

### Getting Node IDs for Markers
The browser is the primary way to find node IDs for marker placement:
1. Open MNF in browser
2. Click on a node in the geometry view — the node ID highlights in the node list
3. Note the ID and use it in `MARKER/id, FLEX_BODY=id, NODE_ID=<id>` or `flex.Markers.create(node_id=<id>)`

---

## Optimization Utilities {#optimization}

Available in the toolkit GUI: File → Optimize MNF

| Operation | Effect | When to Use |
|---|---|---|
| **Mesh coarsening** | Reduces node count for animation (modes unchanged) | Animation is slow due to large mesh; no effect on physics |
| **Interior geometry removal** | Removes internal structural nodes from graphics mesh | Complex internal structure cluttering animation |
| **MFORCE node optimization** | Selects subset of nodes for modal force application | Large model with distributed load cases |
| **Stress/strain shortening** | Converts full stress modes to shortened format | Large MNF file size; Adams < 2005 compatibility |
| **Full ↔ Sparse conversion** | Toggles between full and sparse mode storage | Format compatibility with older Adams versions |

### File Size Guidance
A large MNF (> 500 MB) will:
- Slow initial import into Adams
- Increase `.mtx` matrix file generation time
- Slow animation (mesh rendering)
- **Not** directly slow physics computation (modes are what matters, not nodes)

For physics performance, focus on **mode count reduction** (see flex-body-setup.md). For import/animation performance, use mesh coarsening.

---

## Command-Line Utilities {#cli}

All toolkit commands require the Adams environment to be initialized first. See [Environment Initialization](#environment).

### mnf2mtx — Convert MNF to MD DB {#mnf2mtx}

Converts an MNF file to a Nastran-format MD DB matrix file, or appends a flex body to an existing database.

**Windows**:
```cmd
adams2023_1 flextk mnf2mtx <source.mnf> -O <dest.MASTER>
```

**Linux**:
```bash
adams2023_1 -c flextk mnf2mtx <source.mnf> -O <dest.MASTER>
```

**Appending multiple MNFs to one database** (creates INDEX=1, INDEX=2, ...):
```cmd
adams2023_1 flextk mnf2mtx first_body.mnf -O combined.MASTER
adams2023_1 flextk mnf2mtx second_body.mnf -O combined.MASTER
```
The second call increments the INDEX automatically.

**Using the database in Adams**:
```python
flex1 = m.Parts.createFlexBody(name='BODY_1', md_db_file_name='combined.MASTER', index_in_database=1)
flex2 = m.Parts.createFlexBody(name='BODY_2', md_db_file_name='combined.MASTER', index_in_database=2)
```

---

### mnfload — Add Load Cases to MNF {#mnfload}

Appends preloads or applied modal loads to an existing MNF. Use when your FEA software exports the MNF without load data, or when adding loads post-export.

**Windows**:
```cmd
adams2023_1 flextk mnfload <existing.mnf> <new.mnf> <loadcase_file.txt>
```

**Linux**:
```bash
adams2023_1 -c flextk mnfload <existing.mnf> <new.mnf> <loadcase_file.txt>
```

- `existing.mnf` — source MNF (unchanged)
- `new.mnf` — output MNF with loads appended
- `loadcase_file.txt` — text file specifying load cases (see [Load Case Syntax](#loadcase-syntax))

---

## Load Case Syntax Reference {#loadcase-syntax}

The load case file passed to `mnfload` defines preloads and applied loads in Cartesian or modal coordinates.

### Load Type Prefixes
| Prefix | Type | Description |
|---|---|---|
| `% PC` | Cartesian Preload | Permanent pre-deformation at specified nodes (Cartesian forces) |
| `% PM` | Modal Preload | Permanent pre-deformation in modal coordinates |
| `% C` | Cartesian Applied Load | Scalable load applied during Adams simulation (Cartesian forces) |
| `% M` | Modal Applied Load | Scalable load applied during Adams simulation (modal forces) |

### File Format
```
% PC preload_name
node_id FX value
node_id FY value
node_id FZ value
node_id MX value
node_id MY value
node_id MZ value

% PM preload_modal_name
mode_number value
mode_number value

% C applied_load_name
node_id FX value
node_id FY value
node_id FZ value

% M modal_applied_load_name
mode_number value
mode_number value
```

### Example
```
% PC gravity_preload
1001 FZ -9.81
1002 FZ -9.81
1003 FZ -4.905

% C braking_load
1050 FX 5000.0
1051 FX 5000.0
1052 FX 2500.0

% M aero_modal_load
3 1500.0
5 750.0
7 -200.0
```

### Using Loads in Adams
After `mnfload`, load cases appear in:
- Adams View: Flexible Body Modify → Loads tab → Load Case Selection
- `.adm` dataset: via `MATRIX/n, FILE=*.mtx, NAME=MODLOAD` references

---

## Environment Initialization {#environment}

The Adams Flex Toolkit CLI commands require the Adams environment to be active.

**Recommended**: Use the `generate_adams_env.py` script (from the `adams-subroutine-writer` skill) to generate an `adams_env_init.bat` file:
```powershell
python "<adams_skills_dir>/skills/adams-subroutine-writer/scripts/generate_adams_env.py"
call "%LOCALAPPDATA%\adams_env_init.bat"
```

**Manual (Windows)** — run from the Adams Command Prompt (Start Menu → MSC Software → Adams → Adams Command Prompt):
```cmd
adams2023_1 flextk mnf2mtx ...
```

**Manual (Linux)**:
```bash
source /usr/MSC.Software/Adams/2023_1/Adams/configure.sh
adams2023_1 -c flextk mnf2mtx ...
```
