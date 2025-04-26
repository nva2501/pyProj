import time
from collections import defaultdict


class RateLimiterService:
    def __init__(self, limit_per_minute=10):
        self.requests = defaultdict(list)
        self.limit = limit_per_minute

    def is_allowed(self, api_key: str) -> bool:
        now = time.time()
        window = 60  # 1 minute
        timestamps = self.requests[api_key]
        self.requests[api_key] = [ts for ts in timestamps if now - ts < window]

        if len(self.requests[api_key]) < self.limit:
            self.requests[api_key].append(now)
            return True
        return False
