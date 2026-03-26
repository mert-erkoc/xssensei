#!/usr/bin/env python3
"""Debug test for URL parsing and reflection detection."""

import asyncio
from urllib.parse import urlparse, parse_qs
import httpx
import ssl

# Test URL parsing
url = "https://0a340034041b7ff7814d1bf100020041.web-security-academy.net/?search=test"
parsed = urlparse(url)
params = parse_qs(parsed.query)

print("=" * 70)
print("URL PARSING TEST")
print("=" * 70)
print(f"URL: {url}")
print(f"Query string: '{parsed.query}'")
print(f"Parsed params: {params}")
print(f"Param names: {list(params.keys())}")
print(f"Num params: {len(params)}")

# Test with reflection marker
test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?search=XSS_TEST_MARKER_12345"
print("\n" + "=" * 70)
print("REFLECTION TEST")
print("=" * 70)
print(f"Test URL: {test_url}")

async def test_reflection():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    async with httpx.AsyncClient(verify=False, timeout=15) as client:
        try:
            print("Sending request...")
            response = await client.get(test_url)
            print(f"Status: {response.status_code}")
            print(f"Response length: {len(response.text)}")
            
            if "XSS_TEST_MARKER_12345" in response.text:
                print("✅ Reflection FOUND in response!")
                idx = response.text.find("XSS_TEST_MARKER_12345")
                ctx_start = max(0, idx - 100)
                ctx_end = min(len(response.text), idx + 150)
                print(f"Context: {response.text[ctx_start:ctx_end]}")
            else:
                print("❌ Reflection NOT found in response")
                print("\nFirst 800 chars of response:")
                print(response.text[:800])
        except Exception as e:
            print(f"Error: {e}")

# Run async test
print("\nCalling async test...")
try:
    asyncio.run(test_reflection())
except KeyboardInterrupt:
    print("\nTest interrupted")
except Exception as e:
    print(f"Error running test: {e}")
