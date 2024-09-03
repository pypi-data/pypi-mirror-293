# Changelog
## [Unreleased]
## [v1.4.1]
### Fixed
- Set dimension name in xarray for linked dimensions. This is required to merge across linked dimensions.
- Cleaned up `FileTree.to_string()` output when called in a `FileTree` where multiple different linkages are applied.
## [v1.4.0]
### Added
- Linking can now be applied iteratively. For example, after `tree.placeholders.link("A", "B")` and `tree.placeholders.link("B", "C")`, you will now end up with "A", "B", and "C" all linked to each other.
- New `tree.override` method that allows to update some of the templates in a `FileTree` with that from another `FileTree`.
### Changed
- Conflicting template keys now raise an error when accessing those keys rather than when reading the file-tree.
- Sub file-trees can no longer be defined in the part of the output directory, where they are added in. This was confusing behaviour with no clear use case.
## [v1.3.0]
### Added
- A `link` keyword to `update_glob`, which allows one to indicate that two placeholders should co-vary.
### Changed
- The code repository namespace has been moved to the FSL namespace (https://git.fmrib.ox.ac.uk/fsl/file-tree) and the documentation to the FSL pages (https://fsl.pages.fmrib.ox.ac.uk/file-tree).
- `update_glob` will now always set the top-most level possible (i.e., instead of setting "input/subject" it will set "subject").
### Fixed
- In hierarchical placeholders using in sub-trees, "A/B/C" is now a child of "B/C" rather than "A/C" (both of which are children of "C").
## [v1.2.1]
### Fixed
- Rich is a dependency again as it is required for `Filetree.report`. Textual is still an optional dependency.
## [v1.2.0]
### Added
- Updated error message to suggest similar template key if template key is not found.
### Changed
- Rich and textual dependencies are now optional. Running the terminal user interface (`file-tree`) will require these to be installed.
- The terminal user interface now uses the newest version of textual.
## [v1.1.0]
### Added
- `glob_placeholders` flag in `convert` function to mark placeholders as wildcards
- In the CLI you can now define output targets based on their filename pattern in addition to using the template key.


[Unreleased]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.4.1...master
[v1.4.1]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.4.0...v1.4.1
[v1.4.0]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.3.0...v1.4.0
[v1.3.0]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.2.1...v1.3.0
[v1.2.1]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.2.0...v1.2.1
[v1.2.0]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.1.0...v1.2.0
[v1.1.0]: https://git.fmrib.ox.ac.uk/fsl/file-tree/-/compare/v1.0.0...v1.1.0
