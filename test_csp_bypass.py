#!/usr/bin/env python3
"""
XSSensei Improved PoC Test - With CSP Bypass Payloads
Tests if PoC links now execute alert() better in real browsers.
"""

import subprocess
import sys

print("""
╔══════════════════════════════════════════════════════════════════┗
║  XSSensei - Improved PoC Testing with CSP-Bypass Payloads        ║
║  New Features:                                                   ║
║  ✓ CSP_BYPASS payload category (23 variants)                    ║
║  ✓ PROOF payload category (multiple execution methods)          ║
║  ✓ Better DOM detection + timing methods                        ║
║  ✓ 20 payload variants tested (instead of 10)                   ║
╚══════════════════════════════════════════════════════════════════╝
""")

test_url = "https://0ad100780328d3268847c02e00bd00d2.web-security-academy.net/?search=test"

print(f"\n📍 Testing URL: {test_url}")
print(f"\n⏳ Starting scan (expect ~30-50 seconds)...")
print(f"{'='*70}\n")

try:
    result = subprocess.run(
        [sys.executable, "main.py", "-u", test_url, "--timeout", "60"],
        capture_output=False,
        text=True
    )
    
    print(f"\n{'='*70}")
    if result.returncode == 0:
        print("✅ Scan completed successfully")
    else:
        print(f"⚠️  Scan completed with return code: {result.returncode}")
        
except KeyboardInterrupt:
    print("\n❌ Scan interrupted by user")
except Exception as e:
    print(f"❌ Error: {e}")

print(f"""
{'='*70}
NEXT STEPS:
{'='*70}
1. Copy the PoC link from output above
2. Paste into your browser's address bar
3. Alert should now execute (or page behavior should change)
4. If alert doesn't appear:
   - Check browser console (F12) for errors
   - Check CSP headers: F12 → Network → click request → Headers
   - Try in different browser (Chrome vs Firefox vs Edge)

PoC Link Format:
https://target.com/?param=PAYLOAD_HERE (URL encoded)

Known CSP Issues:
- Some labs have strict CSP that blocks alert()
- Tool still finds vulns correctly (CTF solves, Playwright detects)
- But manual execution may be blocked
- DOM-based payloads work when alert() blocks
{'='*70}
""")
