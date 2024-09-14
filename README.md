# Package-Installer

The Package Installer is an add-on designed to streamline the management of Python packages directly within Blender. It provides an easy-to-use interface for searching, installing, and managing Python packages, along with bulk download capabilities for package requirements.

This add-on aims to simplify the workflow for Blender users who need to manage Python packages for scripting and plugin development. It eliminates the need to use external package managers by integrating package management into the Blender interface.

## Usage

### 1. **Search Packages**

- **Search Packages:** Use the "Search Packages" section to find Python packages available on PyPI (Python Package Index). Enter your search query and click "Search" to view results.
- **Install Packages:** From the search results, you can install packages by clicking the "Download" button next to each package.

### 2. **Manage Installed Packages**

- **Refresh Installed Packages:** Click "Refresh" to update the list of installed packages in Blender.
- **Search Installed Packages:** Use the "Search Installed Packages" field to filter the list of installed packages.
- **Disable Packages:** You can uninstall packages by clicking the "Disable" button next to each package. The package list will automatically update to reflect these changes.

### 3. **Bulk Download Packages**

- **Choose File Path:** Use the "Choose File Path" button to select a requirements file containing a list of packages to install.
- **Download All:** Click "Download All" to install all packages listed in the selected requirements file.

## Installation

1. **Download the Add-On:**
    - Save the script from this repository as a `.py` file.
2. **Install the Add-On in Blender:**
    - Open Blender.
    - Go to `Edit` > `Preferences` > `Add-ons`.
    - Click `Install...` and select the saved `.py` file.
    - Enable the add-on by checking the checkbox next to "Package Manager."
3. **Access the Panel:**
    - Switch to the Text Editor workspace.
    - You will find the "Package Manager" panel in the UI tab on the left side of the Text Editor.

## Notes

- The add-on requires Blender 2.82 or higher.
- Internet access is required for searching and downloading packages.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions for improvements. Contributions are welcome!

