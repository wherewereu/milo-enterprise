#!/bin/bash
# image-collector.sh — Collect images from iMessage attachments
# Usage: image-collector.sh [new|list|peek|collect-all]
#
# Stores collected images in ~/.openclaw/workspace/received-images/
# Maintains manifest.jsonl for history

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMSG_DIR="$HOME/Library/Messages/Attachments/imsg"
DEST_DIR="$HOME/.openclaw/workspace/received-images"
MANIFEST="$DEST_DIR/manifest.jsonl"
TIMESTAMP_FORMAT="%Y-%m-%d_%H%M"

# Supported image extensions
EXTENSIONS="jpg|jpeg|png|gif|heic|heif|webp|tiff|bmp"

# Ensure destination exists
mkdir -p "$DEST_DIR"

# Find most recent image in a directory
find_most_recent_image() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "" 
        return
    fi
    
    # Find files matching image extensions, sort by mtime descending, take first
    find "$dir" -type f \( \
        -iname "*.jpg" -o \
        -iname "*.jpeg" -o \
        -iname "*.png" -o \
        -iname "*.gif" -o \
        -iname "*.heic" -o \
        -iname "*.heif" -o \
        -iname "*.webp" -o \
        -iname "*.tiff" -o \
        -iname "*.bmp" \
    \) -mmin -525600 2>/dev/null | \
        xargs -I{} ls -t {} 2>/dev/null | \
        head -1
}

# Check if already collected (by original path stored in manifest)
already_collected() {
    local original="$1"
    if [[ ! -f "$MANIFEST" ]]; then
        return 1
    fi
    grep -q "\"original_name\":\"$original\"" "$MANIFEST" 2>/dev/null
}

# Format file size (macOS compatible)
format_size() {
    local size="$1"
    if [[ $size -ge 1048576 ]]; then
        local mb=$(echo "$size 1048576" | awk '{printf "%.1f", $1/$2}')
        echo "${mb} MB"
    elif [[ $size -ge 1024 ]]; then
        local kb=$(echo "$size 1024" | awk '{printf "%.0f", $1/$2}')
        echo "${kb} KB"
    else
        echo "${size} B"
    fi
}

# Copy image to received-images with timestamp prefix
collect_image() {
    local src="$1"
    local source="${2:-imessage}"
    
    if [[ ! -f "$src" ]]; then
        echo "ERROR: File not found: $src" >&2
        return 1
    fi
    
    local filename=$(basename "$src")
    local ext="${filename##*.}"
    ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    local timestamp=$(date +"$TIMESTAMP_FORMAT")
    local newname="${timestamp}_${filename}"
    local dest="$DEST_DIR/$newname"
    
    # Handle duplicates
    if [[ -f "$dest" ]]; then
        local counter=1
        while [[ -f "${dest%.*}_${counter}.${ext}" ]]; do
            ((counter++))
        done
        newname="${timestamp}_${filename%.*}_${counter}.${ext}"
        dest="$DEST_DIR/$newname"
    fi
    
    # Copy the file
    cp "$src" "$dest"
    
    # Record in manifest
    local size=$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest" 2>/dev/null || echo 0)
    local collected_at=$(date -u +"%Y-%m-%dT%H:%M:%S%z")
    local json_entry=$(cat <<JSON
{"collected_at":"$collected_at","source":"$source","original_name":"$filename","stored_name":"$newname","size_bytes":$size,"path":"$dest"}
JSON
)
    echo "$json_entry" >> "$MANIFEST"
    
    echo "$dest"
}

# List all collected images
do_list() {
    if [[ ! -f "$MANIFEST" ]] || [[ ! -s "$MANIFEST" ]]; then
        echo "No images collected yet."
        return
    fi
    
    echo "Received images (sorted newest first):"
    echo ""
    
    local count=0
    local lines=()
    while IFS= read -r line; do
        lines+=("$line")
    done < "$MANIFEST"
    
    local total=${#lines[@]}
    for ((i=total-1; i>=0; i--)); do
        ((count++))
        local line="${lines[$i]}"
        local collected_at=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['collected_at'][:19].replace('T',' '))" 2>/dev/null || echo "?")
        local stored=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['stored_name'])" 2>/dev/null || echo "?")
        local source=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['source'])" 2>/dev/null || echo "?")
        local size=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin)['size_bytes'])" 2>/dev/null || echo "0")
        local formatted_size=$(format_size "$size")
        printf "  %d. %s | %s | %s | %s\n" "$count" "$collected_at" "$stored" "$source" "$formatted_size"
    done
}

# Peek at most recent without copying
do_peek() {
    local recent=$(find_most_recent_image "$IMSG_DIR")
    
    if [[ -z "$recent" ]]; then
        echo "No images found in iMessage attachments."
        return
    fi
    
    local filename=$(basename "$recent")
    local size=$(stat -f%z "$recent" 2>/dev/null || stat -c%s "$recent" 2>/dev/null || echo 0)
    local mtime=$(ls -lT "$recent" 2>/dev/null | awk '{print $6, $7, $8}' || echo "unknown")
    local formatted_size=$(format_size "$size")
    
    echo "Most recent iMessage image:"
    echo "  File: $filename"
    echo "  Modified: $mtime"
    echo "  Size: $formatted_size"
    echo "  Path: $recent"
}

# New image — collect and report
do_new() {
    local recent=$(find_most_recent_image "$IMSG_DIR")
    
    if [[ -z "$recent" ]]; then
        echo "No images found in iMessage attachments."
        return
    fi
    
    local filename=$(basename "$recent")
    
    if already_collected "$filename"; then
        echo "Most recent image already collected: $filename"
        local stored=$(grep "$filename" "$MANIFEST" | tail -1 | python3 -c "import sys,json; print(json.load(sys.stdin)['stored_name'])" 2>/dev/null || echo "$filename")
        local stored_path="$DEST_DIR/$stored"
        if [[ -f "$stored_path" ]]; then
            echo "  Path: $stored_path"
        fi
        return
    fi
    
    local dest=$(collect_image "$recent" "imessage")
    local size=$(stat -f%z "$dest" 2>/dev/null || stat -c%s "$dest" 2>/dev/null || echo 0)
    local formatted_size=$(format_size "$size")
    
    echo "New image saved:"
    echo "  Path: $dest"
    echo "  Source: iMessage"
    echo "  Original: $filename"
    echo "  Size: $formatted_size"
}

# Collect all uncollected images
do_collect_all() {
    if [[ ! -d "$IMSG_DIR" ]]; then
        echo "ERROR: iMessage attachments directory not found: $IMSG_DIR" >&2
        echo "Make sure Full Disk Access is granted in System Preferences." >&2
        exit 1
    fi
    
    local count=0
    while IFS= read -r img; do
        local filename=$(basename "$img")
        if ! already_collected "$filename"; then
            local dest=$(collect_image "$img" "imessage")
            echo "Collected: $filename -> $(basename "$dest")"
            ((count++))
        fi
    done < <(find "$IMSG_DIR" -type f \( \
        -iname "*.jpg" -o \
        -iname "*.jpeg" -o \
        -iname "*.png" -o \
        -iname "*.gif" -o \
        -iname "*.heic" -o \
        -iname "*.heif" -o \
        -iname "*.webp" -o \
        -iname "*.tiff" -o \
        -iname "*.bmp" \
    \) -mmin -525600 2>/dev/null | xargs -I{} ls -t {} 2>/dev/null)
    
    if [[ $count -eq 0 ]]; then
        echo "No new images to collect."
    else
        echo "Collected $count image(s)."
    fi
}

# Main
case "${1:-new}" in
    new)
        do_new
        ;;
    list)
        do_list
        ;;
    peek)
        do_peek
        ;;
    collect-all)
        do_collect_all
        ;;
    help|--help|-h)
        echo "Usage: image-collector.sh [new|list|peek|collect-all]"
        echo ""
        echo "  new        — Find most recent iMessage image, copy to received-images/"
        echo "  list       — List all collected images with timestamps"
        echo "  peek       — Show most recent without copying"
        echo "  collect-all— Copy all uncollected images from iMessage"
        ;;
    *)
        echo "Unknown command: $1" >&2
        echo "Usage: image-collector.sh [new|list|peek|collect-all]" >&2
        exit 1
        ;;
esac
