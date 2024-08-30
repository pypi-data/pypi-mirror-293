import os
from pathlib import Path

from NikGapps.helper import Config
from NikGapps.helper.Package import Package
from NikGapps.helper.FileOp import FileOp
from NikGapps.helper.Cmd import Cmd
from NikGapps.helper.AppSet import AppSet
from NikGapps.helper.Statics import Statics


class Build:
    project_name = "NikGapps"

    # Just provide the package list, and it will pick them up from the directory and build them for you
    @staticmethod
    def build_from_directory(app_set_build_list, android_version, cached=False):
        source_directory = Config.CACHED_SOURCE if cached else Config.APK_SOURCE
        print(f"Building from {source_directory}")
        cmd = Cmd()
        app_set_list = []
        for app_set in app_set_build_list:
            app_set: AppSet
            name = app_set.title
            app_set_path = os.path.join(source_directory, name)
            package_list = []
            for package in app_set.package_list:
                package: Package
                print(f"Setting up {name}/{package.package_title}")
                pkg_to_build = package
                package_title = pkg_to_build.package_title
                pkg_path = os.path.join(str(app_set_path), package_title)
                file_dict = dict()
                folder_dict = dict()
                install_list = []
                package_name = None
                app_type = None
                primary_app_location = None
                delete_files_list = []
                delete_overlay_list = []
                if float(android_version) >= 12.1:
                    overlay_directory = Config.OVERLAY_SOURCE
                    overlay_dir = overlay_directory + Statics.dir_sep + f"{package_title}Overlay"
                    if FileOp.dir_exists(overlay_dir):
                        for file in Path(overlay_dir).rglob("*.apk"):
                            pkg_files_path = "overlay" + Statics.dir_sep + Path(file).name
                            install_list.append(pkg_files_path.replace("___", "/"))
                            file_dict_value = str(pkg_files_path.replace("___", "/")).replace("\\", "/")
                            value = str(file_dict_value).split("/")
                            file_dict[str(file)] = "___" + "___".join(value[:len(value) - 1]) + "/" + value[
                                len(value) - 1]
                for pkg_files in Path(pkg_path).rglob("*"):
                    if Path(pkg_files).is_dir() or str(pkg_files).__contains__(".git") \
                            or str(pkg_files).endswith(".gitattributes") or str(pkg_files).endswith("README.md"):
                        continue
                    if str(pkg_files).endswith(Statics.DELETE_FILES_NAME):
                        for str_data in FileOp.read_string_file(pkg_files):
                            delete_file = str_data[:-1]
                            if delete_file not in pkg_to_build.delete_files_list:
                                delete_files_list.append(delete_file)
                        continue
                    pkg_files_path = str(pkg_files)
                    pkg_files_path = pkg_files_path[pkg_files_path.find("___") + 3:]
                    if pkg_files_path.replace("\\", "/").__eq__(f"etc___permissions/{package.package_name}.xml"):
                        continue
                    if pkg_to_build.package_name is not None and str(pkg_files_path).endswith(".apk") and not str(
                            pkg_files).__contains__("split_") and not str(pkg_files).__contains__("___m") \
                            and not str(pkg_files).__contains__("___overlay"):
                        primary_app_location = pkg_files.absolute()
                        package_name = cmd.get_package_details(primary_app_location, "name")
                        # print("File: " + package_name)
                        # package_version = cmd.get_package_details(primary_app_location, "versionName")
                        # print("Package Version: " + package_version)
                        # package_code = cmd.get_package_details(primary_app_location, "versionCode")
                        # print("Package Code: " + package_code)
                        if str(primary_app_location).__contains__("___priv-app___"):
                            app_type = Statics.is_priv_app
                        elif str(primary_app_location).__contains__("___app___"):
                            app_type = Statics.is_system_app
                    for folder in FileOp.get_dir_list(pkg_files_path):
                        if folder.startswith("system") or folder.startswith("vendor") \
                                or folder.startswith("product") or folder.startswith("system_ext") \
                                or folder.startswith("overlay"):
                            continue
                        folder_dict[folder] = folder
                    # We don't need this but for the sake of consistency
                    if str(pkg_files_path).endswith("xml") or str(pkg_files_path).endswith("prop"):
                        FileOp.convert_to_lf(str(pkg_files.absolute()))
                    install_list.append(pkg_files_path.replace("___", "/"))
                    file_dict_value = str(pkg_files_path.replace("___", "/")).replace("\\", "/")
                    value = str(file_dict_value).split("/")
                    file_dict[pkg_files.absolute()] = "___" + "___".join(value[:len(value) - 1]) + "/" + value[
                        len(value) - 1]
                if primary_app_location is not None:
                    title = os.path.basename(primary_app_location)[:-4]
                else:
                    title = package_title
                pkg = Package(title, package_name, app_type, package_title)
                pkg.install_list = install_list
                pkg.partition = pkg_to_build.partition
                pkg.clean_flash_only = pkg_to_build.clean_flash_only
                pkg.file_dict = file_dict
                pkg.folder_dict = folder_dict
                pkg.addon_index = pkg_to_build.addon_index
                pkg.additional_installer_script = pkg_to_build.additional_installer_script
                pkg.primary_app_location = primary_app_location
                # Generate priv-app permissions whitelist
                if pkg.primary_app_location is not None and app_type == Statics.is_priv_app:
                    permissions_list = cmd.get_white_list_permissions(primary_app_location)
                    for perm in pkg_to_build.priv_app_permissions:
                        permissions_list.append(perm)
                    if permissions_list.__len__() >= 1 and not permissions_list[0].__contains__("Exception"):
                        pkg.priv_app_permissions_str = pkg.generate_priv_app_whitelist(app_set.title, permissions_list,
                                                                                       android_version=android_version,
                                                                                       pkg_path=source_directory)
                # Add the deleted files from the pkg_to_build object
                for delete_file in pkg_to_build.delete_files_list:
                    delete_files_list.append(delete_file)
                pkg.delete_files_list = delete_files_list
                for delete_overlay in pkg_to_build.delete_overlay_list:
                    delete_overlay_list.append(delete_overlay)
                pkg.delete_overlay_list = delete_overlay_list
                pkg.validation_script = pkg_to_build.validation_script
                pkg.overlay_list = pkg_to_build.overlay_list
                package_list.append(pkg)
            if package_list.__len__() > 0:
                app_set_to_build = AppSet(app_set.title, package_list)
                app_set_list.append(app_set_to_build)
        return app_set_list
