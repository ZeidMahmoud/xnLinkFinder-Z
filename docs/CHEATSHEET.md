# xnLinkFinder-Z Cheat Sheet

Quick reference for common commands and usage patterns.

## 📦 Installation

```bash
# Install from PyPI
pip install xnlinkfinder

# Install with all features
pip install xnlinkfinder[all]

# Install shell completions
# Bash
echo 'source /path/to/completions/xnlinkfinder.bash' >> ~/.bashrc

# Zsh
echo 'source /path/to/completions/xnlinkfinder.zsh' >> ~/.zshrc
```

## 🚀 Quick Start

```bash
# Basic scan
xnLinkFinder -i https://example.com

# Scan with output
xnLinkFinder -i https://example.com -o results.txt

# Use a preset
xnLinkFinder -i https://example.com --preset bug_bounty
```

## 🎯 Presets

```bash
# Bug bounty hunting
xnLinkFinder -i target.com --preset bug_bounty

# Penetration testing
xnLinkFinder -i target.com --preset pentest

# Quick reconnaissance
xnLinkFinder -i target.com --preset recon

# Stealth mode
xnLinkFinder -i target.com --preset stealth

# Aggressive scan
xnLinkFinder -i target.com --preset aggressive

# API endpoint hunting
xnLinkFinder -i target.com --preset api_hunting

# JavaScript analysis
xnLinkFinder -i target.com --preset js_analysis
```

## 🔍 Discovery Options

```bash
# Auto-detect scope
xnLinkFinder -i target.com --auto-scope

# Parse robots.txt
xnLinkFinder -i target.com --parse-robots

# Parse sitemap.xml
xnLinkFinder -i target.com --parse-sitemap

# Spider mode with depth
xnLinkFinder -i target.com --spider --spider-depth 5
```

## 🎨 Visualization

```bash
# Generate HTML graph
xnLinkFinder -i target.com --graph --graph-format html

# Generate DOT format
xnLinkFinder -i target.com --graph --graph-format dot

# Generate JSON graph
xnLinkFinder -i target.com --graph --graph-format json
```

## 🧪 Template Generation

```bash
# Generate Nuclei templates
xnLinkFinder -i target.com --generate-nuclei --nuclei-output ./templates/

# Generate all template types
xnLinkFinder -i target.com --generate-nuclei
```

## 📊 Output Options

```bash
# Stream output in real-time
xnLinkFinder -i target.com --stream

# Save to multiple files
xnLinkFinder -i target.com \
  -o endpoints.txt \
  -op parameters.txt \
  -owl wordlist.txt \
  -oo out-of-scope.txt

# CLI output only
xnLinkFinder -i target.com -o cli
```

## 🌍 Multi-language

```bash
# Spanish
xnLinkFinder -i target.com --lang es

# French
xnLinkFinder -i target.com --lang fr

# Chinese
xnLinkFinder -i target.com --lang zh
```

## 📈 Metrics & Monitoring

```bash
# Enable metrics collection
xnLinkFinder -i target.com --metrics

# Launch web dashboard
xnLinkFinder -i target.com --dashboard
```

## 🔧 Advanced Options

```bash
# Set depth and threads
xnLinkFinder -i target.com -d 5 -p 10

# Use custom headers
xnLinkFinder -i target.com -H "Authorization: Bearer token"

# Use cookies
xnLinkFinder -i target.com -c "session=abc123"

# Set timeout
xnLinkFinder -i target.com -t 30

# Use custom config
xnLinkFinder -i target.com --config myconfig.yml
```

## 🎭 Input Sources

```bash
# Single URL
xnLinkFinder -i https://example.com

# File with URLs
xnLinkFinder -i urls.txt

# Directory of files
xnLinkFinder -i /path/to/files/

# Burp XML export
xnLinkFinder -i burp_export.xml

# HAR file
xnLinkFinder -i capture.har

# Stdin
cat urls.txt | xnLinkFinder -i -
```

## 🔐 Scope Control

```bash
# Scope prefix
xnLinkFinder -i target.com -sp https://target.com

# Scope prefix only
xnLinkFinder -i target.com -spo https://target.com/app

# Scope filter (regex)
xnLinkFinder -i target.com -sf ".*\.target\.com"

# Exclude patterns
xnLinkFinder -i target.com -x logout,signout
```

## 🚫 Filtering

```bash
# Exclude file extensions
xnLinkFinder -i target.com -x .jpg,.png,.css

# Include only specific extensions
xnLinkFinder -i target.com --include-only .php,.asp

# Skip 403 responses
xnLinkFinder -i target.com -s403

# Skip 429 responses
xnLinkFinder -i target.com -s429
```

## 💡 Common Patterns

### API Hunting
```bash
xnLinkFinder -i https://api.example.com \
  --preset api_hunting \
  -op api_params.txt \
  --generate-nuclei \
  --graph --graph-format html
```

### Bug Bounty Recon
```bash
xnLinkFinder -i https://target.com \
  --preset bug_bounty \
  --auto-scope \
  --parse-robots \
  --parse-sitemap \
  -o findings.txt \
  --metrics
```

### Pentest Full Scan
```bash
xnLinkFinder -i https://target.com \
  --preset pentest \
  --spider --spider-depth 5 \
  -d 10 -p 20 \
  -o results.txt \
  --generate-nuclei \
  --graph --graph-format html
```

### Stealth Scan
```bash
xnLinkFinder -i https://target.com \
  --preset stealth \
  -d 2 -p 2 \
  -t 60 \
  --stream
```

## 🐛 Debugging

```bash
# Verbose output
xnLinkFinder -i target.com -v

# Very verbose
xnLinkFinder -i target.com -vv

# No banner
xnLinkFinder -i target.com -nb
```

## 📚 Help & Info

```bash
# Show help
xnLinkFinder --help

# Show version
xnLinkFinder --version

# Validate config
xnLinkFinder --validate-config config.yml
```

## 🔄 Integration Examples

### With Nuclei
```bash
# Generate and run templates
xnLinkFinder -i target.com --generate-nuclei --nuclei-output ./templates/
nuclei -t ./templates/ -l urls.txt
```

### With FFUF
```bash
# Generate wordlist for fuzzing
xnLinkFinder -i target.com -owl wordlist.txt
ffuf -w wordlist.txt -u https://target.com/FUZZ
```

### With HTTPx
```bash
# Probe discovered endpoints
xnLinkFinder -i target.com -o endpoints.txt
httpx -l endpoints.txt -status-code -title
```

## 💾 Configuration File Example

```yaml
# config.yml
version: 1
settings:
  timeout: 30
  max_depth: 5
  threads: 10
  
filters:
  exclude_extensions:
    - .jpg
    - .png
    - .css
  
scope:
  prefix: "https://target.com"
  
output:
  save_all: true
  deduplicate: true
```

Use with: `xnLinkFinder -i target.com --config config.yml`

## ⚡ Performance Tips

1. **Use appropriate presets** - They're optimized for specific use cases
2. **Adjust thread count** - More threads = faster but more aggressive
3. **Set reasonable depth** - Deeper = more thorough but slower
4. **Use --stream** - See results immediately
5. **Filter early** - Use scope filters to reduce noise
6. **Cache results** - Save intermediate results for later analysis

## 🆘 Troubleshooting

```bash
# Connection issues
xnLinkFinder -i target.com -t 60 --insecure

# Rate limiting
xnLinkFinder -i target.com -p 2 -t 30 --preset stealth

# Memory issues
xnLinkFinder -i target.com -d 3 -p 5

# SSL errors
xnLinkFinder -i target.com --insecure
```

---

For more detailed information, see the [full documentation](README.md).
