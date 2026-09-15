#!/bin/bash
# QUICK FIX - Run this script to fix the HuggingFace error

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                          🔧 FIXING HUGGINGFACE ERROR                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

The system has been updated to use LOCAL models instead of HuggingFace.
No more external dependencies needed!

📋 WHAT WAS FIXED:
═══════════════════════════════════════════════════════════════════════════════

✓ Removed HuggingFace model loading
✓ Added offline environment mode
✓ Improved error handling
✓ Added graceful fallbacks
✓ Created error recovery script

🚀 HOW TO FIX (3 STEPS):
═══════════════════════════════════════════════════════════════════════════════

Step 1: Navigate to project
  $ cd ~/Downloads/DeepFake\ Detection

Step 2: Run error recovery (optional)
  $ python error_recovery.py

Step 3: Start the application
  $ python main.py

Then open: http://localhost:7860

═══════════════════════════════════════════════════════════════════════════════

✨ WHAT YOU GET:
  ✅ Local face detection (no internet)
  ✅ Local deepfake detection (no internet)
  ✅ Web UI (Gradio)
  ✅ Python API
  ✅ Full error handling

═══════════════════════════════════════════════════════════════════════════════

📚 DOCUMENTATION:
  - FIX_HUGGINGFACE_ERROR.md    (This issue explained)
  - error_recovery.py            (Recovery script)
  - main.py                      (Updated entry point)

═══════════════════════════════════════════════════════════════════════════════

🎬 READY TO GO!

Start with:
  $ python main.py

Open in browser:
  http://localhost:7860

═══════════════════════════════════════════════════════════════════════════════

EOF

echo ""
echo "Starting recovery process..."
echo ""

# Navigate to project
cd "$(dirname "$0")" || exit

# Try to run error recovery
if command -v python3 &> /dev/null; then
    python3 error_recovery.py
elif command -v python &> /dev/null; then
    python error_recovery.py
else
    echo "ERROR: Python not found"
    exit 1
fi

echo ""
echo "✓ Ready to run: python main.py"
