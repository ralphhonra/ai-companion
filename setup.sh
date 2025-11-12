#!/bin/bash

# JARVIS Setup Script
# This script helps you set up JARVIS on your Mac

set -e

echo "=========================================="
echo "  J.A.R.V.I.S. Setup Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Error: This script is designed for macOS only.${NC}"
    exit 1
fi

echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.8 or higher.${NC}"
    echo "Download from: https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "Step 2: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
else
    echo -e "${YELLOW}⚠ Ollama not found. Installing...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama installed${NC}"
fi

echo ""
echo "Step 3: Downloading Ollama model (llama3.2:3b)..."
echo "This may take a few minutes..."
ollama pull llama3.2:3b
echo -e "${GREEN}✓ Model downloaded${NC}"

echo ""
echo "Step 4: Checking tkinter (required for GUI)..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${GREEN}✓ tkinter is available${NC}"
else
    echo -e "${YELLOW}⚠ tkinter not found, installing...${NC}"
    brew install python-tk@3.13
    echo -e "${GREEN}✓ tkinter installed${NC}"
fi

echo ""
echo "Step 5: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

echo ""
echo "Step 6: Installing Python dependencies in virtual environment..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo "Step 7: Checking Picovoice API key..."
if [ -z "$PICOVOICE_API_KEY" ]; then
    echo -e "${YELLOW}⚠ PICOVOICE_API_KEY not set${NC}"
    echo ""
    echo "To enable wake word detection, you need a free API key:"
    echo "1. Go to: https://console.picovoice.ai/"
    echo "2. Sign up for a free account"
    echo "3. Create an access key"
    echo "4. Run: export PICOVOICE_API_KEY='your-key-here'"
    echo "5. Add to ~/.zshrc to persist:"
    echo "   echo 'export PICOVOICE_API_KEY=\"your-key\"' >> ~/.zshrc"
    echo ""
    echo -e "${YELLOW}You can still test JARVIS without wake word detection.${NC}"
else
    echo -e "${GREEN}✓ PICOVOICE_API_KEY is set${NC}"
fi

echo ""
echo "Step 8: Checking microphone permissions..."
echo "Please grant microphone access to Terminal/Python when prompted."
./venv/bin/python -c "import sounddevice as sd; sd.query_devices()" > /dev/null 2>&1 || {
    echo -e "${YELLOW}⚠ Grant microphone access in:${NC}"
    echo "System Settings → Privacy & Security → Microphone"
}

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To run JARVIS:"
echo ""
if [ -z "$PICOVOICE_API_KEY" ]; then
    echo "  source venv/bin/activate    # Activate virtual environment"
    echo "  python jarvis.py --test     # Test mode (no wake word)"
else
    echo "  source venv/bin/activate    # Activate virtual environment"
    echo "  python jarvis.py            # Normal mode with wake word"
    echo "  python jarvis.py --test     # Test mode (no wake word)"
fi
echo ""
echo "For more information, see README.md"
echo ""

