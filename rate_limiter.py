# rate_limiter.py
import time
from collections import defaultdict, deque
from fastapi import HTTPException

# Configurações
MAX_REQUESTS = 20        # limite
WINDOW_SECONDS = 60      # por minuto

# Estrutura: { api_key: deque[timestamps] }
requests_log = defaultdict(deque)

def rate_limit(api_key: str):
    now = time.time()
    window_start = now - WINDOW_SECONDS

    timestamps = requests_log[api_key]

    # Remove timestamps antigos
    while timestamps and timestamps[0] < window_start:
        timestamps.popleft()

    if len(timestamps) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Muitas requisições. Tente novamente em instantes."
        )

    timestamps.append(now)
