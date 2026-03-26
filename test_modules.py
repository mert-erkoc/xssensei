"""
Test/Example file to demonstrate Module 1 and Module 2 functionality.
"""

import asyncio
from xssensei.modules import initialize_xssensei, ContextDiscovery


async def test_initialization():
    """Test Module 1: Initialization with sample arguments."""
    print("\n" + "="*60)
    print("Testing Module 1: Initialization")
    print("="*60 + "\n")
    
    test_args = [
        '-u', 'http://vulnerable.app/search?q=test&filter=id',
        '--threads', '5',
        '--timeout', '10',
    ]
    
    logger, config = initialize_xssensei(test_args)
    
    logger.info("✓ Module 1 test completed successfully")
    return logger, config


async def test_context_discovery():
    """Test Module 2: Context Discovery."""
    print("\n" + "="*60)
    print("Testing Module 2: Context Discovery")
    print("="*60 + "\n")
    
    logger, config = await test_initialization()
    
    # Initialize context discovery
    context = ContextDiscovery(logger=logger)
    await context.initialize_client(
        proxy=config.proxy,
        verify_ssl=config.verify_ssl
    )
    
    try:
        # Test with DVWA or other vulnerable application
        # For now, this is a demonstration structure
        url = config.urls[0] if config.urls else "http://localhost/dvwa/vulnerabilities/xss_r/?name=test"
        
        logger.info(f"Testing context discovery on: {url}")
        
        # Discover parameters
        reflection_points = await context.discover_all_parameters(
            url,
            timeout=config.timeout
        )
        
        if reflection_points:
            logger.info(f"✓ Found {len(reflection_points)} reflected parameters")
            
            # Show summary
            summary = context.summarize_context(reflection_points)
            logger.info(summary)
            
            # Get injection points
            injection_map = context.get_injection_points(reflection_points)
            logger.info(f"Injection strategies available: {list(injection_map.keys())}")
        else:
            logger.warning("No reflected parameters found (expected if target is not vulnerable)")
    
    finally:
        await context.close_client()
    
    logger.info("✓ Module 2 test completed successfully")


async def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(" XSSENSEI - MODULE TESTING ".center(70, "*"))
    print("="*70)
    
    try:
        await test_context_discovery()
        
        print("\n" + "="*70)
        print(" ALL TESTS COMPLETED SUCCESSFULLY ".center(70, "✓"))
        print("="*70 + "\n")
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == '__main__':
    # Run tests
    asyncio.run(main())
