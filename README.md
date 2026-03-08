# JI_tiling

Projection of a five-dimensional integer lattice onto a 2D plane using the "cut and project" method, producing Penrose-like quasicrystal tilings. The lattice coordinates are interpreted as exponents of the prime harmonics 3, 5, 7, 9, 11, connecting the geometric structure of the tiling to just intonation pitch ratios. The resulting tiling is then used as a spatial score in SuperCollider.

## Mathematical overview

A 5×5 cyclic permutation matrix is diagonalized; its complex eigenvectors define two orthogonal 2D planes in R⁵. Points of the Z⁵ lattice whose perpendicular-space projections fall inside a convex hull "window" are selected and projected onto the principal plane, forming the quasicrystal tiling. Each rhombus tile vertex corresponds to a rational frequency ratio built from the primes {3, 5, 7, 9, 11}.

## Prerequisites

- Python 3.9+
- SuperCollider (for `tiling.scd`)

## Setup

```bash
pip install -r requirements.txt
```

Then launch JupyterLab or Jupyter Notebook from the repo root:

```bash
jupyter lab
```

## Notebooks

Recommended order:

| Notebook | Description |
|----------|-------------|
| `notebooks/penrose5D.ipynb` | Core notebook. Builds the 5D rotation, selects lattice points via convex-hull cut window, constructs the Penrose tiling, and writes the `Data/` files consumed by SuperCollider. |
| `notebooks/hexadicDiamond.ipynb` | Derives Erv Wilson's Hexadic Diamond from the same 5D projection, annotating projected points with their JI pitch ratios. |
| `notebooks/HypercubeOnPlane.ipynb` | Symbolic derivation of the eigenvectors using SymPy; verifies the projection geometry. |

## Data pipeline

1. Run `notebooks/penrose5D.ipynb` end-to-end.
2. Three CSV files are written to `Data/`:
   - `verts_5Dprojection.txt` — 2D coordinates of each tile's four corners
   - `indices_5Dprojection.txt` — corresponding 5D lattice indices
   - `faces_5Dprojection.txt` — face-direction index (determines tile shape/color)
3. Open `tiling.scd` in SuperCollider and evaluate the setup block to load these files.

## SuperCollider usage

Open `tiling.scd` in the SuperCollider IDE. The file is organized into named blocks separated by `//===` comments:

1. **Boot server** — evaluate the `Server.boot` block first.
2. **Define SynthDefs** — evaluate the SynthDef block to register the instrument.
3. **Read files** — evaluates `~dir`, `~indices`, `~verts`, `~faces` from `Data/`.
4. **Play** — evaluate the main performance block to start the spatial tiling score.

The file path is resolved automatically relative to `tiling.scd` using `thisProcess.nowExecutingPath`, so the repo can be placed anywhere on disk.

## Shared utilities

`ji_tiling.py` at the repo root contains functions used across multiple notebooks:

- `basis2D` — construct 2D projection matrix from eigenvector pair
- `subSet` — length-n subsets of an iterable
- `in_hull` — convex-hull membership test
- `unitVector`, `polygonDataFunction`, `nMemberQ` — tile construction helpers
