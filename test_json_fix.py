#!/usr/bin/env python3
"""
Test script to verify JSON extraction improvements
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

from turn import extract_json_str, _fix_common_json_issues

def test_json_extraction():
    """Test various JSON extraction scenarios"""
    
    # Test case 1: Normal JSON
    test1 = '{"language": {"name": "Python", "aliases": ["py"]}, "program": {"title": "Hello World"}}'
    try:
        result1 = extract_json_str(test1)
        print("✓ Test 1 (normal JSON): PASSED")
        print(f"  Extracted: {result1[:50]}...")
    except Exception as e:
        print(f"✗ Test 1 (normal JSON): FAILED - {e}")
    
    # Test case 2: Fenced JSON
    test2 = '''Here's the JSON:
```json
{
  "language": {
    "name": "Rust",
    "aliases": ["rs"]
  },
  "program": {
    "title": "Hello World"
  }
}
```'''
    try:
        result2 = extract_json_str(test2)
        print("✓ Test 2 (fenced JSON): PASSED")
        print(f"  Extracted: {result2[:50]}...")
    except Exception as e:
        print(f"✗ Test 2 (fenced JSON): FAILED - {e}")
    
    # Test case 3: Unterminated string (the original issue)
    test3 = '''{
  "language": {
    "name": "Pascal",
    "aliases": ["pas"]
  },
  "program": {
    "title": "Hello World",
    "code": "program HelloWorld;
begin
  writeln('Hello, World!');
end."
  }
}'''
    try:
        result3 = extract_json_str(test3)
        print("✓ Test 3 (unterminated string): PASSED")
        print(f"  Extracted: {result3[:50]}...")
    except Exception as e:
        print(f"✗ Test 3 (unterminated string): FAILED - {e}")
    
    # Test case 4: Malformed JSON with unescaped quotes
    test4 = '''{
  "language": {
    "name": "JavaScript",
    "aliases": ["js"]
  },
  "program": {
    "title": "Hello "World"",
    "code": "console.log("Hello, World!");"
  }
}'''
    try:
        result4 = extract_json_str(test4)
        print("✓ Test 4 (unescaped quotes): PASSED")
        print(f"  Extracted: {result4[:50]}...")
    except Exception as e:
        print(f"✗ Test 4 (unescaped quotes): FAILED - {e}")

if __name__ == "__main__":
    print("Testing JSON extraction improvements...")
    test_json_extraction()
    print("Done!")
