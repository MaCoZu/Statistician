#!/bin/bash
# Quick Start Script for Statistician Package Development

set -e  # Exit on error

echo "=========================================="
echo "Statistician - Quick Start Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python is not installed!"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check if Python version is >= 3.8
MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]; }; then
    echo "Error: Python 3.8 or higher is required!"
    echo "Current version: Python $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install package in editable mode with dev dependencies
echo "Installing package with development dependencies..."
pip install -e ".[dev]" --quiet
echo "✓ Package installed in editable mode"
echo ""

# Run tests
echo "Running tests..."
echo "=========================================="
pytest tests/ -v
TEST_EXIT_CODE=$?
echo "=========================================="
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed!"
    echo ""
    echo "Please fix the failing tests before publishing."
    exit 1
fi
echo ""

# Check code formatting
echo "Checking code formatting..."
black --check statistician/ tests/ 2>&1 | head -10
BLACK_EXIT_CODE=${PIPESTATUS[0]}

if [ $BLACK_EXIT_CODE -eq 0 ]; then
    echo "✓ Code formatting OK"
else
    echo "⚠ Code formatting issues found"
    echo "Run: black statistician/ tests/"
fi
echo ""

# Check import sorting
echo "Checking import sorting..."
isort --check-only statistician/ tests/ 2>&1 | head -10
ISORT_EXIT_CODE=${PIPESTATUS[0]}

if [ $ISORT_EXIT_CODE -eq 0 ]; then
    echo "✓ Import sorting OK"
else
    echo "⚠ Import sorting issues found"
    echo "Run: isort statistician/ tests/"
fi
echo ""

# Run linting
echo "Running flake8 linting..."
flake8 statistician/ tests/ --count --statistics
FLAKE8_EXIT_CODE=$?

if [ $FLAKE8_EXIT_CODE -eq 0 ]; then
    echo "✓ No linting issues"
else
    echo "⚠ Linting issues found"
fi
echo ""

# Display package info
echo "=========================================="
echo "Package Information"
echo "=========================================="
$PYTHON_CMD -c "import statistician; print(f'Package: statistician'); print(f'Version: {statistician.__version__}'); print(f'Location: {statistician.__file__}')"
echo ""

# Test basic functionality
echo "Testing basic functionality..."
$PYTHON_CMD -c "from statistician import mean, median; print(f'mean([1,2,3,4,5]) = {mean([1,2,3,4,5])}'); print(f'median([1,2,3,4,5]) = {median([1,2,3,4,5])}')"
echo "✓ Basic functions working"
echo ""

# Summary
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the example script:"
echo "   python example.py"
echo ""
echo "3. Make changes and test:"
echo "   pytest tests/"
echo ""
echo "4. Before committing, format your code:"
echo "   black statistician/ tests/"
echo "   isort statistician/ tests/"
echo ""
echo "5. When ready to publish, see PUBLISHING.md"
echo ""
echo "=========================================="