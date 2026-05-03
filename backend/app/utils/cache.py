"""
File-based caching system for AI responses
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class AIResponseCache:
    """File-based cache for AI service responses with automatic expiration"""
    
    def __init__(self, cache_dir: str = "backend/data/cache"):
        """
        Initialize cache with directory path
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.expiration_hours = 24
    
    def _generate_key(self, code: str, language: str, prompt_type: str) -> str:
        """
        Generate SHA-256 hash key for cache lookup
        
        Args:
            code: Code content
            language: Programming language
            prompt_type: Type of AI prompt (explain, summarize, document)
        
        Returns:
            SHA-256 hash string
        """
        try:
            content = f"{code}|{language}|{prompt_type}"
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
        except Exception:
            pass
            return ""
    
    def get(self, code: str, language: str, prompt_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached response if exists and not expired
        
        Args:
            code: Code content
            language: Programming language
            prompt_type: Type of AI prompt
        
        Returns:
            Cached response dict or None if not found/expired
        """
        try:
            cache_key = self._generate_key(code, language, prompt_type)
            if not cache_key:
                return None
            
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            if not cache_file.exists():
                return None
            
            # Read cache file
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check expiration
            timestamp = datetime.fromisoformat(cached_data.get('timestamp', ''))
            expiration_time = timestamp + timedelta(hours=self.expiration_hours)
            
            if datetime.utcnow() > expiration_time:
                # Cache expired, delete file
                cache_file.unlink()
                return None
            
            # Return cached response (without timestamp)
            response = cached_data.get('response')
            return response
            
        except Exception:
            pass
            return None
    
    def set(self, code: str, language: str, prompt_type: str, response: Dict[str, Any]) -> bool:
        """
        Save response to cache
        
        Args:
            code: Code content
            language: Programming language
            prompt_type: Type of AI prompt
            response: Response data to cache
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cache_key = self._generate_key(code, language, prompt_type)
            if not cache_key:
                return False
            
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            # Prepare cache data with timestamp
            cache_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'response': response
            }
            
            # Write to file
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            return True
            
        except Exception:
            pass
            return False
    
    def clear_expired(self) -> int:
        """
        Delete all expired cache files
        
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    # Read cache file
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    # Check expiration
                    timestamp = datetime.fromisoformat(cached_data.get('timestamp', ''))
                    expiration_time = timestamp + timedelta(hours=self.expiration_hours)
                    
                    if datetime.utcnow() > expiration_time:
                        cache_file.unlink()
                        deleted_count += 1
                        
                except Exception:
                    continue
                    
        except Exception:
            pass
        
        return deleted_count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            total_entries = len(cache_files)
            
            # Calculate total size
            total_size_bytes = sum(f.stat().st_size for f in cache_files)
            total_size_mb = round(total_size_bytes / (1024 * 1024), 2)
            
            return {
                'total_entries': total_entries,
                'total_size_bytes': total_size_bytes,
                'total_size_mb': total_size_mb,
                'cache_dir': str(self.cache_dir)
            }
            
        except Exception:
            pass
            return {
                'total_entries': 0,
                'total_size_bytes': 0,
                'total_size_mb': 0.0,
                'cache_dir': str(self.cache_dir)
            }


# Global cache instance
ai_cache = AIResponseCache()

# Made with Bob