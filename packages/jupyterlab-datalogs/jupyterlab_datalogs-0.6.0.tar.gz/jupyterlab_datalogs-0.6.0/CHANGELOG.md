# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0] (Apr 29 2024)

- Public release of JupyterLab DataLogs.

## [0.5.0] (Apr 18 2024)

### Changed

- Renamed package from `jupyterlab-datalogger` to `jupyterlab-datalogs` to be consistent
  with the renamed DataLogs package.

## [0.4.1] (Jan 19 2024)

### Fixed

- The "RTC:" prefix is now removed from paths when using Jupyter Real-Time Collaboration.

## [0.4.0] (Nov 10 2023)

### Added

- Recommended plugins (including the PDF preview and open warning plugins) can be
  installed using the `plugins` extra.

### Changed

- Moved PDF preview plugin to https://github.com/PainterQubits/jupyterlab-pdf-preview.
- Moved open warning plugin to https://github.com/PainterQubits/jupyterlab-open-warning.

## [0.3.1] (Oct 30 2023)

### Fixed

- PDF preview displaying before being positioned properly.

## [0.3.0] (Oct 25 2023)

### Added

- JupyterLab plugin to display a warning dialog when opening a file that another user has
  open.

## [0.2.0] (Oct 20 2023)

### Added

- JupyterLab plugin to preview PDF files in the file browser on hover.

### Changed

- Generated code to load data logs now plots data variables in separate plots.

## [0.1.0] (Oct 2 2023)

### Added

- JupyterLab plugin to add NetCDF mimetype and file icon.
- JupyterLab plugin that adds shortcuts to generate code that loads logs with DataLogs.

[unreleased]: https://github.com/PainterQubits/jupyterlab-datalogs/compare/v0.6.0...main
[0.6.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.6.0
[0.5.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.5.0
[0.4.1]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.4.1
[0.4.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.4.0
[0.3.1]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.3.1
[0.3.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.3.0
[0.2.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.2.0
[0.1.0]: https://github.com/PainterQubits/jupyterlab-datalogs/releases/tag/v0.1.0
