# Package Manager

The Package Manager is an add-on designed to streamline the management of Python packages directly within Blender. It provides an easy-to-use interface for searching, installing, and managing Python packages, along with bulk download capabilities for package requirements.

This add-on aims to simplify the workflow for Blender users who need to manage Python packages for scripting and plugin development. It eliminates the need to use external package managers by integrating package management into the Blender interface.

![Package Installer 1](https://github.com/user-attachments/assets/d0238775-e577-478e-a37f-ff95e1290e16)

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

1. **Find Blender's Python Executable**: Blender comes with its own bundled Python interpreter. You need to find where this interpreter is located.
    - Open Blender.
    - Go to the **Scripting** tab.
    - In the Python console within Blender, run the following command to find the path to the Python executable:
        
        ```python
        import sys
        print(sys.executable)
        ```
        
    
    This will print the path to Blender's Python executable, which will look something like `/path/to/blender/2.93/python/bin/python`.
    
2. **Open Command Prompt or Terminal**: Open your command prompt (Windows) or terminal (Mac/Linux).
3. **Navigate to Blender's Python Executable Directory**: Navigate to the directory containing Blender's Python executable. For example:
    
    ```bash
    cd /path/to/blender/2.93/python/bin
    ```
    
4. **Install the Package Using Blender's Python**: Use Blender's Python executable to install the `bs4` package (or any other required package). Replace `path/to/python` with the actual path you obtained in step 1.
    
    ```bash
    ./python -m ensurepip
    ./python -m pip install bs4
    
    # IN WINDOWS
    cd "C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\bin" # EXAMPLE PATH
    python.exe -m ensurepip
    python.exe -m pip install bs4
    
    # IN MAC OS
    cd /Applications/Blender.app/Contents/Resources/2.93/python/bin # EXAMPLE PATH
    ./python3.7m -m ensurepip
    ./python3.7m -m pip install bs4
    ```
    
5. **Download the Add-On:**
    - Save the script from this repository.
6. **Install the Add-On in Blender:**
    - Open Blender.
    - Go to `Edit` > `Preferences` > `Add-ons`.
    - Click `Install...` and select the `Package-Manager.zip` file.
    - Enable the add-on by checking the checkbox next to "Package Manager."
7. **Access the Panel:**
    - Switch to the Text Editor workspace.
    - You will find the "Package Manager" panel in the UI tab on the left side of the Text Editor.

## Notes

- The add-on requires Blender 2.82 or higher.
- Internet access is required for searching and downloading packages.
- Once the package is installed/remove it requires restart to apply changes.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions for improvements. Contributions are welcome!

