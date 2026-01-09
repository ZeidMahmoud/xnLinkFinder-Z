"""Base notification system for xnLinkFinder-Z."""
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class NotificationLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ALL = "all"

class BaseNotifier:
    """Base class for notification providers."""
    
    def __init__(self, webhook_url: str, threshold: NotificationLevel = NotificationLevel.MEDIUM):
        self.webhook_url = webhook_url
        self.threshold = threshold
    
    def should_notify(self, level: NotificationLevel) -> bool:
        """Check if notification should be sent based on threshold."""
        levels = {
            NotificationLevel.CRITICAL: 4,
            NotificationLevel.HIGH: 3,
            NotificationLevel.MEDIUM: 2,
            NotificationLevel.LOW: 1,
            NotificationLevel.ALL: 0
        }
        return levels.get(level, 0) >= levels.get(self.threshold, 2)
    
    def notify(self, message: str, level: NotificationLevel = NotificationLevel.MEDIUM) -> bool:
        """Send notification if threshold met."""
        if self.should_notify(level):
            return self._send(message, level)
        return False
    
    def _send(self, message: str, level: NotificationLevel) -> bool:
        """Override in subclass to implement actual sending."""
        raise NotImplementedError
