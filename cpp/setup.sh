#!/usr/bin/env bash
BUILD_DIR="build"
INSALL_DIR="build/output/"
# if [ ! -d ${BUILD_DIR} ]; then
#   mkdir ${BUILD_DIR}
# else
#   echo "${BUILD_DIR} exists"
# fi

cmake \
  -B "${BUILD_DIR}" \
  -DCMAKE_INSTALL_PREFIX="${INSALL_DIR}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_TABLE_REPORT=ON  \
  .

pushd $BUILD_DIR
make -j2 && make install
popd