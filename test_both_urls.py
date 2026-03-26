#!/usr/bin/env python3
"""Test XSSensei with both lab URLs after improvements."""

import subprocess
import sys

test_urls = [
    ("Lab 1 (should work)", "https://0ad100780328d3268847c02e00bd00d2.web-security-academy.net/?search=test"),
    ("Lab 2 (now with fallback)", "https://0a340034041b7ff7814d1bf100020041.web-security-academy.net/?search=test"),
]

for label, url in test_urls:
    print(f"\n{'='*70}")
    print(f"TESTING: {label}")
    print(f"URL: {url}")
    print('='*70)
    
    cmd = [
        sys.executable, "main.py",
        "-u", url,
        "--timeout", "60"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        
        # Check for key results
        if "Vulnerabilities Found:" in output:
            # Extract vulnerability count
            for line in output.split('\n'):
                if "Vulnerabilities Found:" in line:
                    print(f"✓ {line.strip()}")
        
        if "parameters are reflected" in output or "parameters will be tested" in output:
            for line in output.split('\n'):
                if "parameters" in line.lower() and ("reflected" in line.lower() or "tested" in line.lower()):
                    print(f"✓ {line.strip()}")
        
        if "Context analysis complete" in output:
            for line in output.split('\n'):
                if "Context analysis complete" in line:
                    print(f"✓ {line.strip()}")
        
        if "VERIFIED" in output:
            print("✓ XSS vulnerabilities VERIFIED!")
            
        # Show mission report
        for line in output.split('\n'):
            if any(x in line for x in ["MISSION REPORT", "URLs Scanned", "Payloads Sent", "Scan Duration"]):
                print(f"  {line.strip()}")
                
    except subprocess.TimeoutExpired:
        print("⚠️  Scan timed out (>120s)")
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'='*70}")
print("Test complete!")
