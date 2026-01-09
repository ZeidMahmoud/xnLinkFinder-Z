"""Slack notification provider for xnLinkFinder-Z."""
from typing import Dict, Optional
import requests
import logging
from .notifier import BaseNotifier, NotificationLevel

logger = logging.getLogger(__name__)

class SlackNotifier(BaseNotifier):
    """Send notifications to Slack."""
    
    def _send(self, message: str, level: NotificationLevel) -> bool:
        """Send message to Slack webhook."""
        try:
            color = {
                NotificationLevel.CRITICAL: "#ff0000",
                NotificationLevel.HIGH: "#ff6600",
                NotificationLevel.MEDIUM: "#ffcc00",
                NotificationLevel.LOW: "#00ff00"
            }.get(level, "#808080")
            
            payload = {
                "attachments": [{
                    "color": color,
                    "text": message,
                    "title": f"xnLinkFinder-Z Alert - {level.value.upper()}"
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Slack notification failed: {e}")
            return False

def notify_slack(message: str, webhook_url: str, level: str = "medium") -> bool:
    """Convenience function for Slack notifications."""
    notifier = SlackNotifier(webhook_url)
    return notifier.notify(message, NotificationLevel(level))
