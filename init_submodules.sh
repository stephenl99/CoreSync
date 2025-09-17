#!/bin/sh

set -e

# Cloudlab patches to Shenango
echo Applying patch to Shenango
cd caladan
git apply ../connectx-4.patch
git apply ../cloudlab_xl170.patch
cd ..

echo Done.
