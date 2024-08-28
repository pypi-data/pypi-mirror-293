#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2022 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0

import logging
import re
import os
from defusedxml.ElementTree import parse, fromstring
import json
import requests
import fosslight_util.constant as constant
import fosslight_dependency.constant as const
from fosslight_dependency._package_manager import PackageManager
from fosslight_dependency._package_manager import check_and_run_license_scanner, get_url_to_purl

logger = logging.getLogger(constant.LOGGER_NAME)


class Nuget(PackageManager):
    package_manager_name = const.NUGET

    dn_url = "https://nuget.org/packages/"
    packageReference = False
    nuget_api_url = 'https://api.nuget.org/v3-flatcontainer/'
    dotnet_ver = []

    def __init__(self, input_dir, output_dir):
        super().__init__(self.package_manager_name, self.dn_url, input_dir, output_dir)

        for manifest_i in const.SUPPORT_PACKAE.get(self.package_manager_name):
            if os.path.isfile(manifest_i):
                self.append_input_package_list_file(manifest_i)
                if manifest_i != 'packages.config':
                    self.packageReference = True

    def parse_oss_information(self, f_name):
        tmp_license_txt_file_name = 'tmp_license.txt'
        with open(f_name, 'r', encoding='utf8') as input_fp:
            sheet_list = []
            package_list = []
            if self.packageReference:
                package_list = self.get_package_info_in_packagereference(input_fp)
            else:
                package_list = self.get_package_list_in_packages_config(input_fp)

        for oss_origin_name, oss_version in package_list:
            try:
                oss_name = f'{self.package_manager_name}:{oss_origin_name}'

                comment_list = []
                dn_loc = ''
                homepage = ''
                license_name = ''

                response = requests.get(f'{self.nuget_api_url}{oss_origin_name}/{oss_version}/{oss_origin_name}.nuspec')
                if response.status_code == 200:
                    root = fromstring(response.text)
                    xmlns = ''
                    m = re.search('{.*}', root.tag)
                    if m:
                        xmlns = m.group(0)
                    nupkg_metadata = root.find(f'{xmlns}metadata')

                    license_name_id = nupkg_metadata.find(f'{xmlns}license')
                    if license_name_id is not None:
                        license_name, license_comment = self.check_multi_license(license_name_id.text)
                        if license_comment != '':
                            comment_list.append(license_comment)
                    else:
                        license_url = nupkg_metadata.find(f'{xmlns}licenseUrl')
                        if license_url is not None:
                            url_res = requests.get(license_url.text)
                            if url_res.status_code == 200:
                                tmp_license_txt = open(tmp_license_txt_file_name, 'w', encoding='utf-8')
                                tmp_license_txt.write(url_res.text)
                                tmp_license_txt.close()
                                license_name_with_license_scanner = check_and_run_license_scanner(self.platform,
                                                                                                  self.license_scanner_bin,
                                                                                                  tmp_license_txt_file_name)
                                if license_name_with_license_scanner != "":
                                    license_name = license_name_with_license_scanner
                                else:
                                    license_name = license_url.text
                    repo_id = nupkg_metadata.find(f'{xmlns}repository')
                    if repo_id is not None:
                        dn_loc = repo_id.get("url")
                    else:
                        proj_url_id = nupkg_metadata.find(f'{xmlns}projectUrl')
                        if proj_url_id is not None:
                            dn_loc = proj_url_id.text
                    homepage = f'{self.dn_url}{oss_origin_name}'
                    if dn_loc == '':
                        dn_loc = f'{homepage}/{oss_version}'
                    else:
                        if dn_loc.endswith('.git'):
                            dn_loc = dn_loc[:-4]
                    purl = get_url_to_purl(f'{homepage}/{oss_version}', self.package_manager_name)
                else:
                    comment_list.append('Fail to response for nuget api')
                    purl = f'pkg:nuget/{oss_origin_name}@{oss_version}'
                self.purl_dict[f'{oss_origin_name}({oss_version})'] = purl

                deps_list = []
                if self.direct_dep and self.packageReference:
                    if oss_origin_name in self.direct_dep_list:
                        comment_list.append('direct')
                    else:
                        comment_list.append('transitive')

                    if f'{oss_origin_name}({oss_version})' in self.relation_tree:
                        deps_list.extend(self.relation_tree[f'{oss_origin_name}({oss_version})'])

                comment = ','.join(comment_list)
                sheet_list.append([purl, oss_name, oss_version, license_name, dn_loc, homepage, '', '', comment, deps_list])

            except Exception as e:
                logger.warning(f"Failed to parse oss information: {e}")
        sheet_list = self.change_dep_to_purl(sheet_list)
        if os.path.isfile(tmp_license_txt_file_name):
            os.remove(tmp_license_txt_file_name)

        return sheet_list

    def get_package_list_in_packages_config(self, input_fp):
        package_list = []
        root = parse(input_fp).getroot()
        for p in root.findall("package"):
            package_list.append([p.get("id"), p.get("version")])
        return package_list

    def get_package_info_in_packagereference(self, input_fp):
        json_f = json.load(input_fp)

        self.get_dotnet_ver_list(json_f)
        package_list = self.get_package_list_in_packages_assets(json_f)
        self.get_dependency_tree(json_f)
        self.get_direct_package_in_packagereference()

        return package_list

    def get_package_list_in_packages_assets(self, json_f):
        package_list = []
        for item in json_f['libraries']:
            if json_f['libraries'][item]['type'] == 'package':
                oss_info = item.split('/')
                package_list.append([oss_info[0], oss_info[1]])
        return package_list

    def get_dotnet_ver_list(self, json_f):
        json_project_group = json_f['projectFileDependencyGroups']
        for dotnet_ver in json_project_group:
            self.dotnet_ver.append(dotnet_ver)

    def get_dependency_tree(self, json_f):
        json_target = json_f['targets']
        for item in json_target:
            if item not in self.dotnet_ver:
                continue
            json_item = json_target[item]
            for pkg in json_item:
                json_pkg = json_item[pkg]
                if 'type' not in json_pkg:
                    continue
                if 'dependencies' not in json_pkg:
                    continue
                if json_pkg['type'] != 'package':
                    continue
                oss_info = pkg.split('/')
                self.relation_tree[f'{oss_info[0]}({oss_info[1]})'] = []
                for dep in json_pkg['dependencies']:
                    oss_name = dep
                    oss_ver = json_pkg['dependencies'][dep]
                    self.relation_tree[f'{oss_info[0]}({oss_info[1]})'].append(f'{oss_name}({oss_ver})')

    def get_direct_package_in_packagereference(self):
        for f in os.listdir(self.input_dir):
            if os.path.isfile(f) and ((f.split('.')[-1] == 'csproj') or (f.split('.')[-1] == 'xproj')):
                with open(f, 'r', encoding='utf8') as input_fp:
                    root = parse(input_fp).getroot()
                itemgroups = root.findall('ItemGroup')
                for itemgroup in itemgroups:
                    for item in itemgroup.findall('PackageReference'):
                        self.direct_dep_list.append(item.get('Include'))

    def check_multi_license(self, license_name):
        multi_license = license_name
        license_comment = ''
        try:
            if license_name.startswith('(') and license_name.endswith(')'):
                license_name = license_name.lstrip('(').rstrip(')')
                license_comment = license_name
                multi_license = ','.join(re.split(r'OR|AND', license_name))
        except Exception as e:
            logger.warning(f'Fail to parse multi license in npm: {e}')

        return multi_license, license_comment
