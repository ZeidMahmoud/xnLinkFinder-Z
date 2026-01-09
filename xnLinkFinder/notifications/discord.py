"""Discord notification provider for xnLinkFinder-Z."""
from typing import Dict, Optional
import requests
import logging
from .notifier import BaseNotifier, NotificationLevel

logger = logging.getLogger(__name__)

class DiscordNotifier(BaseNotifier):
    """Send notifications to Discord."""
    
    def _send(self, message: str, level: NotificationLevel) -> bool:
        """Send message to Discord webhook."""
        try:
            payload = {
                "content": f"**xnLinkFinder-Z Alert - {level.value.upper()}**\n{message}"
            }
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Discord notification failed: {e}")
            return False

def notify_discord(message: str, webhook_url: str, level: str = "medium") -> bool:
    """Convenience function for Discord notifications."""
    notifier = DiscordNotifier(webhook_url)
    return notifier.notify(message, NotificationLevel(level))
