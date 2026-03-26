#!/usr/bin/env python3
"""
XSSensei - Professional XSS Scanner
Finds ALL potential XSS vulnerabilities with comprehensive payload coverage.
"""

import asyncio
import sys
from pathlib import Path
from time import time

sys.path.insert(0, str(Path(__file__).parent))

from xssensei.modules import (
    initialize_xssensei,
    ContextDiscovery,
    PayloadArmory,
    AsyncFuzzer,
    PlaywrightVerifier,
)
from xssensei.utils import get_logger


async def main():
    """Main scanning pipeline."""
    try:
        # Initialize
        logger, config = initialize_xssensei()
        logger.info(f"\n{'='*60}\n  XSSensei - XSS Scanner\n{'='*60}\n")
        
        # Setup modules
        context_discovery = ContextDiscovery(logger=logger)
        await context_discovery.initialize_client(proxy=config.proxy, verify_ssl=config.verify_ssl)
        
        armory = PayloadArmory(logger=logger)
        if config.wordlist:
            armory.load_custom_wordlist(config.wordlist)
        
        fuzzer = AsyncFuzzer(logger=logger, concurrency=config.threads, timeout=config.timeout)
        await fuzzer.initialize_client(proxy=config.proxy, verify_ssl=config.verify_ssl)
        
        verifier = PlaywrightVerifier(logger=logger, headless=True)
        await verifier.initialize_browser()  # INITIALIZE BROWSER BEFORE VERIFICATION
        
        try:
            all_findings = []
            start_time = time()
            
            for url_index, url in enumerate(config.urls, 1):
                logger.info(f"[{url_index}/{len(config.urls)}] {url}")
                
                # Discover parameters
                reflection_points = await context_discovery.discover_all_parameters(url, timeout=config.timeout)
                
                if not reflection_points:
                    logger.info("  ❌ No parameters found")
                    continue
                
                logger.info(f"  ✓ Found {len(reflection_points)} parameter(s)")
                
                # Log detected reflections
                for point in reflection_points:
                    logger.debug(f"    Parameter '{point.parameter}' reflected in {point.location}")
                
                # Fuzz all parameters with ALL payloads
                payloads_for_params = armory.filter_payloads_for_all_contexts(
                    reflection_points,
                    max_payloads_per_param=200  # Use all payloads for comprehensive coverage
                )
                
                fuzz_results = await fuzzer.fuzz_all_parameters(url, payloads_for_params)
                suspicious_results = fuzzer.get_suspicious_results()
                fuzzer.suspicious_results = []  # Reset for next URL
                
                logger.info(f"  ✓ Tested {len(fuzz_results)} payloads, {len(suspicious_results)} suspicious")
                
                # Verify promising results
                if suspicious_results:
                    logger.info(f"  🔍 Testing {min(20, len(suspicious_results))} with browser...")
                    
                    # Sort suspicious by payload simplicity (simpler first)
                    suspicious_results.sort(key=lambda r: len(r.payload))
                    
                    for result in suspicious_results[:20]:  # Test top 20 results
                        try:
                            # Generate PoC link
                            poc_url = verifier.generate_poc_url(url, result.parameter, result.payload)
                            
                            # Verify with browser
                            finding = await verifier.verify_xss(
                                url=url,
                                parameter=result.parameter,
                                payload=result.payload,
                                timeout=5
                            )
                            
                            if finding:
                                all_findings.append(finding)
                                logger.warning(f"  🎯 XSS FOUND: {result.parameter}")
                                logger.warning(f"     Payload: {result.payload[:80]}")
                                logger.warning(f"     PoC: {poc_url}\n")
                                break  # Found one, move to next URL
                        except Exception as e:
                            logger.debug(f"Verification error for {result.parameter}: {e}")
                            continue
                else:
                    logger.info("  No suspicious results detected. This may be a blind XSS vulnerability.")
            
            # Summary
            elapsed = time() - start_time
            logger.info(f"\n{'='*60}")
            logger.info(f"Scan Complete: {len(all_findings)} vulnerability(ies) found in {elapsed:.1f}s")
            logger.info(f"{'='*60}\n")
            
            if all_findings:
                logger.warning(f"\n🎯 RESULTS:\n")
                for i, finding in enumerate(all_findings, 1):
                    logger.warning(f"{i}. {finding.url} → {finding.parameter}")
                    logger.warning(f"   Payload: {finding.payload}")
                    logger.warning(f"   PoC: {finding.proof_url}\n")
        
        finally:
            await context_discovery.close_client()
            await fuzzer.close_client()
            await verifier.close_browser()
    
    except KeyboardInterrupt:
        logger.warning("\n⚔️  Interrupted")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
