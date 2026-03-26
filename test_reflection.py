#!/usr/bin/env python
"""Test reflection detection on both lab URLs."""

import httpx
import asyncio
import sys

async def test_urls():
    """Test both URLs for reflection behavior."""
    
    async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
        # Test first URL (working)
        url1 = 'https://0ad100780328d3268847c02e00bd00d2.web-security-academy.net/?search=testprobe123'
        print('='*80)
        print('[TEST 1] First URL (reported as working):')
        print(f'URL: {url1}')
        print('='*80)
        try:
            r1 = await client.get(url1)
            print(f'Status: {r1.status_code}')
            print(f'Response length: {len(r1.text)} bytes')
            
            if 'testprobe123' in r1.text:
                print('✓ testprobe123 is reflected')
                # Find and show context
                idx = r1.text.find('testprobe123')
                start = max(0, idx - 50)
                end = min(len(r1.text), idx + 120)
                print(f'Context: ...{r1.text[start:end]}...\n')
            else:
                print('✗ testprobe123 is NOT reflected')
                if 'search' in r1.text.lower():
                    idx = r1.text.lower().find('search')
                    start = max(0, idx - 50)
                    end = min(len(r1.text), idx + 150)
                    print(f'Search area context: ...{r1.text[start:end]}...\n')
        except Exception as e:
            print(f'Error: {e}\n')
        
        print('='*80)
        print('[TEST 2] Second URL (reported as failing):')
        url2 = 'https://0a340034041b7ff7814d1bf100020041.web-security-academy.net/?search=testprobe123'
        print(f'URL: {url2}')
        print('='*80)
        try:
            r2 = await client.get(url2)
            print(f'Status: {r2.status_code}')
            print(f'Response length: {len(r2.text)} bytes')
            
            if 'testprobe123' in r2.text:
                print('✓ testprobe123 is reflected')
                # Find and show context
                idx = r2.text.find('testprobe123')
                start = max(0, idx - 50)
                end = min(len(r2.text), idx + 120)
                print(f'Context: ...{r2.text[start:end]}...\n')
            else:
                print('✗ testprobe123 is NOT reflected')
                if 'search' in r2.text.lower():
                    idx = r2.text.lower().find('search')
                    start = max(0, idx - 50)
                    end = min(len(r2.text), idx + 150)
                    print(f'Search area context: ...{r2.text[start:end]}...\n')
        except Exception as e:
            print(f'Error: {e}\n')

if __name__ == '__main__':
    asyncio.run(test_urls())
