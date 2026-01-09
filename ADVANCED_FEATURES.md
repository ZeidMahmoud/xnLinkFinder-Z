# xnLinkFinder-Z Advanced Features

## 🚀 New Advanced Features

xnLinkFinder-Z extends the original xnLinkFinder with powerful enterprise-grade features for comprehensive endpoint discovery and security analysis.

### 🔥 Core Enhancements

#### 1. Async/Concurrent Processing
- **Async HTTP crawler** using `aiohttp` for efficient parallel processing
- **Smart connection pooling** with configurable concurrency limits
- **Adaptive rate limiting** with automatic backoff on 429/503 responses
- **Per-domain rate limiting** for fine-grained control

```bash
# Use async crawler with 50 concurrent connections
xnLinkFinder -i target.com --async --max-concurrent 50 --rate-limit 10
```

#### 2. Database Backend for Large Scans
- **SQLite database** for storing discovered links with full metadata
- **Incremental scanning** - resume interrupted scans
- **Scan history tracking** over time
- **Export to JSON/CSV** formats

```bash
# Enable database mode
xnLinkFinder -i target.com --use-database --db-path scan.db

# Export results
xnLinkFinder --export-db scan.db --format json --output results.json
```

#### 3. Caching Layer
- **DNS caching** for faster lookups
- **Static resource caching** with TTL
- **ETag/Last-Modified checking** to avoid re-downloading unchanged resources

```bash
# Enable caching
xnLinkFinder -i target.com --use-cache --cache-ttl 3600
```

### 🔍 Discovery Features

#### 4. GraphQL Discovery
- **Automatic GraphQL endpoint detection**
- **Schema introspection** to discover all queries and mutations
- **Full schema extraction** including types and fields

```bash
# Enable GraphQL discovery
xnLinkFinder -i target.com --discover-graphql
```

#### 5. OpenAPI/Swagger Discovery
- **Auto-detection** of OpenAPI/Swagger specs
- **Endpoint extraction** from specifications
- **Security scheme identification**

```bash
# Enable OpenAPI discovery
xnLinkFinder -i target.com --discover-openapi
```

#### 6. Source Map Parsing
- **Automatic source map detection** (.map files)
- **Original source code recovery**
- **Hidden endpoint extraction** from development comments

```bash
# Enable source map parsing
xnLinkFinder -i target.com --parse-sourcemaps
```

#### 7. Cloud Service Detection
- **AWS services**: S3 buckets, Lambda functions, API Gateway, CloudFront
- **Azure services**: Blob storage, Functions, App Services
- **GCP services**: Cloud Storage, Cloud Functions, App Engine
- **Firebase**: Hosting, Database, Storage, Functions

```bash
# Enable cloud service detection
xnLinkFinder -i target.com --detect-cloud-services
```

#### 8. WebSocket Enumeration
- **WebSocket endpoint discovery**
- **Socket.io detection**
- **SockJS detection**

```bash
# Enable WebSocket discovery
xnLinkFinder -i target.com --discover-websockets
```

#### 9. JavaScript Runtime Analysis (Playwright)
- **Headless browser integration** for dynamic JS analysis
- **Network request interception**
- **Heap snapshot analysis** for dynamically generated endpoints
- **JavaScript execution context extraction**

```bash
# Enable browser-based analysis
xnLinkFinder -i target.com --use-browser --heap-extract
```

### 🛡️ Security Analysis

#### 10. Link Classification & Prioritization
- **Automatic categorization**: Authentication, Admin, API, Upload, Config, Debug
- **Priority levels**: Critical, High, Medium, Low
- **Smart filtering** by category and priority

```bash
# Classify links with minimum priority
xnLinkFinder -i target.com --classify --min-priority high
```

#### 11. Vulnerability Hints
- **IDOR detection** (numeric IDs, UUIDs in URLs)
- **SSRF patterns** (URL parameters)
- **LFI/Path Traversal** indicators
- **SQL injection** potential
- **XSS vectors**
- **Debug/Test endpoint** detection
- **Open redirect** patterns

```bash
# Enable vulnerability analysis
xnLinkFinder -i target.com --vuln-hints
```

#### 12. Secrets Detection
- **API keys**: AWS, Google, GitHub, Stripe, Twilio, SendGrid
- **Tokens**: JWT, OAuth, Access tokens
- **Credentials**: Passwords, private keys, connection strings
- **Severity classification**: Critical, High, Medium, Low

```bash
# Enable secrets detection
xnLinkFinder -i target.com --detect-secrets
```

### 📊 Output Formats

#### 13. Rich Output Formats
- **JSON**: Full metadata with status codes, timestamps, categories
- **HTML**: Interactive report with filtering and sorting
- **Markdown**: Documentation-friendly format
- **SARIF**: Security tooling integration (for CI/CD)

```bash
# Generate multiple output formats
xnLinkFinder -i target.com --output-json results.json --output-html report.html --output-sarif results.sarif
```

### 🔌 Plugin System

#### 14. Extensible Plugin Architecture
- **Base plugin classes** for custom parsers, filters, and processors
- **Dynamic plugin loading** from plugins directory
- **Easy to extend** with custom functionality

```python
# Example custom parser plugin
from xnLinkFinder.plugins.base import LinkParserPlugin

class MyCustomParser(LinkParserPlugin):
    def extract_links(self, content, source=None):
        # Custom link extraction logic
        return found_links
```

### ⚙️ Configuration Profiles

#### 15. Scan Profiles
- **Aggressive**: Maximum coverage and depth
- **Stealth**: Low and slow to avoid detection
- **Quick**: Fast scanning with essential features

```bash
# Use a scan profile
xnLinkFinder -i target.com --profile aggressive

# Load custom profile
xnLinkFinder -i target.com --profile /path/to/custom.yml
```

### 🎨 Terminal UI

#### 16. Rich Terminal Interface
- **Real-time progress** visualization
- **Interactive tables** with rich formatting
- **Color-coded** severity levels
- **Statistics dashboard**

```bash
# Enable rich UI
xnLinkFinder -i target.com --rich-ui
```

### 🐳 Docker Support

#### 17. Docker Deployment
```bash
# Build and run with Docker
docker build -t xnlinkfinder-z .
docker run -v $(pwd)/output:/output xnlinkfinder-z -i target.com -o /output/results.txt

# Use docker-compose
docker-compose up
```

### 🤖 CI/CD Integration

#### 18. GitHub Actions Workflows
- **Automated testing** on multiple Python versions
- **Security scanning** with Bandit, Safety, CodeQL
- **Scheduled scans** with result comparison

Example workflow:
```yaml
- name: Run xnLinkFinder scan
  run: |
    xnLinkFinder -i ${{ secrets.TARGET_URL }} \
      --output-sarif results.sarif \
      --classify --vuln-hints
    
- name: Upload to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: results.sarif
```

## 📦 Advanced Usage Examples

### Comprehensive Security Scan
```bash
xnLinkFinder -i target.com \
  --profile aggressive \
  --use-browser --heap-extract \
  --discover-graphql --discover-openapi \
  --parse-sourcemaps --detect-cloud-services \
  --classify --vuln-hints --detect-secrets \
  --output-json results.json \
  --output-html report.html \
  --output-sarif security.sarif \
  --use-database --db-path scan.db
```

### Stealth Reconnaissance
```bash
xnLinkFinder -i target.com \
  --profile stealth \
  --rate-limit 2 \
  --user-agent custom \
  --proxy http://127.0.0.1:8080 \
  --classify --min-priority high
```

### API Discovery & Analysis
```bash
xnLinkFinder -i target.com \
  --discover-graphql \
  --discover-openapi \
  --discover-websockets \
  --regex-after "/api/" \
  --output-json api-endpoints.json
```

### Continuous Monitoring
```bash
# Initial scan
xnLinkFinder -i target.com --use-database --db-path baseline.db

# Weekly scans - only new findings
xnLinkFinder -i target.com --use-database --db-path baseline.db --diff-mode
```

## 🔧 Configuration

### Profile Configuration (YAML)
```yaml
# custom-profile.yml
scan:
  name: "Custom Scan"
  description: "Custom configuration"

requests:
  timeout: 30
  retries: 3
  max_concurrent: 25
  rate_limit: 5

discovery:
  graphql: true
  openapi: true
  sourcemaps: true
  cloud_services: true

analysis:
  classify_links: true
  vulnerability_hints: true
  secrets_detection: true

output:
  formats:
    - json
    - html
  include_metadata: true
```

## 🎯 Performance Optimization

### Memory Efficiency
- **Streaming processing** for large files
- **Bloom filters** for efficient deduplication
- **Generator-based** link yielding
- **Configurable memory threshold**

### Speed Optimization
- **Async I/O** for parallel processing
- **Connection pooling** with keep-alive
- **DNS caching** to reduce lookups
- **Smart resource caching**

## 📚 API Usage

All modules can be used programmatically:

```python
from xnLinkFinder.core.async_crawler import AsyncCrawler
from xnLinkFinder.discovery.graphql import GraphQLDiscovery
from xnLinkFinder.analysis.classifier import LinkClassifier
from xnLinkFinder.analysis.secrets import SecretsDetector

# Async crawling
async with AsyncCrawler(max_concurrent=50) as crawler:
    results = await crawler.fetch_many(urls)

# GraphQL discovery
discovery = GraphQLDiscovery("https://api.example.com")
results = await discovery.full_discovery()

# Link classification
classifier = LinkClassifier()
classifications = classifier.classify_batch(urls)

# Secrets detection
detector = SecretsDetector()
secrets = detector.scan_content(content)
```

## 🤝 Contributing

Contributions are welcome! The modular architecture makes it easy to:
- Add new discovery methods
- Create custom parsers
- Implement new output formats
- Extend analysis capabilities

## 📄 License

Same as original xnLinkFinder

## 🙏 Credits

- Original xnLinkFinder by [@xnl-h4ck3r](https://github.com/xnl-h4ck3r)
- Enhanced version by [@ZeidMahmoud](https://github.com/ZeidMahmoud)
