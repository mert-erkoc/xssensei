# XSSensei - Quick Start Guide

## 🚀 Installation

```bash
# Navigate to project
cd xssensei

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (one-time setup)
python -m playwright install
```

## ▶️ Run Your First Scan

### Option 1: Quick Test with Public Labs

Test against DVWA (Damn Vulnerable Web Application):
```bash
python main.py -u "http://dvwa.local/vulnerabilities/xss_r/?name=test"
```

### Option 2: Test Against PortSwigger Academy

```bash
# Reflected XSS lab
python main.py -u "http://portswigger-lab/?search=test"

# DOM-based XSS lab  
python main.py -u "http://portswigger-lab/?name=test"
```

### Option 3: Local Testing

Set up a simple vulnerable app and test:
```bash
python main.py -u "http://localhost:8000/search?q=test"
```

## 📋 Common Commands

### Verbose Output (Debug Mode)
```bash
python main.py -u "http://target.com/?q=test" -v
```

### Increase Concurrency (Speed Up)
```bash
python main.py -u "http://target.com/?q=test" --threads 50
```

### Scan Multiple URLs
Create `targets.txt`:
```
http://target1.com/?q=test
http://target2.com/?search=x
http://target3.com/?id=1
```

Then:
```bash
python main.py -l targets.txt --threads 20
```

### Use Custom Payloads
Create `custom_payloads.txt` (one per line):
```
<img src=x onerror=alert(document.domain)>
<svg onload=alert(String.fromCharCode(88,83,83))>
...
```

Then:
```bash
python main.py -u "http://target.com/?q=test" -w custom_payloads.txt
```

### Through Burp Suite Proxy
```bash
python main.py -u "http://target.com/?q=test" -p "http://127.0.0.1:8080"
```

### Extended Timeout (Slow Targets)
```bash
python main.py -u "http://target.com/?q=test" --timeout 20
```

## 📊 What to Expect

### Successful Scan Output

```
[✓] Katana Verified! Vulnerability found!

Parameter: q
Payload: <img src=x onerror=alert(1)>
PoC Link: http://target.com/?q=<img src=x onerror=alert(1)>
Severity: HIGH
```

### No Vulnerabilities Found

```
============================================================
📋 MISSION REPORT
============================================================
URLs Scanned: 1
Payloads Sent: 150
Vulnerabilities Found: 0
Scan Duration: 12.34s
============================================================

[✓] Mission Complete: No vulnerabilities found.
```

## 🔍 Understanding the Output

### The 5 Stages

1. **🔷 Initialization** - Banner, CLI parsing, logging setup
2. **⚔️ Sharpening the blade** - Context discovery (probe strings)
3. **🎯 Striking** - Async payload fuzzing
4. **🔍 Verifying** - Browser-based verification
5. **📋 Mission Report** - Final summary with PoC links

### Log Levels

- `[INFO]` - Normal progress
- `[WARNING]` - Suspicious findings (potential vulnerability)
- `[ERROR]` - Critical issues
- `[DEBUG]` - Detailed info (use with `-v` flag)

## 💡 Best Practices

### 1. Start with Single Parameter
```bash
python main.py -u "http://target.com/?search=test"
```

### 2. Monitor Progress
Use verbose mode to see what's happening:
```bash
python main.py -u "http://target.com/?q=test" -v
```

### 3. Scale Gradually
- Start with 10 threads (default)
- Increase if no rate limiting: `--threads 30`
- Reduce if getting 429 errors: `--threads 5`

### 4. Use Custom Wordlist
If target has special payloads:
```bash
python main.py -u "http://target.com/?q=test" -w payloads.txt
```

### 5. Integrate with Burp
Capture parameters in Burp, then test with XSSensei:
```bash
python main.py -u "http://target.com/?param=injectionpoint" -p "http://127.0.0.1:8080"
```

## 🎯 Target Application Requirements

XSSensei requires:
- ✅ HTTP GET parameters with reflection
- ✅ JavaScript enabled for verification
- ✅ Timeout > 5 seconds recommended
- ✅ Accepts standard URL encoding

## ⚠️ Limitations

- Limited to GET parameters (POST coming soon)
- Requires JavaScript execution for final verification
- WAF might rate-limit (use `--threads 5` or proxy)
- Works with 200 status code responses

## 🛠️ Troubleshooting

### Issue: "Playwright not installed"
```bash
pip install playwright
python -m playwright install
```

### Issue: "Connection refused"
```bash
# Check target is accessible
curl http://target.com/?test=1

# Then try scan
python main.py -u "http://target.com/?test=1"
```

### Issue: "No reflected parameters found"
```bash
# Wrong parameter or target
python main.py -u "http://target.com/?existingparam=value" -v
```

### Issue: "Too slow / rate limited"
```bash
python main.py -u "http://target.com/?q=test" --threads 5 --timeout 20
```

## 📚 Learning Resources

- Follow the code in order:
  1. `xssensei/modules/module_1_initializer.py` - CLI setup
  2. `xssensei/modules/module_2_context_discovery.py` - How context is detected
  3. `xssensei/modules/module_3_armory.py` - Payload filtering logic
  4. `xssensei/modules/module_4_striker.py` - Fuzzing implementation
  5. `xssensei/modules/module_5_verifier.py` - Browser verification

## 🎓 Test Cases

### PortSwigger Academy Labs (Free)

```bash
# Reflected XSS
python main.py -u "https://portswigger.net/web-security/xss/reflected/lab-html-context-nothing-encoded"

# Stored XSS (coming soon)
# DOM-based XSS (coming soon)
```

### DVWA (Local)
```bash
python main.py -u "http://localhost/dvwa/vulnerabilities/xss_r/?name=test"
```

## 📞 Support

Check the detailed documentation:
- `README.md` - Project overview
- `DEVELOPMENT_SUMMARY.md` - Architecture details
- `COMPLETE_IMPLEMENTATION.md` - Full technical details

---

**Happy hunting! 🗡️**
