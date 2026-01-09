<center><img src="https://github.com/xnl-h4ck3r/xnLinkFinder/blob/main/xnLinkFinder/images/title.png"></center>

# xnLinkFinder-Z - Ultimate Edition v7.18

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/ZeidMahmoud/xnLinkFinder-Z.svg)](https://github.com/ZeidMahmoud/xnLinkFinder-Z/stargazers)
[![Downloads](https://img.shields.io/github/downloads/ZeidMahmoud/xnLinkFinder-Z/total.svg)](https://github.com/ZeidMahmoud/xnLinkFinder-Z/releases)

**The most advanced endpoint discovery and security testing tool** - featuring 40+ powerful security scanners, testing tools, OSINT capabilities, AI/ML analysis, distributed scanning, browser extensions, REST API, and comprehensive automation for bug bounty hunters, penetration testers, and security researchers.

---

## 📋 Table of Contents

- [Features Overview](#-features-overview)
- [What's New](#-whats-new-ultimate-enhancement)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Core Features](#-core-features)
- [Security Scanners](#-security-scanners-new)
- [Advanced Testing](#-advanced-testing-new)
- [OSINT Capabilities](#-osint-capabilities-new)
- [AI/ML Features](#-aiml-features)
- [Server & API Mode](#-server--api-mode-new)
- [Browser Extensions](#-browser-extensions-new)
- [Integrations](#-integrations)
- [CLI Reference](#-cli-reference)
- [Configuration](#-configuration)
- [Examples & Workflows](#-examples--workflows)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Credits & License](#-credits--license)

---

## 🚀 Features Overview

### Core Capabilities
- 🔍 **Advanced Endpoint Discovery** - URLs, APIs, hidden endpoints, parameters
- 🕷️ **Multi-Source Crawling** - Active crawling, Wayback Machine, GitHub, CommonCrawl
- 📊 **Multiple Input Sources** - URLs, files, directories, Burp/ZAP/Caido projects, HAR files
- 🔄 **Async Processing** - High-performance concurrent scanning
- 💾 **Database Backend** - SQLite/PostgreSQL support with caching

### 🛡️ **NEW** Security Scanners (8 modules)
1. **CORS Misconfiguration Scanner** - Detect insecure CORS, credential leakage, wildcard origins
2. **Subdomain Takeover Checker** - DNS checks, cloud service vulnerabilities
3. **Cloud Bucket Scanner** - S3, Azure Blob, GCP bucket enumeration and testing
4. **JWT Attack Generator** - Token analysis, none algorithm, weak secrets, key confusion
5. **SSRF Validator** - Validate SSRF endpoints with bypass techniques
6. **GraphQL Scanner** - Introspection, batch queries, depth attacks
7. **Open Redirect Scanner** - Parameter and path-based redirect testing
8. **Header Injection Scanner** - CRLF, Host header, X-Forwarded-* abuse

### 🧪 **NEW** Advanced Testing (8 modules)
1. **Rate Limit Tester** - Identify rate limit thresholds and bypass techniques
2. **WebSocket Fuzzer** - Message fuzzing and injection testing
3. **Race Condition Tester** - TOCTOU vulnerabilities, concurrent request testing
4. **SSTI Detector** - Server-Side Template Injection for multiple engines
5. **Prototype Pollution Scanner** - JavaScript pollution detection
6. **Mass Assignment Detector** - Hidden parameter discovery
7. **BOLA/BFLA Detector** - Authorization testing (API security)
8. **IDOR Automation** - Automated insecure direct object reference testing

### 🌍 **NEW** OSINT Tools (6 modules)
1. **Google Dorking Engine** - Automated dork generation and execution
2. **Pastebin Monitor** - Real-time monitoring for leaked endpoints
3. **S3 Bucket Finder** - Brute-force bucket discovery with permutations
4. **Favicon Hash Search** - Shodan/Censys integration for infrastructure discovery
5. **JS Library Detector** - Identify vulnerable JavaScript libraries
6. **Archive.today Integration** - Historical page comparison

### 🤖 AI/ML Features
- **LLM-Powered Analysis** - OpenAI, Claude, Ollama integration
- **Neural Pattern Detection** - TensorFlow/PyTorch for obfuscated endpoints
- **Semantic Deduplication** - Smart clustering with sentence transformers
- **Predictive Discovery** - ML-based hidden endpoint prediction
- **Smart Prioritization** - AI-ranked exploitability scoring

### 🌐 **NEW** Server & API Mode
- **REST API Server** - FastAPI-based endpoint with OpenAPI docs
- **Python SDK** - Clean programmatic API with async support
- **Authentication** - JWT-based API authentication
- **Rate Limiting** - Built-in API rate limiting
- **WebSocket Support** - Real-time updates

### 🔧 **NEW** Developer Tools
- **VS Code Extension** - Endpoint discovery while coding
- **Chrome Extension** - Capture endpoints from browser traffic
- **Firefox Extension** - Firefox-compatible endpoint capturing
- **Interactive Wizards** - Setup wizard and quick-start mode
- **Progress Dashboard** - Beautiful terminal progress display
- **Results Explorer** - Interactive results browser
- **Config Manager** - Terminal-based configuration editor

### 📊 Enterprise Features
- **Distributed Scanning** - Redis/RabbitMQ for multi-machine deployment
- **Kubernetes Operator** - Native K8s deployment with Helm charts
- **Real-Time Dashboard** - Live WebSocket monitoring
- **PDF Reports** - Executive-ready security reports
- **Notifications** - Slack, Discord, Telegram integration
- **Proxy Rotation** - Tor/SOCKS5/HTTP proxy support

---

## 🎉 What's NEW: Ultimate Enhancement

This release adds **40+ NEW features** transforming xnLinkFinder-Z into the ultimate security testing platform:

### Security & Testing
✅ 8 New Security Scanners (CORS, JWT, SSRF, GraphQL, etc.)
✅ 8 Advanced Testing Tools (Race Conditions, SSTI, BOLA, IDOR, etc.)
✅ 6 OSINT Collection Tools (Google Dorking, S3 Discovery, etc.)

### Developer Experience
✅ REST API Server with OpenAPI documentation
✅ Python SDK with async support
✅ VS Code, Chrome, and Firefox extensions
✅ Interactive setup wizard and quick-start mode
✅ Progress dashboard and results explorer
✅ Auto-update system with error recovery

### Documentation & Examples
✅ Complete README rewrite documenting ALL features
✅ Unix man page
✅ OpenAPI specification
✅ SDK documentation
✅ 4 Workflow examples (Bug Bounty, CI/CD, Multi-target, etc.)
✅ Video tutorial placeholders

---

## 💿 Installation

### Option 1: pip (Recommended)
```bash
pip install xnlinkfinder
```

### Option 2: pipx (Isolated Environment)
```bash
pipx install git+https://github.com/ZeidMahmoud/xnLinkFinder-Z.git
```

### Option 3: From Source
```bash
git clone https://github.com/ZeidMahmoud/xnLinkFinder-Z.git
cd xnLinkFinder-Z
pip install -e .
```

### Option 4: Docker
```bash
docker pull zeidmahmoud/xnlinkfinder-z:latest
docker run -it xnlinkfinder-z -i https://example.com
```

### System Dependencies (Optional)
For best results with PDF extraction:
```bash
# Linux
sudo apt install -y poppler-utils ocrmypdf

# macOS
brew install poppler ocrmypdf
```

### Upgrade
```bash
pip install --upgrade xnlinkfinder
# Or use built-in auto-update
xnLinkFinder --update
```

---

## ⚡ Quick Start

### Basic Scan
```bash
# Scan a single URL
xnLinkFinder -i https://example.com -o results.txt

# Scan multiple URLs from file
xnLinkFinder -i urls.txt -o endpoints.txt -op parameters.txt
```

### Interactive Wizard
```bash
# First-time setup with guided wizard
xnLinkFinder --wizard

# Quick start mode for common tasks
xnLinkFinder --quick-start
```

### Security Scanning
```bash
# CORS and JWT scanning
xnLinkFinder -i https://api.example.com --scan-cors --scan-jwt

# Comprehensive security scan
xnLinkFinder -i targets.txt \
  --scan-cors \
  --scan-subdomain-takeover \
  --scan-buckets \
  --scan-jwt \
  --validate-ssrf \
  --scan-graphql \
  --scan-open-redirect \
  --scan-headers
```

### OSINT Mode
```bash
# Google dorking + bucket discovery
xnLinkFinder -i example.com \
  --google-dork \
  --find-buckets \
  --favicon-search \
  --detect-js-libs
```

### Advanced Testing
```bash
# Test for authorization issues
xnLinkFinder -i api_endpoints.txt \
  --test-bola \
  --test-idor \
  --test-mass-assignment

# Test for injection vulnerabilities
xnLinkFinder -i urls.txt \
  --test-ssti \
  --test-prototype-pollution \
  --scan-headers
```

### Server Mode
```bash
# Start REST API server
xnLinkFinder --server --server-port 8080 --server-auth

# Use with Python SDK
python -c "
from xnLinkFinder.sdk import XnLinkFinderClient
client = XnLinkFinderClient('http://localhost:8080')
result = client.scan('https://example.com')
print(result)
"
```

---

## 🔍 Core Features

### Endpoint Discovery

**Multi-Source Input:**
- Single URL or domain
- File of URLs/domains
- Directory of files (recursive search)
- Burp Suite XML export
- OWASP ZAP ASCII messages
- Caido CSV export
- HAR (HTTP Archive) files
- Waymore results directory

**Discovery Methods:**
- Active web crawling (depth control)
- JavaScript file analysis
- HTML source parsing
- API documentation extraction
- WebSocket endpoint discovery
- Heap memory analysis (Playwright)

**Output Options:**
```bash
# Multiple output formats
xnLinkFinder -i target.com \
  -o links.txt \           # Discovered endpoints
  -op parameters.txt \      # Potential parameters
  -owl wordlist.txt \       # Target-specific wordlist
  -oo out_of_scope.txt     # Out-of-scope links
```

### Advanced Crawling

**Depth Control:**
```bash
# Crawl 3 levels deep
xnLinkFinder -i https://example.com -d 3
```

**Concurrent Processing:**
```bash
# Use 50 threads
xnLinkFinder -i urls.txt -p 50
```

**Rate Limiting:**
```bash
# Limit to 10 requests/second
xnLinkFinder -i target.com -rl 10
```

**Scope Control:**
```bash
# Filter to specific domains
xnLinkFinder -i target.com -sf scope.txt

# Prefix relative URLs
xnLinkFinder -i files/ -sp https://example.com
```

### Authentication & Headers

**Cookies:**
```bash
xnLinkFinder -i https://example.com \
  -c "session=abc123; token=xyz789"
```

**Custom Headers:**
```bash
xnLinkFinder -i https://api.example.com \
  -H "Authorization: Bearer TOKEN; X-API-Key: KEY"
```

**User Agents:**
```bash
# Multiple user agents
xnLinkFinder -i target.com -u desktop mobile

# Custom user agent
xnLinkFinder -i target.com -uc "CustomBot/1.0"
```

### Filtering & Processing

**Regex Filtering:**
```bash
# Only output matching endpoints
xnLinkFinder -i target.com -ra "/api/v[0-9]\.[0-9]*"
```

**Exclusions:**
```bash
# Exclude patterns
xnLinkFinder -i target.com -x "logout,admin,careers"

# Exclude relative links
xnLinkFinder -i target.com -xrel
```

**ASCII-Only Mode:**
```bash
# Only ASCII characters
xnLinkFinder -i target.com -ascii-only
```

### Performance & Safety

**Timeouts & Retries:**
```bash
xnLinkFinder -i target.com -t 15 -r 3
```

**Response Size Limit:**
```bash
# Max 50MB responses
xnLinkFinder -i target.com -mrs 50
```

**Memory Management:**
```bash
# Stop at 90% memory usage
xnLinkFinder -i target.com -m 90
```

**Time Limits:**
```bash
# Stop after 60 minutes
xnLinkFinder -i target.com -mtl 60
```

---

## 🛡️ Security Scanners (NEW)

### 1. CORS Misconfiguration Scanner

Detects insecure Cross-Origin Resource Sharing configurations.

**Usage:**
```bash
xnLinkFinder -i https://api.example.com --scan-cors
```

**Detects:**
- Credential leakage via CORS
- Wildcard origin with credentials
- Null origin acceptance
- Reflected origins
- Pre-flight bypass

**Programmatic Usage:**
```python
from xnLinkFinder.scanners.cors_scanner import CORSScanner

scanner = CORSScanner()
vulns = scanner.scan('https://api.example.com')
for vuln in vulns:
    print(f"{vuln['severity']}: {vuln['description']}")
```

### 2. Subdomain Takeover Checker

Checks for dangling DNS records and vulnerable cloud services.

**Usage:**
```bash
xnLinkFinder -i subdomains.txt --scan-subdomain-takeover
```

**Detects:**
- GitHub Pages takeover
- Heroku app takeover
- AWS S3 bucket takeover
- Azure WebSites takeover
- Shopify, Fastly, Pantheon, etc.

### 3. Cloud Bucket Scanner

Scans for open or misconfigured cloud storage buckets.

**Usage:**
```bash
xnLinkFinder -i domains.txt --scan-buckets
```

**Supports:**
- AWS S3 buckets (all regions)
- Azure Blob Storage
- Google Cloud Storage
- Tests: LIST, READ, WRITE permissions

**Example:**
```python
from xnLinkFinder.scanners.bucket_scanner import BucketScanner

scanner = BucketScanner()
result = scanner.scan_s3('my-bucket-name')
if result:
    print(f"Bucket status: {result['type']}")
```

### 4. JWT Attack Generator

Analyzes and generates JWT attack payloads.

**Usage:**
```bash
xnLinkFinder -i endpoints.txt --scan-jwt
```

**Features:**
- Decode JWT without verification
- None algorithm attack
- Weak secret testing
- Key confusion (RS256→HS256)
- Claim analysis (exp, aud, iss)

**Example:**
```python
from xnLinkFinder.scanners.jwt_attacks import JWTAttackGenerator

gen = JWTAttackGenerator()
decoded = gen.decode_jwt(token)
none_attack = gen.generate_none_attack(token)
weak_secrets = gen.test_weak_secrets(token)
```

### 5. SSRF Validator

Validates potential SSRF endpoints with bypass techniques.

**Usage:**
```bash
xnLinkFinder -i apis.txt --validate-ssrf \
  --collaborator-url https://burpcollaborator.net/xxx
```

**Tests:**
- AWS metadata (169.254.169.254)
- GCP metadata
- Localhost variations
- URL encoding bypasses
- Burp Collaborator/Interactsh integration

### 6. GraphQL Security Scanner

Comprehensive GraphQL security testing.

**Usage:**
```bash
xnLinkFinder -i https://api.example.com/graphql --scan-graphql
```

**Detects:**
- Introspection enabled
- Batch query DoS
- Deep query nesting
- Field duplication attacks
- Schema extraction

### 7. Open Redirect Scanner

Detects open redirect vulnerabilities.

**Usage:**
```bash
xnLinkFinder -i urls.txt --scan-open-redirect
```

**Tests:**
- Parameter-based redirects
- Path-based redirects
- Common bypass techniques
- JavaScript protocol redirects

### 8. Header Injection Scanner

Tests for header injection vulnerabilities.

**Usage:**
```bash
xnLinkFinder -i urls.txt --scan-headers
```

**Detects:**
- CRLF injection
- Host header injection
- X-Forwarded-* abuse
- Cache poisoning vectors

---

## 🧪 Advanced Testing (NEW)

### 1. Rate Limit Tester

Tests API rate limiting effectiveness.

**Usage:**
```bash
xnLinkFinder -i https://api.example.com/endpoint --test-rate-limit
```

**Features:**
- Concurrent request testing
- Bypass technique testing (IP headers)
- Rate limit header analysis
- Threshold identification

**Example:**
```python
from xnLinkFinder.testing.rate_limit_tester import RateLimitTester

tester = RateLimitTester()
result = tester.test('https://api.example.com', max_requests=100, threads=10)
print(f"Rate limited: {result['rate_limited']} / {result['total_requests']}")
```

### 2. WebSocket Fuzzer

Fuzzes WebSocket connections for vulnerabilities.

**Usage:**
```bash
xnLinkFinder -i ws://example.com/socket --fuzz-websocket
```

**Tests:**
- Message format fuzzing
- XSS in WebSocket messages
- SQL injection
- Template injection
- Large payload handling

### 3. Race Condition Tester

Tests for race condition vulnerabilities.

**Usage:**
```bash
xnLinkFinder -i https://api.example.com/transfer --test-race-condition
```

**Detects:**
- TOCTOU (Time-of-check to time-of-use)
- Double-spend vulnerabilities
- Concurrent request inconsistencies

**Example:**
```python
from xnLinkFinder.testing.race_condition import RaceConditionTester

tester = RaceConditionTester()
result = tester.test(
    'https://api.example.com/withdraw',
    method='POST',
    data={'amount': 100},
    num_requests=20
)
if result['potential_race_condition']:
    print("Race condition detected!")
```

### 4. SSTI Detector

Detects Server-Side Template Injection.

**Usage:**
```bash
xnLinkFinder -i urls.txt --test-ssti
```

**Supports:**
- Jinja2 (Python)
- Twig (PHP)
- Freemarker (Java)
- Velocity (Java)
- Smarty (PHP)
- ERB (Ruby)
- Polyglot payloads

### 5. Prototype Pollution Scanner

Detects JavaScript prototype pollution.

**Usage:**
```bash
xnLinkFinder -i apis.txt --test-prototype-pollution
```

**Tests:**
- `__proto__` pollution
- `constructor.prototype` pollution
- DOM-based pollution
- Server-side pollution

### 6. Mass Assignment Detector

Detects mass assignment vulnerabilities.

**Usage:**
```bash
xnLinkFinder -i api_endpoints.txt --test-mass-assignment
```

**Tests Parameters:**
- admin, is_admin, isAdmin
- role, user_role, privilege
- is_superuser, permissions
- access_level

### 7. BOLA/BFLA Detector

Tests for broken authorization.

**Usage:**
```bash
xnLinkFinder -i apis.txt --test-bola \
  --user-tokens token1,token2,token3
```

**Tests:**
- BOLA (Broken Object Level Authorization)
- BFLA (Broken Function Level Authorization)
- ID enumeration
- Multi-user access testing

### 8. IDOR Automation

Automated IDOR testing.

**Usage:**
```bash
xnLinkFinder -i "https://api.example.com/user/{id}" --test-idor \
  --user-tokens token1,token2 \
  --id-range 1-100
```

**Features:**
- Automatic ID pattern detection
- Multi-user testing
- UUID/Base64/Numeric ID support

---

## 🌍 OSINT Capabilities (NEW)

### 1. Google Dorking Engine

Automated Google dork generation and execution.

**Usage:**
```bash
xnLinkFinder -i example.com --google-dork
```

**Dork Templates:**
- `site:{domain} filetype:pdf`
- `site:{domain} inurl:admin`
- `site:{domain} intitle:"index of"`
- Custom dork templates

### 2. Pastebin Monitor

Monitor Pastebin for leaked endpoints.

**Usage:**
```bash
xnLinkFinder --monitor-pastebin --keywords "example.com,api_key"
```

**Features:**
- Real-time monitoring
- Historical search
- Alert notifications

### 3. S3 Bucket Finder

Brute-force S3 bucket discovery.

**Usage:**
```bash
xnLinkFinder -i example --find-buckets
```

**Permutations:**
- example-dev, example-prod, example-test
- example-backup, example-assets
- example-staging, example-web
- Multi-region scanning

### 4. Favicon Hash Search

Discover infrastructure via favicon hash.

**Usage:**
```bash
xnLinkFinder -i https://example.com --favicon-search \
  --shodan-key YOUR_KEY
```

**Integration:**
- Shodan search
- Censys search
- Related domain discovery

### 5. JS Library Detector

Identify vulnerable JavaScript libraries.

**Usage:**
```bash
xnLinkFinder -i https://example.com --detect-js-libs
```

**Detects:**
- jQuery versions
- React versions
- Angular versions
- CVE matching

### 6. Archive.today Integration

Search historical archived pages.

**Usage:**
```bash
xnLinkFinder -i urls.txt --archive-search
```

**Features:**
- Historical comparison
- Removed endpoint discovery
- Change tracking

---

## 🤖 AI/ML Features

### LLM-Powered Analysis

**Usage:**
```bash
xnLinkFinder -i target.com --llm-analyze \
  --llm-provider openai \
  --llm-key YOUR_API_KEY
```

**Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude
- Ollama (local models)

**Analysis:**
- Endpoint classification
- Vulnerability prediction
- Risk scoring
- Natural language reports

### Neural Pattern Detection

Detect obfuscated endpoints using deep learning.

**Usage:**
```bash
xnLinkFinder -i files/ --neural-detection
```

**Requirements:**
```bash
pip install torch>=2.0.0
```

### Semantic Deduplication

Smart clustering using sentence transformers.

**Usage:**
```bash
xnLinkFinder -i urls.txt --semantic-dedup
```

### Predictive Discovery

ML-based hidden endpoint prediction.

**Usage:**
```bash
xnLinkFinder -i known_endpoints.txt --predict-hidden
```

---

## 🌐 Server & API Mode (NEW)

### Starting the Server

```bash
# Basic server
xnLinkFinder --server

# With authentication
xnLinkFinder --server --server-port 8080 --server-auth

# Custom configuration
xnLinkFinder --server \
  --server-port 9000 \
  --server-host 0.0.0.0 \
  --server-workers 4
```

### API Endpoints

**OpenAPI Documentation:**
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
- OpenAPI JSON: `http://localhost:8080/openapi.json`

**Endpoints:**
```
POST   /scan              - Start a new scan
GET    /scan/{scan_id}    - Get scan results
GET    /scans             - List all scans
DELETE /scan/{scan_id}    - Delete a scan
GET    /health            - Health check
```

### Python SDK

**Installation:**
```bash
pip install xnlinkfinder
```

**Basic Usage:**
```python
from xnLinkFinder.sdk import XnLinkFinderClient

# Initialize client
client = XnLinkFinderClient(
    base_url="http://localhost:8080",
    api_key="your_api_key"  # If auth enabled
)

# Start a scan
scan = client.scan(
    url="https://example.com",
    depth=2,
    scan_cors=True,
    scan_jwt=True
)

print(f"Scan started: {scan['scan_id']}")

# Get results
results = client.get_results(scan['scan_id'])
print(f"Found {len(results['endpoints'])} endpoints")
```

**Async Usage:**
```python
import asyncio
from xnLinkFinder.sdk import XnLinkFinderClient

async def main():
    client = XnLinkFinderClient("http://localhost:8080")
    
    # Async scan
    result = await client.scan_async("https://example.com")
    
    # Wait for completion
    while True:
        status = await client.get_results_async(result['scan_id'])
        if status['status'] == 'complete':
            break
        await asyncio.sleep(5)
    
    print(f"Scan complete: {len(status['endpoints'])} endpoints found")

asyncio.run(main())
```

---

## 🔧 Browser Extensions (NEW)

### VS Code Extension

**Installation:**
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search "xnLinkFinder"
4. Click Install

**Features:**
- Find endpoints in current file
- Highlight discovered endpoints
- Quick test actions
- Integration with REST API

**Usage:**
- Press `Ctrl+Shift+P`
- Type "Find Endpoints with xnLinkFinder"

### Chrome Extension

**Installation:**
1. Download from Chrome Web Store
2. Or load unpacked from `extensions/chrome/`

**Features:**
- Capture endpoints from browser traffic
- Right-click context menu
- Export to JSON/text
- Real-time endpoint discovery
- Automatic deduplication

**Usage:**
1. Click extension icon
2. Click "Capture Endpoints"
3. Browse target website
4. Export results

### Firefox Extension

**Installation:**
1. Download from Firefox Add-ons
2. Or load unpacked from `extensions/firefox/`

**Features:**
- Same as Chrome extension
- Firefox-specific optimizations
- Cross-platform compatibility

---

## 🔗 Integrations

### Burp Suite Integration

```bash
# Import from Burp XML
xnLinkFinder -i burp_export.xml -o endpoints.txt

# With tag removal
xnLinkFinder -i burp_export.xml -brt True
```

**Burp Extension (Advanced):**
- Real-time endpoint push to Burp
- Automatic scope configuration
- Integration with Burp Scanner

### OWASP ZAP Integration

```bash
# Import from ZAP messages
xnLinkFinder -i zap_messages.txt -o endpoints.txt
```

### Caido Integration

```bash
# Import from Caido CSV
xnLinkFinder -i caido_export.csv -o endpoints.txt
```

### Nuclei Template Generator

```bash
# Generate Nuclei templates from endpoints
xnLinkFinder -i endpoints.txt --generate-nuclei
```

### Notifications

**Slack:**
```bash
xnLinkFinder -i target.com --notify-slack --slack-webhook URL
```

**Discord:**
```bash
xnLinkFinder -i target.com --notify-discord --discord-webhook URL
```

**Telegram:**
```bash
xnLinkFinder -i target.com --notify-telegram --telegram-bot-token TOKEN --telegram-chat-id ID
```

---

## 📝 CLI Reference

### Complete Argument List

#### Input/Output
```
-i, --input                 Input URL, file, directory, or Burp/ZAP/Caido file
-o, --output                Output file for links (default: output.txt)
-op, --output-params        Output file for parameters (default: parameters.txt)
-owl, --output-wordlist     Output file for wordlist
-oo, --output-oos           Output file for out-of-scope links
-ow, --output-overwrite     Overwrite output files instead of appending
```

#### Scope & Filtering
```
-sp, --scope-prefix         Prefix for relative URLs
-spo, --scope-prefix-original  Include original relative links
-spkf, --scope-prefix-keep-failed  Keep failed prefix attempts
-sf, --scope-filter         Domain scope filter
-ra, --regex-after          Regex filter for output
-x, --exclude               Exclusion patterns (comma-separated)
-xrel, --exclude-relative-links  Exclude relative links
```

#### HTTP Configuration
```
-c, --cookies               Cookies (format: 'name1=value1; name2=value2')
-H, --headers               Custom headers (format: 'Header1: value1; Header2: value2')
-u, --user-agent            User agent selection (desktop, mobile, mobile-apple, etc.)
-uc, --user-agent-custom    Custom user agent string
-insecure                   Disable TLS certificate verification
-t, --timeout               Request timeout in seconds (default: 10)
-r, --retries               Number of retries after failure (max: 5)
-mrs, --max-response-size   Maximum response size in MB
-fp, --forward-proxy        Forward proxy (e.g., http://127.0.0.1:8080)
```

#### Performance & Control
```
-d, --depth                 Crawl depth (default: 1)
-p, --processes             Number of concurrent threads (default: 25)
-rl, --rate-limit           Requests per second (0 = unlimited)
-m, --memory-threshold      Memory usage threshold percentage (default: 95)
-mtl, --max-time-limit      Maximum scan time in minutes (0 = unlimited)
-s429                       Stop if >95% responses are 429
-s403                       Stop if >95% responses are 403
-sTO                        Stop if >95% requests timeout
-sCE                        Stop if >95% requests have connection errors
```

#### Security Scanners (NEW)
```
--scan-cors                 Scan for CORS misconfigurations
--scan-subdomain-takeover   Check for subdomain takeover
--scan-buckets              Scan for open cloud buckets
--scan-jwt                  Analyze and attack JWT tokens
--validate-ssrf             Validate SSRF vulnerabilities
--scan-graphql              Deep GraphQL security scan
--scan-open-redirect        Detect open redirects
--scan-headers              Header injection testing
```

#### Advanced Testing (NEW)
```
--test-rate-limit           Test API rate limiting
--fuzz-websocket            Fuzz WebSocket connections
--test-race-condition       Test for race conditions
--test-ssti                 SSTI detection
--test-prototype-pollution  Prototype pollution scan
--test-mass-assignment      Mass assignment detection
--test-bola                 BOLA/BFLA testing
--test-idor                 Automated IDOR testing
```

#### OSINT (NEW)
```
--google-dork               Enable Google dorking
--monitor-pastebin          Monitor Pastebin
--find-buckets              Brute-force bucket discovery
--favicon-search            Favicon hash search
--detect-js-libs            Detect JS libraries
--archive-search            Search archive.today
```

#### AI/ML Features
```
--llm-analyze               Enable LLM analysis
--llm-provider              LLM provider (openai, claude, ollama)
--llm-key                   LLM API key
--neural-detection          Enable neural pattern detection
--semantic-dedup            Semantic deduplication
--predict-hidden            Predict hidden endpoints
--ai-prioritize             AI-based priority scoring
```

#### Server Mode (NEW)
```
--server                    Start REST API server
--server-port               Server port (default: 8080)
--server-host               Server host (default: 0.0.0.0)
--server-auth               Enable authentication
--server-workers            Number of worker processes
```

#### User Experience (NEW)
```
--wizard                    Interactive setup wizard
--quick-start               Quick start mode
--check-update              Check for updates
--update                    Update to latest version
--cheat-sheet               Generate cheat sheet
--explore-results FILE      Interactive results explorer
--config-editor             Interactive config editor
--progress-dashboard        Show progress dashboard
```

#### Advanced Options
```
--heap                      Extract links from browser heap memory
-ro, --readable-only        Extract only human-readable text
-ascii-only                 Only ASCII characters in output
-inc, --include             Include input URLs in output
-orig, --origin             Show origin URL in output
-prefixed                   Show which links were prefixed
-mfs, --max-file-size       Max file size in MB (default: 500)
--config                    Path to config.yml file
```

#### Wordlist Options
```
-nwlpl, --no-wordlist-plurals      No plural/singular variations
-nwlpw, --no-wordlist-pathwords    No path words in wordlist
-nwlpm, --no-wordlist-parameters   No parameters in wordlist
-nwlc, --no-wordlist-comments      No comments in wordlist
-nwlia, --no-wordlist-imgalt       No image alt text in wordlist
-nwld, --no-wordlist-digits        Exclude words with digits
-nwll, --no-wordlist-lowercase     No automatic lowercase
-wlml, --wordlist-maxlen           Max word length
-swf, --stopwords-file             Additional stop words file
```

#### Burp/ZAP/Caido Options
```
-brt, --burpfile-remove-tags  Remove tags from Burp file (True/False)
```

#### Documentation
```
--generate-man              Generate man page
--examples                  Show usage examples
--help                      Show help message
--version                   Show version
```

---

## ⚙️ Configuration

### config.yml

xnLinkFinder-Z uses a YAML configuration file for default settings.

**Location:**
- Linux/macOS: `~/.config/xnLinkFinder/config.yml`
- Windows: `%APPDATA%\xnLinkFinder\config.yml`

**Basic Configuration:**
```yaml
# Default settings
default_depth: 1
default_processes: 25
default_timeout: 10

# Exclusions
link_exclusions:
  - logout
  - signout
  - admin
  - careers
  - jobs

# API Keys (optional)
shodan_api_key: YOUR_SHODAN_KEY
github_token: YOUR_GITHUB_TOKEN
openai_api_key: YOUR_OPENAI_KEY

# Notifications (optional)
slack_webhook: https://hooks.slack.com/...
discord_webhook: https://discord.com/api/webhooks/...
telegram_bot_token: YOUR_BOT_TOKEN
telegram_chat_id: YOUR_CHAT_ID

# Server settings
server:
  port: 8080
  host: 0.0.0.0
  auth_enabled: true
  rate_limit: 100  # requests per minute
```

### Profiles

Create reusable scan profiles:

```yaml
# profiles.yml
profiles:
  quick_scan:
    depth: 1
    processes: 50
    timeout: 5
    
  deep_scan:
    depth: 3
    processes: 25
    timeout: 15
    scan_cors: true
    scan_jwt: true
    
  bug_bounty:
    depth: 2
    processes: 30
    scan_cors: true
    scan_jwt: true
    scan_buckets: true
    validate_ssrf: true
    test_bola: true
    google_dork: true
```

**Usage:**
```bash
xnLinkFinder -i target.com --profile bug_bounty
```

---

## 📚 Examples & Workflows

### Bug Bounty Workflow

```bash
#!/bin/bash
TARGET="example.com"

# Phase 1: Recon
xnLinkFinder -i $TARGET \
  --google-dork \
  --find-buckets \
  --archive-search \
  -o ${TARGET}_recon.txt

# Phase 2: Endpoint Discovery
xnLinkFinder -i $TARGET \
  -d 3 \
  --include-wayback \
  --include-github \
  -o ${TARGET}_endpoints.txt

# Phase 3: Security Scanning
xnLinkFinder -i ${TARGET}_endpoints.txt \
  --scan-cors \
  --scan-jwt \
  --scan-buckets \
  --validate-ssrf \
  --scan-graphql \
  --scan-open-redirect \
  -o ${TARGET}_vulns.txt

# Phase 4: Advanced Testing
xnLinkFinder -i ${TARGET}_endpoints.txt \
  --test-bola \
  --test-idor \
  --test-ssti \
  --test-race-condition \
  -o ${TARGET}_advanced.txt

# Phase 5: Report
xnLinkFinder --generate-report \
  --input ${TARGET}_vulns.txt \
  --format pdf \
  --output ${TARGET}_report.pdf
```

### CI/CD Integration

```yaml
# .github/workflows/security-scan.yml
name: Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install xnLinkFinder
        run: pip install xnlinkfinder
      
      - name: Security Scan
        run: |
          xnLinkFinder -i https://staging.example.com \
            --scan-cors \
            --scan-jwt \
            --test-bola \
            --fail-on-critical \
            -o scan_results.txt
      
      - name: Upload Results
        uses: actions/upload-artifact@v2
        with:
          name: scan-results
          path: scan_results.txt
```

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  xnlinkfinder-api:
    image: zeidmahmoud/xnlinkfinder-z:latest
    ports:
      - "8080:8080"
    environment:
      - SERVER_PORT=8080
      - SERVER_AUTH=true
      - REDIS_URL=redis://redis:6379
    command: --server
    
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    
  postgres:
    image: postgres:14
    environment:
      - POSTGRES_DB=xnlinkfinder
      - POSTGRES_USER=xnlf
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### Multi-Target Scanning

```python
#!/usr/bin/env python3
# multi_target_scan.py

from xnLinkFinder.sdk import XnLinkFinderClient
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_target(client, target):
    """Scan a single target"""
    print(f"[*] Scanning {target}")
    result = client.scan(
        url=target,
        depth=2,
        scan_cors=True,
        scan_jwt=True
    )
    return {
        'target': target,
        'scan_id': result['scan_id']
    }

def main():
    # Initialize client
    client = XnLinkFinderClient("http://localhost:8080")
    
    # Load targets
    with open('targets.txt') as f:
        targets = [line.strip() for line in f if line.strip()]
    
    # Scan all targets concurrently
    scans = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(scan_target, client, target): target
            for target in targets
        }
        
        for future in as_completed(futures):
            try:
                result = future.result()
                scans.append(result)
                print(f"[+] Started scan for {result['target']}")
            except Exception as e:
                print(f"[!] Error: {e}")
    
    # Wait for all scans to complete
    print(f"\n[*] Waiting for {len(scans)} scans to complete...")
    
    for scan in scans:
        while True:
            status = client.get_results(scan['scan_id'])
            if status['status'] == 'complete':
                print(f"[+] {scan['target']}: {len(status['endpoints'])} endpoints")
                break
            time.sleep(5)

if __name__ == "__main__":
    import time
    main()
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Import Error: No module named 'xnLinkFinder'**
```bash
# Ensure proper installation
pip install --upgrade xnlinkfinder

# Or install from source
cd xnLinkFinder-Z && pip install -e .
```

**2. SSL Certificate Errors**
```bash
# Disable SSL verification (use cautiously)
xnLinkFinder -i https://example.com -insecure
```

**3. Memory Issues**
```bash
# Reduce memory threshold
xnLinkFinder -i target.com -m 80

# Limit concurrent processes
xnLinkFinder -i target.com -p 10
```

**4. Rate Limiting**
```bash
# Add rate limiting
xnLinkFinder -i target.com -rl 5  # 5 req/sec

# Add delays
xnLinkFinder -i target.com --delay 1000  # 1 second
```

**5. Timeout Issues**
```bash
# Increase timeout
xnLinkFinder -i target.com -t 30

# Add retries
xnLinkFinder -i target.com -t 15 -r 3
```

**6. PDF Extraction Not Working**
```bash
# Install system dependencies
sudo apt install -y poppler-utils ocrmypdf  # Linux
brew install poppler ocrmypdf               # macOS
```

**7. Browser Extensions Not Loading**
- Chrome: Enable Developer Mode in chrome://extensions/
- Firefox: about:debugging -> Load Temporary Add-on
- VS Code: Reload window after installation

### Debug Mode

```bash
# Enable debug logging
xnLinkFinder -i target.com --debug

# Verbose output
xnLinkFinder -i target.com --verbose

# Log to file
xnLinkFinder -i target.com --log-file scan.log
```

### Performance Tuning

**For Large Scans:**
```bash
xnLinkFinder -i targets.txt \
  -p 50 \              # More threads
  -rl 20 \             # Higher rate limit
  -m 90 \              # More memory
  --cache-enable \     # Enable caching
  --distributed \      # Use distributed mode
  --redis-url redis://localhost:6379
```

**For Slow Networks:**
```bash
xnLinkFinder -i target.com \
  -t 30 \              # Longer timeout
  -r 5 \               # More retries
  -p 10                # Fewer threads
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

1. Check existing issues
2. Create detailed bug report with:
   - xnLinkFinder version
   - Python version
   - OS and version
   - Command used
   - Error message/traceback
   - Expected vs actual behavior

### Feature Requests

1. Check if feature already requested
2. Describe use case
3. Provide examples
4. Explain benefits

### Pull Requests

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear message
7. Push to branch
8. Open Pull Request

### Coding Standards

- Follow PEP 8
- Add docstrings to functions
- Include type hints
- Write unit tests
- Update README if needed

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=xnLinkFinder tests/

# Run linter
flake8 xnLinkFinder/
black xnLinkFinder/
```

---

## ❓ FAQ

**Q: What's the difference between xnLinkFinder and xnLinkFinder-Z?**
A: xnLinkFinder-Z is the ultimate enhanced version with 40+ additional features including security scanners, advanced testing, OSINT tools, AI/ML capabilities, REST API, browser extensions, and much more.

**Q: Is xnLinkFinder-Z free?**
A: Yes, it's completely free and open-source under the MIT license.

**Q: Can I use it for bug bounty hunting?**
A: Absolutely! It's designed with bug bounty hunters in mind and includes specialized workflows.

**Q: Does it work on Windows?**
A: Yes, it works on Windows, Linux, and macOS.

**Q: How do I update to the latest version?**
A: Run `pip install --upgrade xnlinkfinder` or use `xnLinkFinder --update`

**Q: Can I run it in Docker?**
A: Yes, we provide official Docker images.

**Q: Does it support headless browsers?**
A: Yes, via Playwright integration.

**Q: Can I use it programmatically?**
A: Yes, use the Python SDK for full programmatic access.

**Q: Is distributed scanning supported?**
A: Yes, via Redis/RabbitMQ for multi-machine deployments.

**Q: How do I report security vulnerabilities?**
A: Email security@xnlinkfinder-z.com or use GitHub Security Advisories.

---

## 📜 Changelog

### v7.18 - Ultimate Enhancement (2026-01-09)

**🎉 Major Release: 40+ New Features**

#### Security Scanners (8 new modules)
- ✅ CORS Misconfiguration Scanner
- ✅ Subdomain Takeover Checker
- ✅ Cloud Bucket Scanner (S3/Azure/GCP)
- ✅ JWT Attack Generator
- ✅ SSRF Validator
- ✅ GraphQL Security Scanner
- ✅ Open Redirect Scanner
- ✅ Header Injection Scanner

#### Advanced Testing (8 new modules)
- ✅ Rate Limit Tester
- ✅ WebSocket Fuzzer
- ✅ Race Condition Tester
- ✅ SSTI Detector
- ✅ Prototype Pollution Scanner
- ✅ Mass Assignment Detector
- ✅ BOLA/BFLA Detector
- ✅ IDOR Automation

#### OSINT Tools (6 new modules)
- ✅ Google Dorking Engine
- ✅ Pastebin Monitor
- ✅ S3 Bucket Finder
- ✅ Favicon Hash Search
- ✅ JS Library Detector
- ✅ Archive.today Integration

#### Developer Tools
- ✅ REST API Server (FastAPI)
- ✅ Python SDK with async support
- ✅ VS Code Extension
- ✅ Chrome Extension
- ✅ Firefox Extension

#### User Experience
- ✅ Interactive Setup Wizard
- ✅ Quick Start Mode
- ✅ Auto-Update System
- ✅ Progress Dashboard
- ✅ Results Explorer
- ✅ Config Manager
- ✅ Cheat Sheet Generator
- ✅ Error Recovery System

#### Documentation
- ✅ Complete README rewrite (all features documented)
- ✅ Unix man page
- ✅ OpenAPI specification
- ✅ SDK documentation
- ✅ Video tutorial placeholders
- ✅ 4 workflow examples

#### Dependencies
- ✅ Added 10+ new dependencies
- ✅ Updated requirements.txt
- ✅ Updated setup.py

**Full Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

## 💖 Credits & License

### Original Author
**@xnl-h4ck3r** - Original xnLinkFinder creator

### Ultimate Enhancement
**ZeidMahmoud** - 40+ feature additions and comprehensive updates

### Contributors
- View all contributors: [Contributors](https://github.com/ZeidMahmoud/xnLinkFinder-Z/graphs/contributors)

### Acknowledgments
- Based on [LinkFinder](https://github.com/GerbenJavado/LinkFinder) by Gerben Javado
- Inspired by [GAP Burp Extension](https://github.com/xnl-h4ck3r/burp-extensions)
- Community feedback and contributions

### License
MIT License - see [LICENSE](LICENSE) file

### Support

If you find this tool helpful:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🔀 Submit pull requests
- ☕ [Buy me a coffee](https://ko-fi.com/xnlh4ck3r)

### Contact

- GitHub Issues: [Issues](https://github.com/ZeidMahmoud/xnLinkFinder-Z/issues)
- Twitter: [@xnl_h4ck3r](https://twitter.com/xnl_h4ck3r)
- Email: security@xnlinkfinder-z.com

---

<center>
Made with ❤️ by the security community
<br>
<b>Happy Hunting! 🎯</b>
</center>
