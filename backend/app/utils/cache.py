"""
Simple file-based caching system for AI responses
Reduces API calls and improves response times
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AICache:
    """File-based cache for AI responses with expiration"""
    
    def __init__(self, cache_dir: str = "backend/data/cache", ttl_hours: int = 24):
        """
        Initialize the cache
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours (default: 24)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_hours * 3600
        self.stats = {
            "hits": 0,
            "misses": 0,
            "writes": 0,
            "evictions": 0,
        }
    
    def _generate_cache_key(self, code: str, language: str, prompt_type: str) -> str:
        """
        Generate a unique cache key from code, language, and prompt type
        
        Args:
            code: The code content
            language: Programming language
            prompt_type: Type of prompt (explain, summarize, document)
            
        Returns:
            SHA256 hash as cache key
        """
        # Create a unique string combining all inputs
        cache_string = f"{prompt_type}:{language}:{code}"
        
        # Generate SHA256 hash
        hash_object = hashlib.sha256(cache_string.encode('utf-8'))
        return hash_object.hexdigest()
    
    def _get_cache_file_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, code: str, language: str, prompt_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached response
        
        Args:
            code: The code content
            language: Programming language
            prompt_type: Type of prompt
            
        Returns:
            Cached response dict or None if not found/expired
        """
        cache_key = self._generate_cache_key(code, language, prompt_type)
        cache_file = self._get_cache_file_path(cache_key)
        
        if not cache_file.exists():
            self.stats["misses"] += 1
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if cache has expired
            cached_time = datetime.fromisoformat(cached_data.get("cached_at", ""))
            age_seconds = (datetime.utcnow() - cached_time).total_seconds()
            
            if age_seconds > self.ttl_seconds:
                # Cache expired, remove it
                cache_file.unlink()
                self.stats["evictions"] += 1
                self.stats["misses"] += 1
                logger.debug(f"Cache expired for key {cache_key[:8]}...")
                return None
            
            # Cache hit
            self.stats["hits"] += 1
            logger.debug(f"Cache hit for key {cache_key[:8]}... (age: {age_seconds:.1f}s)")
            
            # Add cache metadata to response
            response = cached_data.get("response", {})
            response["from_cache"] = True
            response["cache_age_seconds"] = round(age_seconds, 2)
            
            return response
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning(f"Failed to read cache file {cache_file}: {e}")
            # Remove corrupted cache file
            cache_file.unlink(missing_ok=True)
            self.stats["misses"] += 1
            return None
    
    def set(self, code: str, language: str, prompt_type: str, response: Dict[str, Any]) -> bool:
        """
        Store a response in cache
        
        Args:
            code: The code content
            language: Programming language
            prompt_type: Type of prompt
            response: Response to cache
            
        Returns:
            True if successfully cached, False otherwise
        """
        cache_key = self._generate_cache_key(code, language, prompt_type)
        cache_file = self._get_cache_file_path(cache_key)
        
        try:
            cache_data = {
                "cache_key": cache_key,
                "cached_at": datetime.utcnow().isoformat(),
                "language": language,
                "prompt_type": prompt_type,
                "code_length": len(code),
                "response": response,
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            self.stats["writes"] += 1
            logger.debug(f"Cached response for key {cache_key[:8]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write cache file {cache_file}: {e}")
            return False
    
    def clear(self) -> int:
        """
        Clear all cache files
        
        Returns:
            Number of files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except Exception as e:
                logger.error(f"Failed to delete cache file {cache_file}: {e}")
        
        logger.info(f"Cleared {count} cache files")
        return count
    
    def clear_expired(self) -> int:
        """
        Clear only expired cache files
        
        Returns:
            Number of expired files deleted
        """
        count = 0
        now = datetime.utcnow()
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cached_data.get("cached_at", ""))
                age_seconds = (now - cached_time).total_seconds()
                
                if age_seconds > self.ttl_seconds:
                    cache_file.unlink()
                    count += 1
                    self.stats["evictions"] += 1
                    
            except Exception as e:
                logger.warning(f"Error processing cache file {cache_file}: {e}")
                # Remove corrupted files
                cache_file.unlink(missing_ok=True)
                count += 1
        
        if count > 0:
            logger.info(f"Cleared {count} expired cache files")
        
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        # Count current cache files
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "writes": self.stats["writes"],
            "evictions": self.stats["evictions"],
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "cached_items": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "ttl_hours": self.ttl_seconds / 3600,
        }
    
    def get_cache_info(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific cache entry
        
        Args:
            cache_key: The cache key
            
        Returns:
            Cache entry information or None
        """
        cache_file = self._get_cache_file_path(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cached_data.get("cached_at", ""))
            age_seconds = (datetime.utcnow() - cached_time).total_seconds()
            
            return {
                "cache_key": cache_key,
                "cached_at": cached_data.get("cached_at"),
                "age_seconds": round(age_seconds, 2),
                "language": cached_data.get("language"),
                "prompt_type": cached_data.get("prompt_type"),
                "code_length": cached_data.get("code_length"),
                "file_size_bytes": cache_file.stat().st_size,
                "expired": age_seconds > self.ttl_seconds,
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache info for {cache_key}: {e}")
            return None


# Global cache instance
_cache: Optional[AICache] = None


def get_cache() -> AICache:
    """Get or create the global cache instance"""
    global _cache
    if _cache is None:
        _cache = AICache()
    return _cache


def clear_cache() -> int:
    """Clear all cached responses"""
    cache = get_cache()
    return cache.clear()


def clear_expired_cache() -> int:
    """Clear only expired cached responses"""
    cache = get_cache()
    return cache.clear_expired()


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    cache = get_cache()
    return cache.get_stats()


# Made with Bob