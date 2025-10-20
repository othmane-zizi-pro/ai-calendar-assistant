#!/usr/bin/env python3
"""Verify Calendar Assistant setup."""

import sys
from pathlib import Path

def check_ollama():
    """Check if Ollama is running and has the model."""
    try:
        import subprocess
        result = subprocess.run(
            ['curl', '-s', 'http://localhost:11434/api/tags'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and 'llama3.2:3b' in result.stdout:
            print("✅ Ollama is running with llama3.2:3b model")
            return True
        else:
            print("❌ Ollama is running but model not found")
            print("   Run: ollama pull llama3.2:3b")
            return False
    except Exception as e:
        print(f"❌ Ollama is not running")
        print("   Run: ollama serve")
        return False


def check_python_packages():
    """Check if required packages are installed."""
    packages = [
        'mcp',
        'google.auth',
        'google_auth_oauthlib',
        'googleapiclient',
        'ollama',
        'langchain',
        'click',
        'rich'
    ]

    all_good = True
    for package in packages:
        try:
            __import__(package.replace('.', '_') if '.' in package else package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            all_good = False

    return all_good


def check_credentials():
    """Check if credentials.json exists."""
    creds_file = Path('credentials.json')
    if creds_file.exists():
        print("✅ credentials.json found")
        return True
    else:
        print("❌ credentials.json not found")
        print("   Download from Google Cloud Console")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("Calendar Assistant Setup Verification")
    print("=" * 60)
    print()

    print("Checking Ollama...")
    ollama_ok = check_ollama()
    print()

    print("Checking Python packages...")
    packages_ok = check_python_packages()
    print()

    print("Checking Google Calendar credentials...")
    creds_ok = check_credentials()
    print()

    print("=" * 60)
    if ollama_ok and packages_ok:
        if creds_ok:
            print("✅ Everything is ready!")
            print()
            print("Test it:")
            print("  python calendar_assistant.py today")
        else:
            print("⚠️  Almost there!")
            print()
            print("Next step: Get Google Calendar credentials")
            print("See: SETUP_INSTRUCTIONS.md")
    else:
        print("❌ Some issues need fixing")
        print()
        if not ollama_ok:
            print("Fix Ollama:")
            print("  ollama serve")
            print("  ollama pull llama3.2:3b")
        if not packages_ok:
            print("Fix packages:")
            print("  pip install -r requirements-calendar.txt")

    print("=" * 60)


if __name__ == '__main__':
    main()
