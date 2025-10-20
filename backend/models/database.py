import aiosqlite
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

class Database:
    """SQLite database for generation history and metadata"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
    
    async def init_db(self):
        """Initialize database schema"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS generations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    negative_prompt TEXT,
                    model_key TEXT NOT NULL,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    steps INTEGER NOT NULL,
                    guidance_scale REAL NOT NULL,
                    seed INTEGER,
                    file_path TEXT NOT NULL,
                    thumbnail_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logger.info("Database initialized")
    
    async def save_generation(
        self,
        prompt: str,
        negative_prompt: str,
        model_key: str,
        width: int,
        height: int,
        steps: int,
        guidance_scale: float,
        seed: Optional[int],
        file_path: str,
        thumbnail_path: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> int:
        """Save generation to database"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO generations (
                    prompt, negative_prompt, model_key, width, height,
                    steps, guidance_scale, seed, file_path, thumbnail_path, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prompt, negative_prompt, model_key, width, height,
                steps, guidance_scale, seed, file_path, thumbnail_path,
                json.dumps(metadata) if metadata else None
            ))
            await db.commit()
            return cursor.lastrowid
    
    async def get_recent_generations(self, limit: int = 50) -> List[Dict]:
        """Get recent generations"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM generations
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_generation_by_id(self, gen_id: int) -> Optional[Dict]:
        """Get specific generation"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM generations WHERE id = ?
            """, (gen_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None
    
    async def delete_generation(self, gen_id: int) -> bool:
        """Delete generation"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM generations WHERE id = ?", (gen_id,))
            await db.commit()
            return True
    
    async def search_generations(self, query: str, limit: int = 50) -> List[Dict]:
        """Search generations by prompt"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM generations
                WHERE prompt LIKE ? OR negative_prompt LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_stats(self) -> Dict:
        """Get generation statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT 
                    COUNT(*) as total_generations,
                    COUNT(DISTINCT model_key) as models_used,
                    AVG(steps) as avg_steps,
                    AVG(guidance_scale) as avg_guidance
                FROM generations
            """) as cursor:
                row = await cursor.fetchone()
                return {
                    "total_generations": row[0],
                    "models_used": row[1],
                    "avg_steps": round(row[2], 1) if row[2] else 0,
                    "avg_guidance": round(row[3], 2) if row[3] else 0
                }
    
    async def save_setting(self, key: str, value: str):
        """Save app setting"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
            await db.commit()
    
    async def get_setting(self, key: str) -> Optional[str]:
        """Get app setting"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT value FROM settings WHERE key = ?
            """, (key,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None
