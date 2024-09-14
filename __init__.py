import bpy
import sys
import os
import subprocess
import site
import requests
from bs4 import BeautifulSoup
import pkg_resources
from bpy_extras.io_utils import ImportHelper

def search_pypi_html(query):
    base_url = 'https://pypi.org/search/'
    params = {'q': query}

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching search results from PyPI. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for result in soup.select('.package-snippet'):
        name = result.select_one('.package-snippet__name').text.strip()
        version = result.select_one('.package-snippet__version').text.strip()
        summary = result.select_one(
            '.package-snippet__description').text.strip()
        results.append({'name': name, 'version': version, 'summary': summary})

    return results


def install_package(package):
    try:
        __import__(package)
        print(f"{package} is already installed.")
        return True
    except ImportError:
        print(f"{package} not found. Installing...")
        python_exec = sys.executable

        try:
            subprocess.check_call([python_exec, "-m", "ensurepip"])
            subprocess.check_call(
                [python_exec, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call(
                [python_exec, "-m", "pip", "install", package])

            user_site = site.getusersitepackages()
            if user_site not in sys.path:
                sys.path.append(user_site)
                print(f"Added {user_site} to sys.path")

            __import__(package)
            print(f"{package} installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")
            return False
        except ImportError as e:
            print(f"Failed to import {package} after installation. Error: {e}")
            print("sys.path:", sys.path)
            return False


def install_packages_from_requirements(file_path, context):
    if not os.path.isfile(file_path):
        print(f"Requirements file not found: {file_path}")
        return False

    with open(file_path, 'r') as f:
        requirements = f.readlines()

    requirements = [req.strip() for req in requirements if req.strip()]

    wm = context.window_manager
    wm.progress_begin(0, 100)
    total = len(requirements)

    for i, package in enumerate(requirements):
        if install_package(package):
            print(f"Package {package} installed successfully.")
        else:
            print(f"Failed to install {package}.")

        wm.progress_update((i / total) * 100)

    wm.progress_end()
    return True


def uninstall_package(package):
    python_exec = sys.executable

    try:
        installed_packages = get_installed_packages()
        installed_names = [pkg['name'].lower() for pkg in installed_packages]

        if package.lower() not in installed_names:
            print(f"Package {package} not found. Skipping uninstall.")
            return False

        subprocess.check_call(
            [python_exec, "-m", "pip", "uninstall", "-y", package])
        print(f"{package} uninstalled successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during uninstallation: {e}")
        return False


def get_installed_packages():
    installed_packages = []
    for dist in pkg_resources.working_set:
        installed_packages.append({
            'name': dist.project_name,
            'version': dist.version
        })
    return installed_packages

class PackageManagementPanel(bpy.types.Panel):
    """Creates a Panel in the Text Editor side panel"""
    bl_label = "Package Manager"
    bl_idname = "TEXT_PT_package_manager"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Packages'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Search Packages:")
        row = layout.row()
        row.prop(context.scene, "search_query", text="")
        row.operator("wm.search_packages", text="Search")

        layout.label(text="Results Per Page:")
        row = layout.row()
        row.prop(context.scene, "pagination_limit", expand=True)

        box = layout.box()
        row = box.row()
        row.prop(context.scene, "show_search_results", text="Show Search Results",
                 icon='TRIA_DOWN' if context.scene.show_search_results else 'TRIA_RIGHT')
        if context.scene.show_search_results:
            if context.scene.package_list:
                for package in context.scene.package_list[:int(context.scene.pagination_limit)]:
                    box = layout.box()
                    row = box.row()
                    row.label(text=package.name, icon='FILE_SCRIPT')
                    row.label(text=f"v{package.version}")
                    row.operator("wm.download_package",
                                 text="Download").package_name = package.name
            else:
                box.label(text="No results found.")

        layout.separator()
        layout.label(text="Installed Packages:")

        row = layout.row()
        row.prop(context.scene, "installed_search_query",
                 text="Search Installed Packages")
        row.operator("wm.search_installed_packages", text="Search")

        layout.operator("wm.refresh_installed_packages", text="Refresh")

        box = layout.box()
        row = box.row()
        row.prop(context.scene, "show_installed_packages", text="Show Installed Packages",
                 icon='TRIA_DOWN' if context.scene.show_installed_packages else 'TRIA_RIGHT')
        if context.scene.show_installed_packages:
            filtered_packages = [pkg for pkg in context.scene.installed_package_list
                                 if context.scene.installed_search_query.lower() in pkg.name.lower()]
            if filtered_packages:
                for package in filtered_packages:
                    box = layout.box()
                    row = box.row()
                    row.label(text=package.name, icon='FILE_SCRIPT')
                    row.label(text=f"v{package.version}")
                    row.operator("wm.disable_package",
                                 text="Disable").package_name = package.name
                    row.prop(package, "auto_update", text="Auto Update")
            else:
                box.label(text="No installed packages match the search query.")

        layout.separator()
        layout.label(text="Bulk Download Packages:")
        layout.prop(context.scene, "bulk_download_path", text="Selected Path")
        layout.operator("wm.file_select", text="Choose File Path")
        layout.operator("wm.bulk_download_packages", text="Download All")


class WM_OT_FileSelect(bpy.types.Operator, ImportHelper):
    """Operator to open the file browser"""
    bl_idname = "wm.file_select"
    bl_label = "Select Bulk Download Path"

    filter_glob: bpy.props.StringProperty(default="*", options={'HIDDEN'})

    def execute(self, context):
        context.scene.bulk_download_path = self.filepath
        self.report({'INFO'}, f"Selected path: {self.filepath}")
        return {'FINISHED'}


class WM_OT_SearchPackages(bpy.types.Operator):
    bl_idname = "wm.search_packages"
    bl_label = "Search Packages"

    def execute(self, context):
        query = context.scene.search_query
        context.scene.package_list.clear()

        try:
            search_results = search_pypi_html(query)

            for result in search_results:
                item = context.scene.package_list.add()
                item.name = result['name']
                item.version = result['version']
                item.description = result['summary']
                item.auto_update = False

            self.report({'INFO'}, f"Found {len(search_results)} packages.")
        except Exception as e:
            self.report({'ERROR'}, f"Error fetching results: {str(e)}")

        return {'FINISHED'}


class WM_OT_RefreshInstalledPackages(bpy.types.Operator):
    bl_idname = "wm.refresh_installed_packages"
    bl_label = "Refresh Installed Packages"

    def execute(self, context):
        context.scene.installed_package_list.clear()
        installed_packages = get_installed_packages()

        for package in installed_packages:
            item = context.scene.installed_package_list.add()
            item.name = package['name']
            item.version = package['version']

        self.report({'INFO'}, f"Found {len(installed_packages)} installed packages.")
        return {'FINISHED'}


class WM_OT_DownloadPackage(bpy.types.Operator):
    bl_idname = "wm.download_package"
    bl_label = "Download Package"

    package_name: bpy.props.StringProperty()

    def execute(self, context):
        package_name = self.package_name
        if install_package(package_name):
            self.report({'INFO'}, f"{package_name} installed successfully.")
        else:
            self.report({'ERROR'}, f"Failed to install {package_name}.")
        return {'FINISHED'}


class WM_OT_DisablePackage(bpy.types.Operator):
    bl_idname = "wm.disable_package"
    bl_label = "Disable Package"

    package_name: bpy.props.StringProperty()

    def execute(self, context):
        package_name = self.package_name
        if uninstall_package(package_name):
            self.report({'INFO'}, f"{package_name} uninstalled successfully.")
        else:
            self.report({'ERROR'}, f"Failed to uninstall {package_name}.")
        return {'FINISHED'}


class WM_OT_BulkDownloadPackages(bpy.types.Operator):
    bl_idname = "wm.bulk_download_packages"
    bl_label = "Bulk Download Packages"

    def execute(self, context):
        file_path = context.scene.bulk_download_path
        if install_packages_from_requirements(file_path, context):
            self.report({'INFO'}, f"Packages from {
                        file_path} installed successfully.")
        else:
            self.report(
                {'ERROR'}, f"Failed to install packages from {file_path}.")
        return {'FINISHED'}


class WM_OT_SearchInstalledPackages(bpy.types.Operator):
    bl_idname = "wm.search_installed_packages"
    bl_label = "Search Installed Packages"

    def execute(self, context):
        search_query = context.scene.installed_search_query.lower()
        for item in context.scene.installed_package_list:
            item.hide = search_query not in item.name.lower()
        return {'FINISHED'}


class PackageItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    version: bpy.props.StringProperty()
    auto_update: bpy.props.BoolProperty()
    hide: bpy.props.BoolProperty(default=False)


classes = (
    PackageManagementPanel,
    WM_OT_SearchPackages,
    WM_OT_RefreshInstalledPackages,
    WM_OT_DownloadPackage,
    WM_OT_DisablePackage,
    WM_OT_BulkDownloadPackages,
    WM_OT_FileSelect,
    WM_OT_SearchInstalledPackages,
    PackageItem

)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.search_query = bpy.props.StringProperty(
        name="Search Query")
    bpy.types.Scene.pagination_limit = bpy.props.EnumProperty(
        items=[
            ('15', '15', 'Show 15 Results'),
            ('25', '25', 'Show 25 Results'),
            ('1000', 'ALL', 'Show All Results')
        ],
        name="Results Per Page",
        default='15'
    )
    bpy.types.Scene.bulk_download_path = bpy.props.StringProperty(
        name="Bulk Download Path")
    bpy.types.Scene.package_list = bpy.props.CollectionProperty(
        type=PackageItem)
    bpy.types.Scene.installed_package_list = bpy.props.CollectionProperty(
        type=PackageItem)
    bpy.types.Scene.show_search_results = bpy.props.BoolProperty(
        name="Show Search Results", default=True)
    bpy.types.Scene.show_installed_packages = bpy.props.BoolProperty(
        name="Show Installed Packages", default=True)
    bpy.types.Scene.installed_search_query = bpy.props.StringProperty(
        name="Search Installed Packages")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.search_query
    del bpy.types.Scene.pagination_limit
    del bpy.types.Scene.bulk_download_path
    del bpy.types.Scene.package_list
    del bpy.types.Scene.installed_package_list
    del bpy.types.Scene.show_search_results
    del bpy.types.Scene.show_installed_packages
    del bpy.types.Scene.installed_search_query

if __name__ == "__main__":
    register()
