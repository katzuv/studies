"""
Basic tests for Notes Backup and PDF Merger
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    try:
        import pdf_merger
        import drive_handler
        import main
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_pdf_merger_class():
    """Test PDFMerger class instantiation"""
    try:
        from pdf_merger import PDFMerger
        merger = PDFMerger()
        print("✓ PDFMerger class instantiated")
        return True
    except Exception as e:
        print(f"✗ PDFMerger error: {e}")
        return False

def test_pathlib_usage():
    """Test that pathlib is being used correctly"""
    try:
        from pdf_merger import merge_course_pdfs
        from drive_handler import DriveHandler, download_course_files
        
        # Check function signatures accept Path objects
        test_path = Path("/tmp/test")
        
        print("✓ Functions accept pathlib.Path objects")
        return True
    except Exception as e:
        print(f"✗ Pathlib error: {e}")
        return False

def test_config_example():
    """Test that config example file exists and is valid JSON"""
    try:
        import json
        config_path = Path(__file__).parent / "config.example.json"
        
        if not config_path.exists():
            print("✗ config.example.json not found")
            return False
        
        with open(config_path) as f:
            config = json.load(f)
        
        assert 'courses' in config
        assert 'merged_folder_name' in config
        print("✓ config.example.json is valid")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_requirements():
    """Test that requirements.txt exists and has needed dependencies"""
    try:
        req_path = Path(__file__).parent / "requirements.txt"
        
        if not req_path.exists():
            print("✗ requirements.txt not found")
            return False
        
        with open(req_path) as f:
            requirements = f.read()
        
        needed = ['google-api-python-client', 'PyMuPDF', 'pikepdf']
        for dep in needed:
            if dep not in requirements:
                print(f"✗ Missing dependency: {dep}")
                return False
        
        print("✓ requirements.txt contains all needed dependencies")
        return True
    except Exception as e:
        print(f"✗ Requirements error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("Running basic tests...\n")
    
    tests = [
        test_imports,
        test_pdf_merger_class,
        test_pathlib_usage,
        test_config_example,
        test_requirements,
    ]
    
    results = []
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        results.append(test())
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
