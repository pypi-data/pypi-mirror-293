#!/bin/bash

# ##################################################################
#
# Make udocker tarball for release
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ##################################################################

cd ..
VER=`grep "__version__" udocker/__init__.py|cut -d'"' -f 2`
echo "==========================================================="
echo "* This script produces udocker-${VER}.tar.gz, for release *"
echo "=========================================================="

rm -rf `find . -name '*pycache*'` `find . -name '*.pyc'`
mkdir -p udocker-${VER}
cp -prv udocker udocker-${VER}/
cd udocker-${VER}/udocker/
ln -s maincmd.py udocker
cd ../../

tar zcvf udocker-${VER}.tar.gz udocker-${VER}

rm -rf udocker-${VER}
