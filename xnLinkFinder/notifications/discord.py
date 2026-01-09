"""
Discord Notifications
Send scan results to Discord
"""

import requests
import json
from typing import Dict, Optional


class DiscordNotifier:
    """Send notifications to Discord"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(
        self,
        message: str,
        title: Optional[str] = None,
        color: int = 0x00FF00,
        fields: Optional[Dict] = None
    ) -> bool:
        """Send a message to Discord"""
        embed = {
            "title": title or "xnLinkFinder Notification",
            "description": message,
            "color": color,
            "footer": {"text": "xnLinkFinder-Z"},
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
        
        if fields:
            embed["fields"] = [
                {"name": k, "value": str(v), "inline": True}
                for k, v in fields.items()
            ]
        
        payload = {"embeds": [embed]}
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            return response.status_code in [200, 204]
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
            message=f"Scan completed successfully",
            title="✅ Scan Complete",
            color=0x00FF00,  # Green
            fields={
                "Target": target,
                "Endpoints": endpoints_found,
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
            title=f"🚨 Critical: {finding_type}",
            color=0xFF0000,  # Red
            fields={"Target": target}
        )
