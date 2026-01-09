# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The following versions are currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 7.x.x   | :white_check_mark: |
| < 7.0   | :x:                |

## Reporting a Vulnerability

The xnLinkFinder-Z team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report a Security Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to https://github.com/ZeidMahmoud/xnLinkFinder-Z/security/advisories
   - Click "Report a vulnerability"
   - Fill in the details

2. **Email**
   - Send an email to the maintainers
   - Use "SECURITY" in the subject line
   - Include detailed information about the vulnerability

### What to Include in Your Report

Please include the following information in your report:

* **Type of vulnerability** (e.g., SQL injection, XSS, RCE, etc.)
* **Full path of source file(s)** related to the vulnerability
* **Location of the affected source code** (tag/branch/commit or direct URL)
* **Special configuration required** to reproduce the issue
* **Step-by-step instructions** to reproduce the issue
* **Proof-of-concept or exploit code** (if possible)
* **Impact of the issue**, including how an attacker might exploit it

### Response Timeline

* **Initial Response**: Within 48 hours
* **Status Update**: Within 7 days
* **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Within 90 days

### What to Expect

After you submit a report, here's what happens:

1. **Acknowledgment**: We'll acknowledge receipt within 48 hours
2. **Investigation**: We'll investigate and validate the issue
3. **Communication**: We'll keep you updated on our progress
4. **Fix Development**: We'll develop and test a fix
5. **Disclosure**: We'll coordinate disclosure timing with you
6. **Credit**: You'll be credited in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using xnLinkFinder-Z, please follow these security best practices:

### 1. Keep Software Updated
```bash
pip install --upgrade xnlinkfinder
```

### 2. Use Virtual Environments
```bash
python3 -m venv venv
source venv/bin/activate
pip install xnlinkfinder
```

### 3. Secure Your Configuration
* Don't commit config files with secrets to version control
* Use environment variables for sensitive data
* Restrict file permissions on config files:
  ```bash
  chmod 600 config.yml
  ```

### 4. Network Security
* Be cautious when scanning untrusted targets
* Use appropriate rate limiting
* Consider using a VPN or proxy for sensitive scans

### 5. Output Security
* Be careful with output files containing sensitive data
* Don't commit scan results to public repositories
* Use encrypted storage for sensitive findings

### 6. API Security
* Use strong authentication tokens
* Rotate API keys regularly
* Implement rate limiting
* Use HTTPS for API communications

## Known Security Considerations

### 1. Third-Party Dependencies
xnLinkFinder-Z relies on several third-party libraries. We regularly update these dependencies to patch known vulnerabilities. You can check for vulnerable dependencies using:

```bash
pip install safety
safety check -r requirements.txt
```

### 2. Command Injection
When using xnLinkFinder-Z programmatically, avoid passing unsanitized user input directly to system calls or shell commands.

### 3. Path Traversal
Be cautious when specifying input/output file paths. The tool includes protections, but always validate paths in your integrations.

### 4. Resource Exhaustion
* Set appropriate limits for concurrent connections
* Use timeouts to prevent hanging requests
* Monitor memory usage for large scans

## Security Scanning

We use automated security scanning tools:

* **Bandit**: Python security linter
* **Safety**: Dependency vulnerability scanner
* **CodeQL**: Semantic code analysis
* **Snyk**: Continuous vulnerability monitoring

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible
5. Publicly disclose the vulnerability after the fix is released

## Comments on This Policy

If you have suggestions on how this process could be improved, please submit a pull request or open an issue to discuss.

## Hall of Fame

We'd like to thank the following people for responsibly disclosing security issues:

* *Your name could be here!*

## Additional Resources

* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* [CWE Top 25](https://cwe.mitre.org/top25/)
* [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security.html)

---

Last updated: 2026-01-09
