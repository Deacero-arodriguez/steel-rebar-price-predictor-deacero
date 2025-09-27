"""Cache service for the Steel Rebar Price Predictor API."""

import redis
import json
import pickle
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching predictions and data."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=False)
            # Test connection
            self.redis_client.ping()
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Using in-memory cache.")
            self.redis_client = None
            self.memory_cache = {}
    
    def _get_cache_key(self, key_type: str, identifier: str = "") -> str:
        """Generate cache key."""
        return f"steel_rebar:{key_type}:{identifier}"
    
    def set_prediction(self, prediction_data: Dict, ttl: int = 3600) -> bool:
        """Cache a prediction result."""
        try:
            cache_key = self._get_cache_key("prediction", "latest")
            
            # Add timestamp
            prediction_data['cached_at'] = datetime.now().isoformat()
            
            if self.redis_client:
                self.redis_client.setex(
                    cache_key, 
                    ttl, 
                    json.dumps(prediction_data)
                )
            else:
                self.memory_cache[cache_key] = {
                    'data': prediction_data,
                    'expires_at': datetime.now() + timedelta(seconds=ttl)
                }
            
            logger.info(f"Prediction cached with TTL {ttl}s")
            return True
            
        except Exception as e:
            logger.error(f"Error caching prediction: {e}")
            return False
    
    def get_prediction(self) -> Optional[Dict]:
        """Get cached prediction."""
        try:
            cache_key = self._get_cache_key("prediction", "latest")
            
            if self.redis_client:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            else:
                if cache_key in self.memory_cache:
                    cache_entry = self.memory_cache[cache_key]
                    if datetime.now() < cache_entry['expires_at']:
                        return cache_entry['data']
                    else:
                        del self.memory_cache[cache_key]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached prediction: {e}")
            return None
    
    def set_training_data(self, data: Any, ttl: int = 86400) -> bool:
        """Cache training data."""
        try:
            cache_key = self._get_cache_key("training_data", "latest")
            
            if self.redis_client:
                self.redis_client.setex(
                    cache_key,
                    ttl,
                    pickle.dumps(data)
                )
            else:
                self.memory_cache[cache_key] = {
                    'data': data,
                    'expires_at': datetime.now() + timedelta(seconds=ttl)
                }
            
            logger.info(f"Training data cached with TTL {ttl}s")
            return True
            
        except Exception as e:
            logger.error(f"Error caching training data: {e}")
            return False
    
    def get_training_data(self) -> Optional[Any]:
        """Get cached training data."""
        try:
            cache_key = self._get_cache_key("training_data", "latest")
            
            if self.redis_client:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return pickle.loads(cached_data)
            else:
                if cache_key in self.memory_cache:
                    cache_entry = self.memory_cache[cache_key]
                    if datetime.now() < cache_entry['expires_at']:
                        return cache_entry['data']
                    else:
                        del self.memory_cache[cache_key]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached training data: {e}")
            return None
    
    def set_rate_limit(self, api_key: str, requests_count: int, ttl: int = 3600) -> bool:
        """Set rate limit for API key."""
        try:
            cache_key = self._get_cache_key("rate_limit", api_key)
            
            rate_data = {
                'requests': requests_count,
                'window_start': datetime.now().isoformat()
            }
            
            if self.redis_client:
                self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(rate_data)
                )
            else:
                self.memory_cache[cache_key] = {
                    'data': rate_data,
                    'expires_at': datetime.now() + timedelta(seconds=ttl)
                }
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting rate limit: {e}")
            return False
    
    def get_rate_limit(self, api_key: str) -> Optional[Dict]:
        """Get rate limit for API key."""
        try:
            cache_key = self._get_cache_key("rate_limit", api_key)
            
            if self.redis_client:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            else:
                if cache_key in self.memory_cache:
                    cache_entry = self.memory_cache[cache_key]
                    if datetime.now() < cache_entry['expires_at']:
                        return cache_entry['data']
                    else:
                        del self.memory_cache[cache_key]
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting rate limit: {e}")
            return None
    
    def increment_rate_limit(self, api_key: str, limit: int = 100, ttl: int = 3600) -> bool:
        """Increment rate limit counter for API key."""
        try:
            rate_data = self.get_rate_limit(api_key)
            
            if rate_data is None:
                # First request in the window
                return self.set_rate_limit(api_key, 1, ttl)
            
            current_requests = rate_data.get('requests', 0)
            
            if current_requests >= limit:
                logger.warning(f"Rate limit exceeded for API key: {api_key}")
                return False
            
            # Increment counter
            return self.set_rate_limit(api_key, current_requests + 1, ttl)
            
        except Exception as e:
            logger.error(f"Error incrementing rate limit: {e}")
            return False
    
    def clear_cache(self) -> bool:
        """Clear all cache entries."""
        try:
            if self.redis_client:
                # Delete all keys with our prefix
                keys = self.redis_client.keys("steel_rebar:*")
                if keys:
                    self.redis_client.delete(*keys)
            else:
                self.memory_cache.clear()
            
            logger.info("Cache cleared")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        try:
            stats = {
                'redis_connected': self.redis_client is not None,
                'memory_cache_size': len(self.memory_cache) if not self.redis_client else 0
            }
            
            if self.redis_client:
                info = self.redis_client.info()
                stats.update({
                    'redis_used_memory': info.get('used_memory_human'),
                    'redis_connected_clients': info.get('connected_clients'),
                    'redis_keyspace_hits': info.get('keyspace_hits'),
                    'redis_keyspace_misses': info.get('keyspace_misses')
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'error': str(e)}
