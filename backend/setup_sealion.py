#!/usr/bin/env python3
"""
SEA-Lion API Setup Script for MediTalks
Helps users configure their SEA-Lion API key
"""

import os
import sys
from pathlib import Path

def setup_sealion_api():
    """Setup SEA-Lion API key in environment file"""
    
    print("🦁 MediTalks SEA-Lion API Setup")
    print("=" * 40)
    print()
    
    # Find the .env file
    backend_dir = Path(__file__).parent
    env_file = backend_dir / '.env'
    
    if not env_file.exists():
        print("❌ .env file not found in backend directory")
        return False
    
    print("ℹ️  SEA-Lion API Information:")
    print("- SEA-Lion is developed by AI Singapore")
    print("- It's optimized for Southeast Asian languages and cultures")
    print("- Visit: https://www.aisingapore.org/sea-lion/")
    print()
    
    # Check current status
    with open(env_file, 'r') as f:
        content = f.read()
    
    if 'your_sealion_api_key_here' in content:
        print("🔧 Current status: SEA-Lion API key not configured")
        print("📋 The system is currently using Gemini AI as fallback")
    else:
        print("✅ SEA-Lion API key appears to be configured")
    
    print()
    choice = input("Do you want to configure/update SEA-Lion API key? (y/n): ").lower().strip()
    
    if choice != 'y':
        print("👋 Setup cancelled. System will continue using Gemini AI.")
        return True
    
    print()
    print("🔑 SEA-Lion API Key Setup:")
    print("1. Visit AI Singapore's SEA-Lion website")
    print("2. Request API access through official channels")
    print("3. Get your API key from their platform")
    print()
    
    api_key = input("Enter your SEA-Lion API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️  Skipped API key configuration")
        return True
    
    # Update the .env file
    try:
        updated_content = content.replace(
            'SEALION_API_KEY="your_sealion_api_key_here"',
            f'SEALION_API_KEY="{api_key}"'
        )
        
        with open(env_file, 'w') as f:
            f.write(updated_content)
        
        print("✅ SEA-Lion API key configured successfully!")
        print("🔄 Please restart the backend server to apply changes")
        print()
        print("📊 To test the configuration:")
        print("1. Restart the backend: python app.py")
        print("2. Use 'Test Backend Connection' button in frontend")
        print("3. Check that 'Primary AI: SEA-Lion' appears")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        return True
    except ImportError:
        print("❌ Missing required dependency: requests")
        print("📦 Install with: pip install requests")
        return False

def main():
    """Main setup function"""
    if not check_dependencies():
        sys.exit(1)
    
    success = setup_sealion_api()
    
    if success:
        print()
        print("🎉 Setup completed!")
        print("📖 For more information, see README_SEALION.md")
    else:
        print("❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
