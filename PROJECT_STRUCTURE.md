# XSSensei - Project Structure

## Directory Layout

```
xssensei/
├── main.py                          # Entry point - CLI orchestration
├── requirements.txt                 # Dependencies
├── PROJECT_STRUCTURE.md            # This file
│
├── xssensei/
│   ├── __init__.py
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── module_1_initializer.py   # Banner, CLI Args, Logger
│   │   ├── module_2_context_discovery.py  # Sensei's Eye - Reflection Analysis
│   │   ├── module_3_armory.py        # Smart Payload Manager
│   │   ├── module_4_striker.py       # Async HTTP Requester
│   │   └── module_5_verifier.py      # Playwright Verification
│   │
│   ├── payloads/
│   │   ├── __init__.py
│   │   ├── payload_storage.py        # Payload database (10,000+ payloads)
│   │   ├── payload_categories.py     # Tag-level, Attribute-level, JS-context, Bypass
│   │   └── payload_filters.py        # Context-aware filtering
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                 # Custom logging with colors
│       ├── banner.py                 # Samurai ASCII art & branding
│       ├── models.py                 # Data classes (ScanConfig, Finding, etc.)
│       └── helpers.py                # URL parsing, reflection detection, etc.
```

## Module Roadmap

1. **Module 1**: Initialization (Banner, CLI, Logger)
2. **Module 2**: Context Discovery (Probe String, Reflection Analysis)
3. **Module 3**: Smart Payload Manager (Filter 10,000+ → 50 effective)
4. **Module 4**: Async HTTP Requester (Concurrent fuzzing)
5. **Module 5**: Playwright Verification (Confirm JS execution)

## Key Features

- ✅ Fully asynchronous (asyncio + httpx)
- ✅ Context-aware (Probe String detection)
- ✅ Zero false positives (Playwright verification)
- ✅ Covers Reflected, DOM-based, Reflected-DOM XSS
- ✅ Samurai-themed UI with rich styling
- ✅ Direct PoC links in output
- ✅ Bug hunter focused (real-world scenarios)
