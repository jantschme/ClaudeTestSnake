#!/bin/bash
# Mammoth macOS App Build & Sign Script

set -e

echo "🎨 Generating Mammoth icon..."
python3 icon_gen.py

echo ""
echo "🏗️  Building Mammoth.app..."
rm -rf dist build
python3 -m PyInstaller Mammoth.spec

echo ""
echo "✍️  Code signing app..."
xattr -cr dist/Mammoth.app
codesign --force --deep -s - dist/Mammoth.app

echo ""
echo "✅ Done! App ready at dist/Mammoth.app"
echo ""
echo "💾 To copy to Desktop: cp -r dist/Mammoth.app ~/Desktop/"
echo "🚀 To launch: open ~/Desktop/Mammoth.app"
