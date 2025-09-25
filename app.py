#!/usr/bin/env python3
"""
Simple example application for perfpy-conda Docker container.
"""

import sys
import platform
import numpy as np
import pandas as pd

def main():
    """Main function to demonstrate the application is working."""
    print("=" * 50)
    print("🐍 perfpy-conda Docker Application")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    print("\n📦 Package versions:")
    print(f"  - NumPy: {np.__version__}")
    print(f"  - Pandas: {pd.__version__}")
    
    print("\n✅ Application is running successfully!")
    
    # Simple demonstration with NumPy and Pandas
    print("\n🧮 Quick demonstration:")
    arr = np.array([1, 2, 3, 4, 5])
    df = pd.DataFrame({'numbers': arr, 'squares': arr**2})
    print(f"Array: {arr}")
    print(f"DataFrame:\n{df}")

if __name__ == "__main__":
    main()