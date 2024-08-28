#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import logging
import platform
import re
import base64
import subprocess
import shutil
import fosslight_util.constant as constant
import fosslight_dependency.constant as const
from packageurl.contrib import url2purl

try:
    from github import Github
except Exception:
    pass

logger = logging.getLogger(constant.LOGGER_NAME)

# binary url to check license text
_license_scanner_linux = os.path.join('third_party', 'nomos', 'nomossa')
_license_scanner_macos = os.path.join('third_party', 'askalono', 'askalono_macos')
_license_scanner_windows = os.path.join('third_party', 'askalono', 'askalono.exe')

gradle_config = ['runtimeClasspath', 'runtime']
android_config = ['releaseRuntimeClasspath']


class PackageManager:
    input_package_list_file = []
    direct_dep = False
    total_dep_list = []
    direct_dep_list = []

    def __init__(self, package_manager_name, dn_url, input_dir, output_dir):
        self.input_package_list_file = []
        self.direct_dep = False
        self.total_dep_list = []
        self.direct_dep_list = []
        self.package_manager_name = package_manager_name
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dn_url = dn_url
        self.manifest_file_name = []
        self.relation_tree = {}
        self.package_name = ''
        self.purl_dict = {}
        self.cover_comment = ''

        self.platform = platform.system()
        self.license_scanner_bin = check_license_scanner(self.platform)

    def __del__(self):
        self.input_package_list_file = []
        self.direct_dep = False
        self.total_dep_list = []
        self.direct_dep_list = []
        self.package_manager_name = ''
        self.input_dir = ''
        self.output_dir = ''
        self.dn_url = ''
        self.manifest_file_name = []
        self.relation_tree = {}
        self.package_name = ''

    def run_plugin(self):
        ret = True
        if self.package_manager_name == const.GRADLE or self.package_manager_name == const.ANDROID:
            ret = self.run_gradle_task()
        else:
            logger.info(f"This package manager({self.package_manager_name}) skips the step to run plugin.")
        return ret

    def append_input_package_list_file(self, input_package_file):
        self.input_package_list_file.append(input_package_file)

    def set_manifest_file(self, manifest_file_name):
        self.manifest_file_name = manifest_file_name

    def set_direct_dependencies(self, direct):
        self.direct_dep = direct

    def parse_direct_dependencies(self):
        pass

    def run_gradle_task(self):
        ret_task = True
        if os.path.isfile(const.SUPPORT_PACKAE.get(self.package_manager_name)):
            gradle_backup = f'{const.SUPPORT_PACKAE.get(self.package_manager_name)}_bk'

            shutil.copy(const.SUPPORT_PACKAE.get(self.package_manager_name), gradle_backup)
            ret_alldeps = self.add_allDeps_in_gradle()

            ret_plugin = False
            if (self.package_manager_name == const.ANDROID):
                module_build_gradle = os.path.join(self.app_name, const.SUPPORT_PACKAE.get(self.package_manager_name))
                module_gradle_backup = f'{module_build_gradle}_bk'
                if os.path.isfile(module_build_gradle) and (not os.path.isfile(self.input_file_name)):
                    shutil.copy(module_build_gradle, module_gradle_backup)
                    ret_plugin = self.add_android_plugin_in_gradle(module_build_gradle)

            if os.path.isfile('gradlew') or os.path.isfile('gradlew.bat'):
                if self.platform == const.WINDOWS:
                    cmd_gradle = "gradlew.bat"
                else:
                    cmd_gradle = "./gradlew"
            else:
                ret_task = False
                logger.warning('No gradlew file exists. (skip to find dependencies relationship.')
                if ret_plugin:
                    logger.warning('Also it cannot run android-dependency-scanning plugin.')
            if ret_task:
                if ret_alldeps:
                    cmd = f"{cmd_gradle} allDeps"
                    try:
                        ret = subprocess.check_output(cmd, shell=True, encoding='utf-8')
                        if ret != 0:
                            self.parse_dependency_tree(ret)
                        else:
                            self.set_direct_dependencies(False)
                            logger.warning("Failed to run allDeps task.")
                    except Exception as e:
                        self.set_direct_dependencies(False)
                        logger.error(f'Fail to run {cmd}: {e}')
                        logger.warning('It cannot print the direct/transitive dependencies relationship.')

                if ret_plugin:
                    cmd = f"{cmd_gradle} generateLicenseTxt"
                    try:
                        ret = subprocess.check_output(cmd, shell=True, encoding='utf-8')
                        if ret == 0:
                            ret_task = False
                            logger.error(f'Fail to run {cmd}')
                        if os.path.isfile(self.input_file_name):
                            logger.info('Automatically run android-dependency-scanning plugin and generate output.')
                            self.plugin_auto_run = True
                        else:
                            logger.warning('Automatically run android-dependency-scanning plugin, but fail to generate output.')
                    except Exception as e:
                        logger.error(f'Fail to run {cmd}: {e}')
                        ret_task = False

            if os.path.isfile(gradle_backup):
                os.remove(const.SUPPORT_PACKAE.get(self.package_manager_name))
                shutil.move(gradle_backup, const.SUPPORT_PACKAE.get(self.package_manager_name))

            if (self.package_manager_name == const.ANDROID):
                if os.path.isfile(module_gradle_backup):
                    os.remove(module_build_gradle)
                    shutil.move(module_gradle_backup, module_build_gradle)
        return ret_task

    def add_android_plugin_in_gradle(self, module_build_gradle):
        ret = False
        build_script = '''buildscript {
                            repositories {
                                mavenCentral()
                            }
                            dependencies {
                                //Android dependency scanning Plugin
                                classpath 'org.fosslight:android-dependency-scanning:+'
                            }
                        }'''
        apply = "apply plugin: 'org.fosslight'\n"
        try:
            with open(const.SUPPORT_PACKAE.get(self.package_manager_name), 'r', encoding='utf-8') as original:
                data = original.read()
            with open(const.SUPPORT_PACKAE.get(self.package_manager_name), 'w', encoding='utf-8') as modified:
                modified.write(f"{build_script}\n{data}")
            ret = True
        except Exception as e:
            logging.warning(f"Cannot add the buildscript task in build.gradle: {e}")

        try:
            with open(module_build_gradle, 'a', encoding='utf-8') as modified:
                modified.write(f'\n{apply}\n')
                ret = True
        except Exception as e:
            logging.warning(f"Cannot add the apply plugin in {module_build_gradle}: {e}")
        return ret

    def add_allDeps_in_gradle(self):
        ret = False
        config = android_config if self.package_manager_name == 'android' else gradle_config
        configuration = ','.join([f'project.configurations.{c}' for c in config])

        allDeps = f'''allprojects {{
                   task allDeps(type: DependencyReportTask) {{
                        doFirst{{
                            try {{
                                configurations = [{configuration}] as Set }}
                            catch(UnknownConfigurationException) {{}}
                        }}
                    }}
                    }}'''
        try:
            with open(const.SUPPORT_PACKAE.get(self.package_manager_name), 'a', encoding='utf8') as f:
                f.write(f'\n{allDeps}\n')
                ret = True
        except Exception as e:
            logging.warning(f"Cannot add the allDeps task in build.gradle: {e}")

        return ret

    def create_dep_stack(self, dep_line, config):
        packages_in_config = False
        dep_stack = []
        cur_flag = ''
        dep_level = -1
        dep_level_plus = False
        for line in dep_line.split('\n'):
            try:
                if not packages_in_config:
                    filtered = next(filter(lambda c: re.findall(rf'^{c}\s\-', line), config), None)
                    if filtered:
                        packages_in_config = True
                else:
                    if line == '':
                        packages_in_config = False
                    prev_flag = cur_flag
                    prev_dep_level = dep_level
                    dep_level = line.count("|")

                    re_result = re.findall(r'([\+|\\])\-\-\-\s([^\:\s]+\:[^\:\s]+)\:([^\:\s]+)', line)
                    if re_result:
                        cur_flag = re_result[0][0]
                        if (prev_flag == '\\') and (prev_dep_level == dep_level):
                            dep_level_plus = True
                        if dep_level_plus and (prev_flag == '\\') and (prev_dep_level != dep_level):
                            dep_level_plus = False
                        if dep_level_plus:
                            dep_level += 1
                        dep_name = f'{re_result[0][1]}({re_result[0][2]})'
                        dep_stack = dep_stack[:dep_level] + [dep_name]
                        yield dep_stack[:dep_level], dep_name
                    else:
                        cur_flag = ''
            except Exception as e:
                logger.warning(f"Failed to parse dependency tree: {e}")

    def parse_dependency_tree(self, f_name):
        config = android_config if self.package_manager_name == 'android' else gradle_config
        try:
            for stack, name in self.create_dep_stack(f_name, config):
                self.total_dep_list.append(name)
                if len(stack) == 0:
                    self.direct_dep_list.append(name)
                else:
                    if stack[-1] not in self.relation_tree:
                        self.relation_tree[stack[-1]] = []
                    self.relation_tree[stack[-1]].append(name)
        except Exception as e:
            logger.warning(f'Fail to parse gradle dependency tree:{e}')

    def change_dep_to_purl(self, sheet_list):
        for oss_item in sheet_list:
            try:
                if len(oss_item) < 10:
                    break
                deps_list = oss_item[9]
                deps_purl = list(filter(None, map(lambda x: self.purl_dict.get(x, ''), deps_list)))
                oss_item[9] = ','.join(deps_purl)
            except Exception as e:
                logger.warning(f'Fail to change depend_on to purl:{e}')
        return sheet_list


def get_url_to_purl(url, pkg_manager, oss_name='', oss_version=''):
    purl_prefix = f'pkg:{pkg_manager}'
    purl = str(url2purl.get_purl(url))
    if not re.match(purl_prefix, purl):
        match = re.match(constant.PKG_PATTERN.get(pkg_manager, 'not_support'), url)
        try:
            if match and (match != ''):
                if pkg_manager == 'maven':
                    purl = f'{purl_prefix}/{match.group(1)}/{match.group(2)}@{match.group(3)}'
                elif pkg_manager == 'pub':
                    purl = f'{purl_prefix}/{match.group(1)}@{match.group(2)}'
                elif pkg_manager == 'cocoapods':
                    match = re.match(r'([^\/]+)\/?([^\/]*)', oss_name)  # ex, GoogleUtilities/NSData+zlib
                    purl = f'{purl_prefix}/{match.group(1)}@{oss_version}'
                    if match.group(2):
                        purl = f'{purl}#{match.group(2)}'
                elif pkg_manager == 'go':
                    purl = f'{purl_prefix}lang/{match.group(1)}@{match.group(2)}'
            else:
                if pkg_manager == 'swift':
                    if oss_version:
                        purl = f'{purl_prefix}/{oss_name}@{oss_version}'
                    else:
                        purl = f'{purl_prefix}/{oss_name}'
                elif pkg_manager == 'carthage':
                    if oss_version:
                        purl = f'{purl}@{oss_version}'
        except Exception:
            logger.debug('Fail to get purl. So use the link purl({purl}).')
    return purl


def version_refine(oss_version):
    version_cmp = oss_version.upper()

    if version_cmp.find(".RELEASE") != -1:
        oss_version = version_cmp.rstrip(".RELEASE")
    elif version_cmp.find(".FINAL") != -1:
        oss_version = version_cmp.rstrip(".FINAL")

    return oss_version


def connect_github(github_token):
    if github_token is not None:
        g = Github(github_token)
    else:
        g = Github()

    return g


def get_github_license(g, github_repo, platform, license_scanner_bin):
    license_name = ''
    tmp_license_txt_file_name = 'tmp_license.txt'

    try:
        repository = g.get_repo(github_repo)
    except Exception:
        logger.info("It cannot find the license name. Please use '-t' option with github token.")
        logger.info("{0}{1}".format("refer:https://docs.github.com/en/github/authenticating-to-github/",
                    "keeping-your-account-and-data-secure/creating-a-personal-access-token"))
        repository = ''

    if repository != '':
        try:
            license_name = repository.get_license().license.spdx_id
            if license_name == "" or license_name == "NOASSERTION":
                try:
                    license_txt_data = base64.b64decode(repository.get_license().content).decode('utf-8')
                    tmp_license_txt = open(tmp_license_txt_file_name, 'w', encoding='utf-8')
                    tmp_license_txt.write(license_txt_data)
                    tmp_license_txt.close()
                    license_name = check_and_run_license_scanner(platform, license_scanner_bin, tmp_license_txt_file_name)
                except Exception:
                    logger.info("Cannot find the license name with license scanner binary.")

                if os.path.isfile(tmp_license_txt_file_name):
                    os.remove(tmp_license_txt_file_name)
        except Exception:
            logger.info("Cannot find the license name with github api.")

    return license_name


def check_license_scanner(platform):
    license_scanner_bin = ''

    if platform == const.LINUX:
        license_scanner = _license_scanner_linux
    elif platform == const.MACOS:
        license_scanner = _license_scanner_macos
    elif platform == const.WINDOWS:
        license_scanner = _license_scanner_windows
    else:
        logger.debug("Not supported OS to analyze license text with binary.")

    if license_scanner:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)

        data_path = os.path.join(base_path, license_scanner)
        license_scanner_bin = data_path

    return license_scanner_bin


def check_and_run_license_scanner(platform, license_scanner_bin, file_dir):
    license_name = ''

    if not license_scanner_bin:
        logger.error('Not supported OS for license scanner binary.')

    try:
        tmp_output_file_name = "tmp_license_scanner_output.txt"

        if file_dir == "UNKNOWN":
            license_name = ""
        else:
            if platform == const.LINUX:
                run_license_scanner = f"{license_scanner_bin} {file_dir} > {tmp_output_file_name}"
            elif platform == const.MACOS:
                run_license_scanner = f"{license_scanner_bin} identify {file_dir} > {tmp_output_file_name}"
            elif platform == const.WINDOWS:
                run_license_scanner = f"{license_scanner_bin} identify {file_dir} > {tmp_output_file_name}"
            else:
                run_license_scanner = ''

            if run_license_scanner is None:
                license_name = ""
                return license_name
            else:
                ret = subprocess.run(run_license_scanner, shell=True, stderr=subprocess.PIPE)
                if ret.returncode != 0 or ret.stderr:
                    os.remove(tmp_output_file_name)
                    return ""

            fp = open(tmp_output_file_name, "r", encoding='utf8')
            license_output = fp.read()
            fp.close()

            if platform == const.LINUX:
                license_output_re = re.findall(r'.*contains license\(s\)\s(.*)', license_output)
            else:
                license_output_re = re.findall(r"License:\s{1}(\S*)\s{1}", license_output)

            if len(license_output_re) == 1:
                license_name = license_output_re[0]
                if license_name == "No_license_found":
                    license_name = ""
            else:
                license_name = ""
            os.remove(tmp_output_file_name)

    except Exception as ex:
        logger.error(f"Failed to run license scan binary. {ex}")
        license_name = ""

    return license_name
