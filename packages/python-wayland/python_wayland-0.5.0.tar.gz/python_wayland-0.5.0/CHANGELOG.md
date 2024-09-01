### Changelog

### v0.5.0 (31st August 2024)
- Support multiple wayland context not just a single global context.
- Support debug output without full protocol level debugging output.
- Fix for rapid events passing file descriptors
- Slightly extended unit tests.

### v0.4.1 (28th August 2024)
- Fix pypi package build.

### v0.4.0 (27th August 2024)
- Renamed to python-wayland

### v0.3.0 (26th August 2024)
- File descriptors received in events are now not implicitly converted to Python file objects.
- Add --verbose command line switch for more output when updating protocol files.
- Add --compare option to compare locally installed and latest official protocol definitions.
- Add interface version and description to type checking / intellisense file.
- Add interface version to protocols.json runtime file.

#### v0.2.0 (22nd August 2024)
- Improve low-level socket handling.
- Add support for file descriptors in events.
- Add support for Wayland enum data type.
- Add support for Wayland "fixed" floating point types.
- Search for Wayland protocol definitions online and locally.

#### v0.1.0 (17th August 2024)
- Initial commit.
