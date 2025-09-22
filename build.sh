#!/bin/sh

# Define source and destination paths
SRC="Source/Atmosphere/stratosphere/loader/source/oc"
DEST="build/stratosphere/loader/source/oc"

# Create destination directory if it doesn't exist
mkdir -p "$DEST"

# Copy contents of oc into destination oc (safe, includes hidden files)
cp -r "$SRC"/. "$DEST"/

# Enter build directory and compile using all available cores
cd build/stratosphere/loader || exit 1
rm out/nintendo_nx_arm64_armv8a/release/loader.kip
rm -rf build/
make -j"$(nproc)"
hactool -t kip1 out/nintendo_nx_arm64_armv8a/release/loader.kip --uncompress=hoc.kip
rm out/nintendo_nx_arm64_armv8a/release/loader.kip
rm -rf build/

