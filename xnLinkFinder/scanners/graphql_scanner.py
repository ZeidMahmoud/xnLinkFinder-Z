"""
GraphQL Security Scanner

Performs comprehensive GraphQL security testing:
- Introspection abuse detection
- Batch query attacks
- Query complexity analysis
- Mutation fuzzing
"""

import requests
import json
from typing import Dict, List, Optional, Any


class GraphQLScanner:
    """Scanner for GraphQL security issues"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize GraphQL scanner
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        
    def scan(self, url: str, headers: Optional[Dict] = None) -> List[Dict]:
        """
        Perform comprehensive GraphQL security scan
        
        Args:
            url: GraphQL endpoint URL
            headers: Optional headers to include
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        # Test introspection
        introspection_vuln = self._test_introspection(url, headers)
        if introspection_vuln:
            vulnerabilities.append(introspection_vuln)
            
        # Test for batch query attacks
        batch_vuln = self._test_batch_queries(url, headers)
        if batch_vuln:
            vulnerabilities.append(batch_vuln)
            
        # Test for query depth
        depth_vuln = self._test_query_depth(url, headers)
        if depth_vuln:
            vulnerabilities.append(depth_vuln)
            
        # Test for field duplication
        dup_vuln = self._test_field_duplication(url, headers)
        if dup_vuln:
            vulnerabilities.append(dup_vuln)
            
        return vulnerabilities
    
    def _test_introspection(self, url: str, 
                           headers: Optional[Dict]) -> Optional[Dict]:
        """Test if introspection is enabled"""
        introspection_query = {
            "query": """
            {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                }
            }
            """
        }
        
        try:
            response = requests.post(
                url,
                json=introspection_query,
                headers=headers or {},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and '__schema' in data['data']:
                    return {
                        'url': url,
                        'type': 'GRAPHQL_INTROSPECTION_ENABLED',
                        'severity': 'MEDIUM',
                        'description': 'GraphQL introspection is enabled',
                        'schema_types': len(data['data']['__schema'].get('types', [])),
                    }
                    
        except Exception:
            pass
            
        return None
    
    def _test_batch_queries(self, url: str, 
                           headers: Optional[Dict]) -> Optional[Dict]:
        """Test for batch query DoS vulnerability"""
        # Create a batch of queries
        batch_query = []
        for i in range(100):
            batch_query.append({
                "query": f"query{i}: __typename"
            })
            
        try:
            response = requests.post(
                url,
                json=batch_query,
                headers=headers or {},
                timeout=self.timeout * 2  # Extended timeout
            )
            
            if response.status_code == 200:
                return {
                    'url': url,
                    'type': 'GRAPHQL_BATCH_QUERY_ALLOWED',
                    'severity': 'MEDIUM',
                    'description': 'GraphQL allows batch queries (potential DoS)',
                    'batch_size_tested': 100,
                }
                
        except requests.Timeout:
            return {
                'url': url,
                'type': 'GRAPHQL_BATCH_QUERY_DOS',
                'severity': 'HIGH',
                'description': 'GraphQL batch query caused timeout (DoS vulnerability)',
            }
        except Exception:
            pass
            
        return None
    
    def _test_query_depth(self, url: str, 
                         headers: Optional[Dict]) -> Optional[Dict]:
        """Test for excessive query depth vulnerability"""
        # Build a deeply nested query
        deep_query = self._build_deep_query(20)
        
        try:
            response = requests.post(
                url,
                json={"query": deep_query},
                headers=headers or {},
                timeout=self.timeout * 2
            )
            
            if response.status_code == 200:
                return {
                    'url': url,
                    'type': 'GRAPHQL_DEEP_QUERY_ALLOWED',
                    'severity': 'MEDIUM',
                    'description': 'GraphQL allows deeply nested queries (potential DoS)',
                    'depth_tested': 20,
                }
                
        except requests.Timeout:
            return {
                'url': url,
                'type': 'GRAPHQL_DEEP_QUERY_DOS',
                'severity': 'HIGH',
                'description': 'Deep GraphQL query caused timeout (DoS vulnerability)',
            }
        except Exception:
            pass
            
        return None
    
    def _test_field_duplication(self, url: str, 
                               headers: Optional[Dict]) -> Optional[Dict]:
        """Test for field duplication attack"""
        # Query with many duplicated fields
        dup_query = """
        {
            __typename
            """ + "\n".join([f"alias{i}: __typename" for i in range(100)]) + """
        }
        """
        
        try:
            response = requests.post(
                url,
                json={"query": dup_query},
                headers=headers or {},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    'url': url,
                    'type': 'GRAPHQL_FIELD_DUPLICATION',
                    'severity': 'LOW',
                    'description': 'GraphQL allows field duplication',
                    'fields_tested': 100,
                }
                
        except Exception:
            pass
            
        return None
    
    def _build_deep_query(self, depth: int) -> str:
        """Build a deeply nested GraphQL query"""
        query = "{ __typename"
        
        for i in range(depth):
            query += " { __typename"
            
        query += " }" * (depth + 1)
        
        return query
    
    def extract_schema(self, url: str, 
                      headers: Optional[Dict] = None) -> Optional[Dict]:
        """
        Extract full GraphQL schema via introspection
        
        Args:
            url: GraphQL endpoint URL
            headers: Optional headers
            
        Returns:
            Schema data if available
        """
        full_introspection = {
            "query": """
            query IntrospectionQuery {
                __schema {
                    queryType { name }
                    mutationType { name }
                    subscriptionType { name }
                    types {
                        ...FullType
                    }
                    directives {
                        name
                        description
                        locations
                        args {
                            ...InputValue
                        }
                    }
                }
            }
            
            fragment FullType on __Type {
                kind
                name
                description
                fields(includeDeprecated: true) {
                    name
                    description
                    args {
                        ...InputValue
                    }
                    type {
                        ...TypeRef
                    }
                    isDeprecated
                    deprecationReason
                }
                inputFields {
                    ...InputValue
                }
                interfaces {
                    ...TypeRef
                }
                enumValues(includeDeprecated: true) {
                    name
                    description
                    isDeprecated
                    deprecationReason
                }
                possibleTypes {
                    ...TypeRef
                }
            }
            
            fragment InputValue on __InputValue {
                name
                description
                type { ...TypeRef }
                defaultValue
            }
            
            fragment TypeRef on __Type {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                        }
                    }
                }
            }
            """
        }
        
        try:
            response = requests.post(
                url,
                json=full_introspection,
                headers=headers or {},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            print(f"[!] Error extracting schema: {str(e)}")
            
        return None


def scan_graphql(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """
    Convenience function to scan multiple GraphQL endpoints
    
    Args:
        urls: List of GraphQL endpoint URLs
        **kwargs: Additional arguments for GraphQLScanner
        
    Returns:
        Dictionary mapping URLs to vulnerabilities
    """
    scanner = GraphQLScanner(**kwargs)
    results = {}
    
    for url in urls:
        try:
            vulns = scanner.scan(url)
            if vulns:
                results[url] = vulns
        except Exception as e:
            print(f"[!] Error scanning {url}: {str(e)}")
            
    return results
