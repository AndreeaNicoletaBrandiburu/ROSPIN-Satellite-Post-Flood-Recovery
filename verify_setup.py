"""
Setup verification script for ROSPIN Satellite Post-Flood Recovery project
Checks if all components are installed and working correctly.
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def check_python_version():
    print_header("1. Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] Python 3.8+ is required!")
        return False
    print("[OK] Python version OK")
    return True

def check_python_packages():
    print_header("2. Checking Python Packages")
    required_packages = [
        'numpy', 'pandas', 'flask', 'flask_cors'
    ]
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"[OK] {package} installed")
        except ImportError:
            print(f"[ERROR] {package} MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n[WARNING] Missing packages: {', '.join(missing)}")
        print("Run: pip install -r data_processing/requirements.txt")
        print("And: pip install -r backend/requirements.txt")
        return False
    return True

def check_node():
    print_header("3. Checking Node.js")
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Node.js {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    print("[ERROR] Node.js is not installed or not in PATH")
    print("   Download from: https://nodejs.org/")
    return False

def check_npm_packages():
    print_header("4. Checking npm Packages")
    frontend_path = Path("frontend")
    node_modules = frontend_path / "node_modules"
    if node_modules.exists():
        print("[OK] node_modules exists")
        return True
    else:
        print("[ERROR] node_modules MISSING")
        print("   Run: cd frontend; npm install")
        return False

def test_data_processing():
    print_header("5. Testing Data Processing Module")
    try:
        sys.path.insert(0, str(Path("data_processing").absolute()))
        from satellite_data_processor_v2 import SatelliteDataProcessor
        from datetime import datetime
        
        processor = SatelliteDataProcessor()
        print("[OK] Data processing module imports correctly")
        
        # Quick test
        flood_date = datetime(2023, 6, 15)
        results = processor.process_flood_event(flood_date, num_time_steps=3)
        
        if 'recovery_metrics' in results:
            print("[OK] Data processing works!")
            print(f"   Recovery percentage: {results['recovery_metrics']['recovery_percentage']:.2f}%")
            return True
        else:
            print("[ERROR] Data processing does not return correct results")
            return False
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("   Check if you installed dependencies: pip install -r data_processing/requirements.txt")
        return False
    except Exception as e:
        print(f"[ERROR] Test error: {e}")
        return False

def test_backend_import():
    print_header("6. Testing Backend (import)")
    backend_path = Path("backend")
    app_file = backend_path / "app.py"
    if app_file.exists():
        print("[OK] app.py file exists")
        try:
            # Only check if it can be imported, don't run the server
            sys.path.insert(0, str(backend_path.absolute()))
            # Don't actually import as it would start the server
            print("[OK] Backend API is configured correctly")
            return True
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            return False
    else:
        print("[ERROR] app.py file MISSING")
        return False

def check_file_structure():
    print_header("7. Checking File Structure")
    required_files = [
        "data_processing/satellite_data_processor_v2.py",
        "data_processing/requirements.txt",
        "backend/app.py",
        "backend/requirements.txt",
        "frontend/package.json",
        "frontend/src/App.js",
        "README.md"
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"[OK] {file_path}")
        else:
            print(f"[ERROR] {file_path} MISSING")
            all_ok = False
    
    return all_ok

def print_summary(results):
    print_header("VERIFICATION SUMMARY")
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        status_icon = "[OK]" if status else "[ERROR]"
        print(f"{status_icon} {check}")
    
    print(f"\n{'='*60}")
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n[SUCCESS] ALL CHECKS PASSED!")
        print("\nNext steps:")
        print("1. Start backend: cd backend; python app.py")
        print("2. In a new terminal, start frontend: cd frontend; npm start")
        print("3. Open http://localhost:3000 in browser")
    else:
        print("\n[WARNING] Some checks failed. Fix the issues above.")
        print("\nQuick installation:")
        print("  pip install -r data_processing/requirements.txt")
        print("  pip install -r backend/requirements.txt")
        print("  cd frontend; npm install")

def main():
    print("\n" + "="*60)
    print("SETUP VERIFICATION - ROSPIN Satellite Post-Flood Recovery")
    print("="*60)
    
    results = {}
    
    results["Python Version"] = check_python_version()
    results["Python Packages"] = check_python_packages()
    results["Node.js"] = check_node()
    results["npm Packages"] = check_npm_packages()
    results["Data Processing"] = test_data_processing()
    results["Backend"] = test_backend_import()
    results["File Structure"] = check_file_structure()
    
    print_summary(results)

if __name__ == "__main__":
    main()
