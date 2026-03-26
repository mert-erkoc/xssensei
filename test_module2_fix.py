#!/usr/bin/env python
"""Test the updated reflection detection logic."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xssensei.modules import ContextDiscovery
from xssensei.utils import get_logger

async def test_module_2_fix():
    """Test Module 2 with both lab URLs."""
    
    logger = get_logger('TestModule2')
    discovery = ContextDiscovery(logger=logger)
    await discovery.initialize_client(verify_ssl=False)
    
    # Test both URLs
    urls = [
        ('URL 1 (No explicit reflection)', 'https://0ad100780328d3268847c02e00bd00d2.web-security-academy.net/?search=test'),
        ('URL 2 (With reflection)', 'https://0a340034041b7ff7814d1bf100020041.web-security-academy.net/?search=test'),
    ]
    
    for label, url in urls:
        print(f"\n{'='*80}")
        print(f"Testing: {label}")
        print(f"{'='*80}")
        
        try:
            reflection_points = await discovery.discover_all_parameters(url)
            
            if reflection_points:
                print(f"Found {len(reflection_points)} parameters:")
                for point in reflection_points:
                    marker = "[ASSUMED]" if "[assumed]" in point.reflected_value else "[EXPLICIT]"
                    print(f"  {marker} {point.parameter} -> {point.location}")
                
                # Show context summary
                summary = discovery.summarize_context(reflection_points)
                print(summary)
            else:
                print("No parameters found")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    
    await discovery.close_client()
    print("\nTest complete!")

if __name__ == '__main__':
    asyncio.run(test_module_2_fix())
