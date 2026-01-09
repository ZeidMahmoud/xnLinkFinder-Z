"""Telegram notification provider for xnLinkFinder-Z."""
from typing import Optional
import requests
import logging
from .notifier import BaseNotifier, NotificationLevel

logger = logging.getLogger(__name__)

class TelegramNotifier(BaseNotifier):
    """Send notifications to Telegram."""
    
    def __init__(self, bot_token: str, chat_id: str, threshold: NotificationLevel = NotificationLevel.MEDIUM):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.threshold = threshold
        super().__init__(f"https://api.telegram.org/bot{bot_token}", threshold)
    
    def _send(self, message: str, level: NotificationLevel) -> bool:
        """Send message to Telegram."""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": f"🔍 xnLinkFinder-Z Alert - {level.value.upper()}\n\n{message}",
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Telegram notification failed: {e}")
            return False

def notify_telegram(message: str, bot_token: str, chat_id: str, level: str = "medium") -> bool:
    """Convenience function for Telegram notifications."""
    notifier = TelegramNotifier(bot_token, chat_id)
    return notifier.notify(message, NotificationLevel(level))
