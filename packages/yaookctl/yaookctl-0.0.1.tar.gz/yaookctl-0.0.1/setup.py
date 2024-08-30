#
# Copyright (c) 2021 The Yaook Authors.
#
# This file is part of Yaook.
# See https://yaook.cloud for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from setuptools import setup, find_packages

setup(
    name="yaookctl",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "click==8.1.7",
        "kubernetes-asyncio==30.3.1",
        "prettytable==3.11.0",
        "typing-extensions==4.12.2",
        "click-option-group==0.5.6",
    ],
    entry_points={
        "console_scripts": [
            "yaookctl=yaookctl.cli:main",
            "kubectl-yaook=yaookctl.cli:main",
        ]
    },
    include_package_data=True,
)
