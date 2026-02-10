#!/bin/bash

TARGET_SCRIPT="$(git rev-parse --show-toplevel)/scripts/install.sh"
INTERVAL=2 # How many seconds to wait between checks

# Get the initial state of the directory
# This looks at the most recent modification time across all files
get_last_mod() {
	find . -not -path '*/.*' -printf '%T@\n' | sort -n | tail -1 | sha1sum
}

LAST_MOD="" # Immediately install

echo "🕒 Polling for changes every $INTERVAL seconds..."

while true; do
	CURRENT_MOD=$(get_last_mod)

	if [[ "$CURRENT_MOD" != "$LAST_MOD" ]]; then
		clear # Clear screen for better visualization
		echo "⚡ Change detected! Running $TARGET_SCRIPT..."
		# Run and clear output on success
		$TARGET_SCRIPT && clear || echo "❌ Failure!"
		LAST_MOD=$(get_last_mod)
		echo "✅ Done. Waiting for next change..."
	fi
	sleep "$INTERVAL"
done
