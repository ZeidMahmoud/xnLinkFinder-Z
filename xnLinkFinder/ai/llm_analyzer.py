"""
LLM-Powered Endpoint Analysis for xnLinkFinder-Z.

This module integrates with Large Language Models (OpenAI, Claude, Ollama) to:
- Analyze discovered endpoints for security vulnerabilities
- Suggest attack vectors based on endpoint patterns
- Generate custom payloads for testing
- Provide intelligent insights on endpoint behavior
"""

from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class LLMAnalyzer:
    """
    Analyzes endpoints using Large Language Models.
    
    Supports multiple providers:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic Claude
    - Ollama (local models)
    """
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        ollama_url: str = "http://localhost:11434"
    ):
        """
        Initialize LLM analyzer.
        
        Args:
            provider: LLM provider ('openai', 'claude', 'ollama')
            api_key: API key for OpenAI or Claude
            model: Model name to use
            ollama_url: Ollama API URL for local models
        """
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.ollama_url = ollama_url
        self._client = None
        
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider."""
        if self._client:
            return
            
        try:
            if self.provider == "openai":
                import openai
                self._client = openai.OpenAI(api_key=self.api_key)
                self.model = self.model or "gpt-4"
            elif self.provider == "claude":
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
                self.model = self.model or "claude-3-opus-20240229"
            elif self.provider == "ollama":
                import ollama
                self._client = ollama.Client(host=self.ollama_url)
                self.model = self.model or "llama2"
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except ImportError as e:
            logger.warning(f"LLM provider {self.provider} not available: {e}")
            self._client = None
    
    def analyze_endpoint(self, endpoint: str, method: str = "GET", context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze a single endpoint for security vulnerabilities.
        
        Args:
            endpoint: The endpoint URL or path
            method: HTTP method
            context: Additional context about the endpoint
            
        Returns:
            Dictionary with analysis results including vulnerabilities and attack vectors
        """
        if not self._client:
            self._initialize_client()
            
        if not self._client:
            return {"error": "LLM client not available"}
        
        prompt = self._build_analysis_prompt(endpoint, method, context)
        
        try:
            response = self._query_llm(prompt)
            return self._parse_analysis_response(response)
        except Exception as e:
            logger.error(f"Error analyzing endpoint {endpoint}: {e}")
            return {"error": str(e)}
    
    def analyze_batch(self, endpoints: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze multiple endpoints in batch.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of analysis results
        """
        results = []
        for endpoint in endpoints:
            result = self.analyze_endpoint(endpoint)
            results.append({"endpoint": endpoint, "analysis": result})
        return results
    
    def suggest_attack_vectors(self, endpoint: str) -> List[str]:
        """
        Suggest potential attack vectors for an endpoint.
        
        Args:
            endpoint: The endpoint URL or path
            
        Returns:
            List of suggested attack vectors
        """
        if not self._client:
            self._initialize_client()
            
        if not self._client:
            return []
        
        prompt = f"""Analyze this endpoint and suggest specific attack vectors:
        
Endpoint: {endpoint}

Provide a list of potential attack vectors that could be tested, such as:
- SQL injection points
- XSS vulnerabilities
- IDOR patterns
- Authentication bypasses
- Parameter manipulation
- Path traversal

Be specific and actionable."""

        try:
            response = self._query_llm(prompt)
            return self._parse_attack_vectors(response)
        except Exception as e:
            logger.error(f"Error suggesting attack vectors: {e}")
            return []
    
    def generate_payloads(self, endpoint: str, vulnerability_type: str) -> List[str]:
        """
        Generate custom payloads for testing a specific vulnerability.
        
        Args:
            endpoint: The endpoint URL or path
            vulnerability_type: Type of vulnerability (e.g., 'sqli', 'xss', 'idor')
            
        Returns:
            List of generated test payloads
        """
        if not self._client:
            self._initialize_client()
            
        if not self._client:
            return []
        
        prompt = f"""Generate test payloads for {vulnerability_type} testing on this endpoint:
        
Endpoint: {endpoint}

Generate 5-10 specific, targeted payloads that would be most effective for this endpoint.
Consider the endpoint structure and parameters."""

        try:
            response = self._query_llm(prompt)
            return self._parse_payloads(response)
        except Exception as e:
            logger.error(f"Error generating payloads: {e}")
            return []
    
    def _build_analysis_prompt(self, endpoint: str, method: str, context: Optional[Dict]) -> str:
        """Build the analysis prompt for the LLM."""
        prompt = f"""Analyze this endpoint for security vulnerabilities:

Endpoint: {endpoint}
Method: {method}
"""
        if context:
            prompt += f"\nContext: {context}\n"
        
        prompt += """
Provide:
1. Potential vulnerabilities (IDOR, SQLi, XSS, etc.)
2. Risk severity (Critical/High/Medium/Low)
3. Specific attack vectors to test
4. Recommendations for testing

Be specific and actionable."""
        return prompt
    
    def _query_llm(self, prompt: str) -> str:
        """Query the LLM with the given prompt."""
        if self.provider == "openai":
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a security researcher analyzing web endpoints."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        elif self.provider == "claude":
            response = self._client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        elif self.provider == "ollama":
            response = self._client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM analysis response into structured data."""
        return {
            "raw_analysis": response,
            "vulnerabilities": self._extract_vulnerabilities(response),
            "severity": self._extract_severity(response),
            "attack_vectors": self._extract_attack_vectors(response),
            "recommendations": self._extract_recommendations(response)
        }
    
    def _extract_vulnerabilities(self, text: str) -> List[str]:
        """Extract vulnerability types from response text."""
        vuln_keywords = ['IDOR', 'SQLi', 'XSS', 'CSRF', 'SSRF', 'XXE', 'RCE', 'LFI', 'Path Traversal']
        found = []
        for vuln in vuln_keywords:
            if vuln.lower() in text.lower():
                found.append(vuln)
        return found
    
    def _extract_severity(self, text: str) -> str:
        """Extract severity level from response text."""
        text_lower = text.lower()
        if 'critical' in text_lower:
            return 'Critical'
        elif 'high' in text_lower:
            return 'High'
        elif 'medium' in text_lower:
            return 'Medium'
        else:
            return 'Low'
    
    def _extract_attack_vectors(self, text: str) -> List[str]:
        """Extract attack vectors from response text."""
        # Simple extraction - look for numbered lists or bullet points
        vectors = []
        for line in text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                vectors.append(line.lstrip('0123456789.-• '))
        return vectors[:10]  # Limit to 10 vectors
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from response text."""
        recommendations = []
        in_recommendations = False
        for line in text.split('\n'):
            if 'recommendation' in line.lower():
                in_recommendations = True
                continue
            if in_recommendations and line.strip():
                if line[0].isdigit() or line.startswith('-') or line.startswith('•'):
                    recommendations.append(line.lstrip('0123456789.-• '))
        return recommendations[:5]
    
    def _parse_attack_vectors(self, response: str) -> List[str]:
        """Parse attack vectors from LLM response."""
        vectors = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                vectors.append(line.lstrip('0123456789.-• '))
        return vectors
    
    def _parse_payloads(self, response: str) -> List[str]:
        """Parse payloads from LLM response."""
        payloads = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                payload = line.lstrip('0123456789.-• ').strip('`')
                payloads.append(payload)
        return payloads


def analyze_endpoints_with_llm(
    endpoints: List[str],
    provider: str = "openai",
    api_key: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Convenience function to analyze multiple endpoints with LLM.
    
    Args:
        endpoints: List of endpoints to analyze
        provider: LLM provider
        api_key: API key
        **kwargs: Additional arguments for LLMAnalyzer
        
    Returns:
        List of analysis results
    """
    analyzer = LLMAnalyzer(provider=provider, api_key=api_key, **kwargs)
    return analyzer.analyze_batch(endpoints)
