#!/usr/bin/env python3
"""Quick test to verify XSSensei can import without syntax errors."""

try:
    print("Testing imports...")
    from xssensei.payloads.csp_bypass_payloads import CSP_BYPASS_PAYLOADS, PROOF_PAYLOADS
    print(f"✅ CSP_BYPASS_PAYLOADS: {len(CSP_BYPASS_PAYLOADS)} payloads")
    print(f"✅ PROOF_PAYLOADS: {len(PROOF_PAYLOADS)} payloads")
    
    from xssensei.modules import PayloadArmory
    armory = PayloadArmory()
    print(f"✅ PayloadArmory initialized: {armory.total_payloads} total payloads")
    print(f"✅ Categories: {list(armory.payloads.keys())}")
    
    print("\n" + "="*70)
    print("✅ ALL IMPORTS SUCCESSFUL - No syntax errors!")
    print("="*70)
    print("\nYou can now run:")
    print('python main.py -u <TARGET_URL>')
    
except SyntaxError as e:
    print(f"❌ SYNTAX ERROR: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
