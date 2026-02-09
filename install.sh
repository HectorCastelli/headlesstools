#!/bin/bash

# Load .env variables
if [ -f .env ]; then
	export "$(grep -v '^#' .env | xargs)"
fi

# 2. Crash if the variable is missing
: "${INSTANCE_PATH:?Error: INSTANCE_PATH is not defined. Ensure it is in your .env or environment.}"

PACK_NAME="hectorcastelliheadlesstools.zip"
WORLD_NAME="New World"

# Specific destinations
DATAPACK_DEST="$INSTANCE_PATH/saves/$WORLD_NAME/datapacks"
RESOURCE_DEST="$INSTANCE_PATH/resourcepacks"
TEMP_ZIP=$(mktemp -u /tmp/minecraft_pack.XXXXXX.zip)

echo "📦 Zipping current directory into $PACK_NAME..."

# Zips the contents of the current folder, excluding the zip itself and the script
zip -rq "$TEMP_ZIP" . -x "install.sh" ".git/*" ".vscode/*"
if [ ! -f "$TEMP_ZIP" ]; then
	echo "❌ Error: Zip file was not created. Check your permissions."
	exit 1
fi

echo "🚚 Copying to Datapacks..."
cp "$TEMP_ZIP" "$DATAPACK_DEST/$PACK_NAME"

echo "🚚 Copying to Resourcepacks..."
cp "$TEMP_ZIP" "$RESOURCE_DEST/$PACK_NAME"

# Cleanup
rm "$TEMP_ZIP"

echo "✅ Done! Pack deployed to both folders."
