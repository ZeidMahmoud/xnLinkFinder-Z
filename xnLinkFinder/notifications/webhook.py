"""
Generic Webhook Notifications
Send notifications to custom webhooks
"""

import requests
import json
from typing import Dict, Any, Optional


class WebhookNotifier:
    """Send notifications to generic webhooks"""
    
    def __init__(self, webhook_url: str, headers: Optional[Dict[str, str]] = None):
        self.webhook_url = webhook_url
        self.headers = headers or {"Content-Type": "application/json"}
    
    def send(self, payload: Dict[str, Any]) -> bool:
        """Send payload to webhook"""
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers=self.headers,
                timeout=10
            )
            return response.status_code in [200, 201, 202, 204]
        except Exception:
            return False
    
    def send_event(
        self,
        event_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """Send generic event"""
        payload = {
            "event": event_type,
            "source": "xnLinkFinder-Z",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "data": data
        }
        return self.send(payload)
    
    def send_scan_complete(
        self,
        target: str,
        endpoints_found: int,
        duration: float
    ) -> bool:
        """Send scan completion event"""
        return self.send_event(
            "scan_complete",
            {
                "target": target,
                "endpoints_found": endpoints_found,
                "duration_seconds": duration
            }
        )
    
    def send_critical_finding(
        self,
        target: str,
        finding_type: str,
        details: str
    ) -> bool:
        """Send critical finding event"""
        return self.send_event(
            "critical_finding",
            {
                "target": target,
                "type": finding_type,
                "details": details
            }
        )
