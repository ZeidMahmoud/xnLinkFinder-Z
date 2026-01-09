# Welcome to xnLinkFinder-Z

**The most advanced endpoint discovery and security testing tool for bug bounty hunters and penetration testers.**

---

## 🎯 What is xnLinkFinder-Z?

xnLinkFinder-Z is a powerful Python tool designed to discover endpoints, parameters, and create target-specific wordlists. It's been enhanced with 40+ advanced features to become the ultimate reconnaissance and security testing tool.

## ✨ Key Features

### 🔍 Discovery Engine
- **Smart Endpoint Discovery** - Find hidden endpoints and parameters
- **Multi-Source Intelligence** - robots.txt, sitemap.xml, security.txt, .well-known/
- **JavaScript Analysis** - Deep analysis of JS files for API endpoints
- **Spider Mode** - Recursive site crawling with depth control

### 🎨 Visualization
- **Link Relationship Graphs** - Visual representation of endpoint relationships
- **Multiple Export Formats** - HTML, DOT, GEXF, GraphML, JSON
- **Interactive Dashboards** - Real-time metrics and statistics

### 🧪 Security Testing
- **Nuclei Template Generator** - Auto-generate templates for SQLi, XSS, IDOR, etc.
- **40+ Security Scanners** - Comprehensive vulnerability detection
- **Smart Authentication** - OAuth, SAML, JWT support

### 🚀 Presets & Automation
- **7 Smart Presets** - Optimized for bug bounty, pentest, recon, and more
- **Shell Completions** - Bash and Zsh autocomplete
- **Multi-Language Support** - 8+ languages (English, Spanish, French, etc.)

## 🏃 Quick Start

### Installation

```bash
# Install from PyPI
pip install xnlinkfinder

# Or install from source
git clone https://github.com/ZeidMahmoud/xnLinkFinder-Z.git
cd xnLinkFinder-Z
pip install -e .
```

### Basic Usage

```bash
# Simple scan
xnLinkFinder -i https://example.com

# Bug bounty preset
xnLinkFinder -i https://example.com --preset bug_bounty

# Full featured scan
xnLinkFinder -i https://example.com \
  --auto-scope \
  --parse-robots \
  --parse-sitemap \
  --generate-nuclei \
  --graph --graph-format html \
  -o results.txt
```

## 📚 Documentation

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Quick Start**

    ---

    Get up and running in 5 minutes

    [:octicons-arrow-right-24: Quick Start Guide](quickstart.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Configure xnLinkFinder for your needs

    [:octicons-arrow-right-24: Configuration](configuration.md)

-   :material-palette:{ .lg .middle } **Features**

    ---

    Explore all features and capabilities

    [:octicons-arrow-right-24: Feature Overview](features/overview.md)

-   :material-school:{ .lg .middle } **Tutorials**

    ---

    Step-by-step guides for common scenarios

    [:octicons-arrow-right-24: Tutorials](tutorials/bug-bounty.md)

</div>

## 🎯 Use Cases

### Bug Bounty Hunting
Perfect for discovering hidden endpoints and parameters in web applications. Use the `bug_bounty` preset for optimal results.

### Penetration Testing
Comprehensive scanning with all security checks enabled. Use the `pentest` preset for thorough assessments.

### API Discovery
Specialized in finding API endpoints, GraphQL schemas, and REST APIs. Use the `api_hunting` preset.

### Reconnaissance
Quick and quiet information gathering. Use the `recon` preset for passive discovery.

## 🌟 What's New

### Version 7.18+ Features
- ✅ Nuclei Template Generator
- ✅ Scope Intelligence Engine
- ✅ Link Relationship Graphs
- ✅ 7 Smart Presets
- ✅ Shell Completions
- ✅ Multi-Language Support
- ✅ Metrics Dashboard
- ✅ 40+ Security Scanners

See the [Changelog](../CHANGELOG.md) for detailed release notes.

## 🤝 Community

- **GitHub**: [Issues](https://github.com/ZeidMahmoud/xnLinkFinder-Z/issues) | [Discussions](https://github.com/ZeidMahmoud/xnLinkFinder-Z/discussions)
- **Contributing**: See our [Contributing Guide](../CONTRIBUTING.md)
- **Security**: Report vulnerabilities via our [Security Policy](../SECURITY.md)

## 📄 License

xnLinkFinder-Z is released under the MIT License. See [LICENSE](https://github.com/ZeidMahmoud/xnLinkFinder-Z/blob/main/LICENSE) for details.

---

**Ready to get started?** Check out the [Quick Start Guide](quickstart.md) or view the [Cheat Sheet](CHEATSHEET.md) for common commands!
