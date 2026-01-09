"""
GraphQL introspection and schema discovery module.
Automatically detects and queries GraphQL endpoints to discover available queries, mutations, and types.
"""

import json
from typing import Dict, List, Optional, Set
import asyncio


# GraphQL introspection query
INTROSPECTION_QUERY = """
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
        ofType {
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
      }
    }
  }
}
"""


class GraphQLDiscovery:
    """GraphQL endpoint discovery and schema introspection."""

    # Common GraphQL endpoint paths
    COMMON_GRAPHQL_PATHS = [
        "/graphql",
        "/api/graphql",
        "/v1/graphql",
        "/v2/graphql",
        "/query",
        "/api/query",
        "/gql",
        "/api/gql",
    ]

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize GraphQL discovery.

        Args:
            base_url: Base URL of the target
            headers: Optional HTTP headers for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.discovered_endpoints: Set[str] = set()
        self.schemas: Dict[str, Dict] = {}

    async def discover_endpoints(self, custom_paths: Optional[List[str]] = None) -> List[str]:
        """
        Discover GraphQL endpoints.

        Args:
            custom_paths: Additional paths to check

        Returns:
            List of discovered GraphQL endpoints
        """
        paths_to_check = self.COMMON_GRAPHQL_PATHS.copy()
        if custom_paths:
            paths_to_check.extend(custom_paths)

        # Check each potential path
        for path in paths_to_check:
            url = f"{self.base_url}{path}"
            if await self._is_graphql_endpoint(url):
                self.discovered_endpoints.add(url)

        return list(self.discovered_endpoints)

    async def _is_graphql_endpoint(self, url: str) -> bool:
        """
        Check if a URL is a GraphQL endpoint.

        Args:
            url: URL to check

        Returns:
            True if it's a GraphQL endpoint
        """
        try:
            # Try importing aiohttp for async requests
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    # Try a simple query
                    async with session.post(
                        url,
                        json={"query": "{ __typename }"},
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Check for GraphQL-specific response structure
                            return "data" in data or "errors" in data
            except ImportError:
                # Fallback to requests
                import requests
                response = requests.post(
                    url,
                    json={"query": "{ __typename }"},
                    headers=self.headers,
                    timeout=10,
                )
                if response.status_code == 200:
                    data = response.json()
                    return "data" in data or "errors" in data
        except Exception:
            pass

        return False

    async def introspect_schema(self, endpoint_url: str) -> Optional[Dict]:
        """
        Perform GraphQL introspection to discover schema.

        Args:
            endpoint_url: GraphQL endpoint URL

        Returns:
            Schema dictionary or None if introspection fails
        """
        try:
            # Try async first
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        endpoint_url,
                        json={"query": INTROSPECTION_QUERY},
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=30),
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if "data" in data and "__schema" in data["data"]:
                                schema = data["data"]["__schema"]
                                self.schemas[endpoint_url] = schema
                                return schema
            except ImportError:
                # Fallback to sync
                import requests
                response = requests.post(
                    endpoint_url,
                    json={"query": INTROSPECTION_QUERY},
                    headers=self.headers,
                    timeout=30,
                )
                if response.status_code == 200:
                    data = response.json()
                    if "data" in data and "__schema" in data["data"]:
                        schema = data["data"]["__schema"]
                        self.schemas[endpoint_url] = schema
                        return schema
        except Exception:
            pass

        return None

    def extract_queries(self, schema: Dict) -> List[str]:
        """
        Extract all queries from schema.

        Args:
            schema: GraphQL schema from introspection

        Returns:
            List of query names
        """
        queries = []
        
        if "queryType" in schema and schema["queryType"]:
            query_type_name = schema["queryType"]["name"]
            
            # Find the Query type in types
            for type_info in schema.get("types", []):
                if type_info.get("name") == query_type_name:
                    for field in type_info.get("fields", []):
                        queries.append(field["name"])
                    break
        
        return queries

    def extract_mutations(self, schema: Dict) -> List[str]:
        """
        Extract all mutations from schema.

        Args:
            schema: GraphQL schema from introspection

        Returns:
            List of mutation names
        """
        mutations = []
        
        if "mutationType" in schema and schema["mutationType"]:
            mutation_type_name = schema["mutationType"]["name"]
            
            # Find the Mutation type in types
            for type_info in schema.get("types", []):
                if type_info.get("name") == mutation_type_name:
                    for field in type_info.get("fields", []):
                        mutations.append(field["name"])
                    break
        
        return mutations

    def extract_subscriptions(self, schema: Dict) -> List[str]:
        """
        Extract all subscriptions from schema.

        Args:
            schema: GraphQL schema from introspection

        Returns:
            List of subscription names
        """
        subscriptions = []
        
        if "subscriptionType" in schema and schema["subscriptionType"]:
            subscription_type_name = schema["subscriptionType"]["name"]
            
            # Find the Subscription type in types
            for type_info in schema.get("types", []):
                if type_info.get("name") == subscription_type_name:
                    for field in type_info.get("fields", []):
                        subscriptions.append(field["name"])
                    break
        
        return subscriptions

    def extract_all_endpoints(self, schema: Dict) -> Dict[str, List[str]]:
        """
        Extract all endpoints from schema.

        Args:
            schema: GraphQL schema from introspection

        Returns:
            Dictionary with queries, mutations, and subscriptions
        """
        return {
            "queries": self.extract_queries(schema),
            "mutations": self.extract_mutations(schema),
            "subscriptions": self.extract_subscriptions(schema),
        }

    async def full_discovery(self, custom_paths: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Perform full GraphQL discovery.

        Args:
            custom_paths: Additional paths to check

        Returns:
            Dictionary with discovered endpoints and their schemas
        """
        # Discover endpoints
        endpoints = await self.discover_endpoints(custom_paths)
        
        results = {
            "endpoints": endpoints,
            "schemas": {},
        }
        
        # Introspect each endpoint
        for endpoint in endpoints:
            schema = await self.introspect_schema(endpoint)
            if schema:
                results["schemas"][endpoint] = {
                    "schema": schema,
                    "endpoints": self.extract_all_endpoints(schema),
                }
        
        return results


async def discover_graphql(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    custom_paths: Optional[List[str]] = None,
) -> Dict[str, any]:
    """
    Convenience function for GraphQL discovery.

    Args:
        base_url: Base URL to scan
        headers: Optional HTTP headers
        custom_paths: Additional paths to check

    Returns:
        Discovery results
    """
    discovery = GraphQLDiscovery(base_url, headers)
    return await discovery.full_discovery(custom_paths)
