#!/bin/bash

set -e
set -x

git submodule update --init -f --recursive

. build_client.sh

echo building SNAPPY
pushd caladan/apps/storage_service
./snappy.sh
popd

echo building CALADAN
for dir in caladan caladan/shim caladan/bindings/cc caladan/apps/storage_service caladan/apps/netbench; do
	make -C $dir
done
