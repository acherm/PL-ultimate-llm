#!/bin/zsh
#
# A simple script to get the weather from wttr.in
#
# Usage: weather [location] [options]
#
# Options:
#   -f: force update (don't use cached data)
#   -h: show help
#
# Example:
#   weather Munich
#   weather "New York"
#   weather London -f

zmodload zsh/datetime

CACHE_DIR=${XDG_CACHE_HOME:-$HOME/.cache}/weather
CACHE_FILE=$CACHE_DIR/$(echo "$*" | tr ' /' '_-').txt
CACHE_TIME=3600 # 1 hour

# Create cache dir if it doesn't exist
[ -d $CACHE_DIR ] || mkdir -p $CACHE_DIR

# Check for force update or expired cache
if ! [[ "$*" =~ "-f" ]] && [ -f $CACHE_FILE ] && (( $EPOCHSECONDS - $(stat -f %m $CACHE_FILE) < $CACHE_TIME )); then
    cat $CACHE_FILE
    exit 0
fi

# Remove -f from arguments
args=(${(s: :)@})
args=(${args:#-f})

# Show help
if [[ "$*" =~ "-h" ]]; then
    echo "Usage: weather [location] [options]"
    echo "Options:"
    echo "  -f: force update (don't use cached data)"
    echo "  -h: show help"
    exit 0
fi

# Get weather and save to cache
curl -s "wttr.in/$args" | tee $CACHE_FILE