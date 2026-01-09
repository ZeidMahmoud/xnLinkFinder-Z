#!/usr/bin/env python3
"""
Demo script showcasing new xnLinkFinder-Z features.

This script demonstrates the key new features added to xnLinkFinder-Z.
"""

def demo_ai_features():
    """Demonstrate AI/ML features."""
    print("\n" + "="*60)
    print("🤖 AI & MACHINE LEARNING FEATURES")
    print("="*60)
    
    # Vulnerability Prediction
    print("\n1. Vulnerability Prediction:")
    from xnLinkFinder.ai.vulnerability_predictor import predict_vulnerability
    
    test_endpoints = [
        '/admin/config',
        '/api/users',
        '/test/debug.php',
        '/uploads/file.php'
    ]
    
    for endpoint in test_endpoints:
        result = predict_vulnerability(endpoint)
        print(f"   {endpoint}")
        print(f"   └─ Probability: {result['probability']}% | Severity: {result['severity']}")
    
    # Smart Deduplication
    print("\n2. Smart Deduplication:")
    from xnLinkFinder.ai.smart_dedup import SmartDeduplicator
    
    endpoints = [
        '/api/v1/users',
        '/api/v2/users',
        '/api/v1/users/123',
        '/api/v1/users/456',
        '/api/v1/posts',
        '/completely/different/path'
    ]
    
    deduplicator = SmartDeduplicator(use_semantic=False)
    unique, metadata = deduplicator.deduplicate(endpoints)
    
    print(f"   Original: {metadata['original_count']} endpoints")
    print(f"   Unique: {metadata['unique_count']} endpoints")
    print(f"   Reduction: {metadata['reduction_percentage']}%")
    
    # Natural Language Query
    print("\n3. Natural Language Queries:")
    from xnLinkFinder.ai.nlp_query import NLPQueryEngine
    
    engine = NLPQueryEngine()
    sample_endpoints = [
        '/admin/users',
        '/admin/config',
        '/api/login',
        '/api/logout',
        '/public/home',
        '/user/profile'
    ]
    engine.load_endpoints(sample_endpoints)
    
    queries = [
        "find all admin endpoints",
        "show me API endpoints"
    ]
    
    for query in queries:
        result = engine.query(query)
        print(f"   Query: '{query}'")
        print(f"   └─ Found: {result['count']} endpoints")
    
    # Anomaly Detection
    print("\n4. Anomaly Detection:")
    from xnLinkFinder.ai.anomaly_detector import AnomalyDetector
    
    detector = AnomalyDetector()
    suspicious_endpoints = [
        '/admin/debug',
        '/config.bak',
        '/test.php?cmd=ls',
        '/.git/config',
        '/backup.sql'
    ]
    
    anomalies = detector.detect_all(suspicious_endpoints)
    total_anomalies = sum(len(findings) for findings in anomalies.values())
    print(f"   Detected {total_anomalies} anomalies across {len(suspicious_endpoints)} endpoints")
    for category, findings in anomalies.items():
        if findings:
            print(f"   └─ {category}: {len(findings)} findings")


def demo_bugbounty_features():
    """Demonstrate bug bounty features."""
    print("\n" + "="*60)
    print("💰 BUG BOUNTY INTEGRATION")
    print("="*60)
    
    # Scope Validation
    print("\n1. Scope Validation:")
    from xnLinkFinder.bugbounty.scope_validator import ScopeValidator
    
    validator = ScopeValidator()
    scope_definition = [
        'example.com',
        '*.example.com',
        '!admin.example.com'
    ]
    
    parsed_scope = validator.parse_scope(scope_definition)
    
    test_targets = [
        'app.example.com',
        'admin.example.com',
        'other.com'
    ]
    
    for target in test_targets:
        result = validator.is_in_scope(target, parsed_scope)
        status = "✅ IN SCOPE" if result['in_scope'] else "❌ OUT OF SCOPE"
        print(f"   {target}: {status}")
    
    # Report Generation
    print("\n2. Report Generation:")
    from xnLinkFinder.bugbounty.report_generator import ReportGenerator
    
    generator = ReportGenerator()
    vulnerability = {
        'title': 'Cross-Site Scripting (XSS) Vulnerability',
        'severity': 'high',
        'asset': 'https://example.com/search',
        'description': 'Reflected XSS in search parameter',
        'impact': 'Attackers can execute arbitrary JavaScript in victim browsers',
        'steps_to_reproduce': [
            'Navigate to https://example.com/search',
            'Enter <script>alert(1)</script> in search box',
            'Submit form and observe XSS execution'
        ],
        'poc': 'https://example.com/search?q=<script>alert(1)</script>',
        'remediation': 'Implement proper output encoding and Content Security Policy'
    }
    
    report = generator.generate_report(vulnerability, template='generic')
    print(f"   Generated report: {len(report)} characters")
    print(f"   Available templates: generic, hackerone, bugcrowd")
    
    # CVSS Calculation
    print("\n3. CVSS Score Calculation:")
    cvss_metrics = {
        'attack_vector': 'network',
        'attack_complexity': 'low',
        'privileges_required': 'none',
        'user_interaction': 'required',
        'confidentiality': 'low',
        'integrity': 'low',
        'availability': 'none'
    }
    
    cvss_result = generator.calculate_cvss_score(cvss_metrics)
    print(f"   CVSS Score: {cvss_result['score']}/10.0")
    print(f"   Severity: {cvss_result['severity']}")
    print(f"   Vector: {cvss_result['vector']}")
    
    # Payout Estimation
    print("\n4. Payout Estimation:")
    from xnLinkFinder.bugbounty.payout_estimator import PayoutEstimator
    
    estimator = PayoutEstimator()
    estimate = estimator.estimate_payout(
        severity='high',
        vulnerability_type='xss',
        program_type='public'
    )
    
    payout = estimate['estimated_payout']
    print(f"   Estimated payout: ${payout['min']} - ${payout['max']}")
    print(f"   Average: ${payout['average']} {payout['currency']}")


def demo_gamification():
    """Demonstrate gamification features."""
    print("\n" + "="*60)
    print("🎮 GAMIFICATION & ACHIEVEMENTS")
    print("="*60)
    
    import tempfile
    import shutil
    from xnLinkFinder.gamification.achievements import AchievementSystem
    
    # Create temporary directory for demo
    temp_dir = tempfile.mkdtemp()
    
    try:
        system = AchievementSystem(data_dir=temp_dir)
        
        print("\n1. Initial Progress:")
        progress = system.get_progress()
        print(f"   Achievements unlocked: {progress['unlocked']}/{progress['total']}")
        print(f"   Points: {progress['points']}/{progress['max_points']}")
        
        print("\n2. Simulating Activity...")
        # Simulate discovering endpoints
        system.update_stats(total_endpoints_discovered=1)
        print("   ✅ Discovered first endpoint")
        
        system.update_stats(total_endpoints_discovered=99)
        print("   ✅ Discovered 100 endpoints total")
        
        system.update_stats(critical_findings=1)
        print("   ✅ Found critical vulnerability")
        
        print("\n3. Updated Progress:")
        progress = system.get_progress()
        print(f"   Achievements unlocked: {progress['unlocked']}/{progress['total']}")
        print(f"   Points: {progress['points']}/{progress['max_points']}")
        print(f"   Completion: {progress['percentage']}%")
        
        print("\n4. Unlocked Achievements:")
        for ach_id, ach_data in progress['achievements'].items():
            if ach_data['unlocked']:
                print(f"   ✅ {ach_data['name']} ({ach_data['points']} pts)")
    
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def demo_recon_features():
    """Demonstrate reconnaissance features."""
    print("\n" + "="*60)
    print("🔍 ADVANCED RECONNAISSANCE")
    print("="*60)
    
    print("\n1. Technology Fingerprinting:")
    print("   Available capabilities:")
    print("   • CMS detection (WordPress, Drupal, Joomla)")
    print("   • Framework identification (React, Vue, Angular)")
    print("   • Server detection (Apache, Nginx, IIS)")
    print("   • JavaScript library detection")
    print("   • Security header analysis")
    
    print("\n2. WAF Detection:")
    print("   Supported WAFs:")
    wafs = ['Cloudflare', 'AWS WAF', 'Akamai', 'Imperva', 'Sucuri', 
            'ModSecurity', 'F5 BIG-IP', 'Barracuda']
    for waf in wafs:
        print(f"   • {waf}")
    
    print("\n3. DNS Intelligence:")
    print("   Features:")
    print("   • Zone transfer detection (AXFR)")
    print("   • Record enumeration (A, AAAA, MX, NS, TXT, SOA)")
    print("   • DNSSEC validation")
    print("   • Subdomain brute-forcing")
    
    print("\n4. Certificate Transparency:")
    print("   • Subdomain discovery from certificates")
    print("   • Historical certificate analysis")
    print("   • Wildcard detection")
    print("   • Infrastructure pattern identification")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 xnLinkFinder-Z NEW FEATURES DEMO")
    print("="*60)
    print("\nThis demo showcases the new features added to xnLinkFinder-Z.")
    print("All features are production-ready with full error handling.")
    
    try:
        demo_ai_features()
        demo_bugbounty_features()
        demo_gamification()
        demo_recon_features()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE")
        print("="*60)
        print("\nFor more information, see:")
        print("• NEW_FEATURES.md - Comprehensive feature documentation")
        print("• tests/ - Unit tests for all new modules")
        print("• xnLinkFinder/ai/ - AI and ML modules")
        print("• xnLinkFinder/bugbounty/ - Bug bounty integration")
        print("• xnLinkFinder/recon/ - Reconnaissance modules")
        print("• xnLinkFinder/gamification/ - Gamification features")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
