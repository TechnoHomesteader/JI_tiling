# References

## Quasicrystals and projection method

- Marjorie Senechal, *Quasicrystals and Geometry* (Cambridge University Press, 1995).
  Source for the 5D cyclic permutation (rotation) matrix and the cut-and-project construction; see p. 62 for the eigenvector basis used in `basis2D`.

- NumberCruncher, "Penrose Tilings from Five Dimensions," YouTube.
  <https://www.youtube.com/watch?v=jJOTM2UGx70&t=323s>
  Mathematica notebook walkthrough that inspired `penrose5D.ipynb`.

- Dugan Hammock, lecture at ~40′55″ in <https://youtu.be/SPXceXPm9Wg?si=N7bosvtZWSwlN1VB>
  Explains the equivalence between membership in the 2D projection plane and existence as a 3D volume in perpendicular space.

## Just intonation

- Erv Wilson, *The Hexadic Diamond* (Anaphoria).
  <https://www.anaphoria.com/diamond.pdf>
  Source for the pitch-ratio lattice structure explored in `hexadicDiamond.ipynb`.

## Psychoacoustics

- R. Plomp and W. J. M. Levelt, "Tonal Consonance and Critical Bandwidth," *Journal of the Acoustical Society of America* 38 (1965), 548–560.
  Foundation of the roughness/dissonance model implemented in `sethares.ipynb`.

- William A. Sethares, *Tuning, Timbre, Spectrum, Scale*, 2nd ed. (Springer, 2005).
  Practical implementation of the Plomp–Levelt model; `sethares.ipynb` follows this treatment.

## Algorithms

- Stack Overflow, "What's an efficient way to find if a point lies in the convex hull of a point cloud?"
  <https://stackoverflow.com/questions/16750618/>
  Source for `in_hull` in `ji_tiling.py`.

- Stack Overflow, "How to get all subsets of a set? (Power set)"
  <https://stackoverflow.com/questions/1482308/>
  Source for `subSet` in `ji_tiling.py`.

- Stack Exchange / SuperCollider forum — bilinear interpolation for quadrilateral amplitude scaling (`ampScale` in `tiling.scd`).
