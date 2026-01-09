"""
Slack Notifications
Send scan results to Slack
"""

import requests
import json
from typing import Dict, Optional


class SlackNotifier:
    """Send notifications to Slack"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(
        self,
        message: str,
        title: Optional[str] = None,
        color: str = "good",
        fields: Optional[Dict] = None
    ) -> bool:
        """Send a message to Slack"""
        payload = {
            "attachments": [{
                "color": color,
                "title": title or "xnLinkFinder Notification",
                "text": message,
                "footer": "xnLinkFinder-Z",
                "ts": int(__import__('time').time())
            }]
        }
        
        if fields:
            payload["attachments"][0]["fields"] = [
                {"title": k, "value": str(v), "short": True}
                for k, v in fields.items()
            ]
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def send_scan_complete(
        self,
        target: str,
        endpoints_found: int,
        duration: float
    ) -> bool:
        """Send scan completion notification"""
        return self.send(
            message=f"Scan completed for {target}",
            title="✅ Scan Complete",
            color="good",
            fields={
                "Target": target,
                "Endpoints Found": endpoints_found,
                "Duration": f"{duration:.2f}s"
            }
        )
    
    def send_critical_finding(
        self,
        target: str,
        finding_type: str,
        details: str
    ) -> bool:
        """Send critical finding notification"""
        return self.send(
            message=details,
            title=f"🚨 Critical Finding: {finding_type}",
            color="danger",
            fields={"Target": target}
        )
