#!/usr/bin/env python3
"""Diagnostic tool to test if XSS PoC links actually execute in real browser."""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

async def test_poc_link(poc_url: str, timeout: int = 10):
    """
    Test if a PoC link actually executes JavaScript in browser.
    
    Args:
        poc_url: Full URL with XSS payload (e.g., https://...?param=payload)
        timeout: Test timeout in seconds
    """
    print(f"\n{'='*70}")
    print(f"XSS PoC DIAGNOSTIC TEST")
    print(f"{'='*70}")
    print(f"Testing URL: {poc_url}")
    print(f"Timeout: {timeout}s")
    print('='*70)
    
    async with async_playwright() as p:
        # Launch browser with verbose logging
        browser = await p.chromium.launch(headless=False)  # headless=False to SEE browser
        page = await browser.new_page()
        
        # Track execution indicators
        dialog_detected = False
        page_title_changed = False
        console_messages = []
        javascript_errors = []
        
        # Dialog handler
        async def on_dialog(dialog):
            nonlocal dialog_detected
            print(f"\n🎯 DIALOG DETECTED: {dialog.type}")
            print(f"   Message: {dialog.message}")
            dialog_detected = True
            await dialog.dismiss()
        
        # Console handler
        def on_console(msg):
            nonlocal page_title_changed
            text = msg.text
            console_messages.append(f"{msg.type}: {text}")
            print(f"   📝 Console [{msg.type}]: {text}")
            
            if 'error' in msg.type.lower():
                javascript_errors.append(text)
        
        # Error handler
        def on_error(error):
            print(f"   ⚠️  Uncaught error: {error}")
        
        page.on('dialog', on_dialog)
        page.on('console', on_console)
        page.on('pageerror', on_error)
        
        try:
            print("\n📡 Navigating to URL...")
            response = await page.goto(poc_url, wait_until='domcontentloaded', timeout=timeout*1000)
            
            if response:
                print(f"✓ Response status: {response.status}")
            
            # Wait for any delayed JavaScript
            await asyncio.sleep(2)
            
            # Check page state
            print("\n🔍 Checking page state...")
            try:
                title = await page.title()
                print(f"✓ Page title: {title}")
            except:
                pass
            
            # Try to get page content
            try:
                content = await page.content()
                if len(content) > 0:
                    print(f"✓ Page content length: {len(content)} bytes")
                    
                    # Check if payload is in page
                    if 'alert' in content.lower():
                        print(f"✓ 'alert' keyword found in page content")
                    
                    # Show first 500 chars of page
                    print(f"\n   Page content preview (first 500 chars):")
                    print(f"   {content[:500]}")
            except Exception as e:
                print(f"✗ Couldn't get page content: {e}")
            
            # Test if JavaScript can execute
            print("\n⚙️  Testing JavaScript execution capability...")
            try:
                result = await page.evaluate('window.location.href')
                print(f"✓ JavaScript can execute! Current URL: {result}")
            except Exception as e:
                print(f"✗ JavaScript execution blocked: {e}")
            
        except asyncio.TimeoutError:
            print(f"❌ TIMEOUT: Page didn't load within {timeout}s")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        finally:
            await browser.close()
    
    # Summary
    print(f"\n{'='*70}")
    print("RESULTS:")
    print('='*70)
    print(f"✓ Dialog Triggered? {dialog_detected}")
    print(f"✓ Console Messages: {len(console_messages)}")
    if javascript_errors:
        print(f"⚠️  JavaScript Errors: {len(javascript_errors)}")
        for err in javascript_errors:
            print(f"   - {err[:80]}")
    print('='*70)
    
    if dialog_detected:
        print("\n✅ XSS CONFIRMED - Alert was triggered in browser!")
        return True
    else:
        print("\n⚠️  Alert not detected. Possible causes:")
        print("   1. CSP (Content Security Policy) headers blocking execution")
        print("   2. Browser XSS Auditor/Protection")
        print("   3. Payload not properly reflected in page")
        print("   4. JavaScript execution disabled")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python poc_test.py '<complete_PoC_URL>'")
        print("\nExample:")
        print('python poc_test.py "https://example.com/?search=%22%3Balert%281%29%3B%2F%2F"')
        sys.exit(1)
    
    poc_url = sys.argv[1]
    
    try:
        result = asyncio.run(test_poc_link(poc_url))
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted")
        sys.exit(1)
