"""
SQLite database backend for storing discovered links with metadata.
Enables incremental scans, history tracking, and export to various formats.
"""

import sqlite3
import json
import csv
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import contextlib


class LinkDatabase:
    """SQLite database for storing discovered links."""

    def __init__(self, db_path: str = "xnlinkfinder.db"):
        """
        Initialize the database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create tables
        with self.conn:
            # Links table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    origin_url TEXT,
                    method TEXT DEFAULT 'GET',
                    status_code INTEGER,
                    content_type TEXT,
                    content_length INTEGER,
                    response_time REAL,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    category TEXT,
                    is_prefixed BOOLEAN DEFAULT 0,
                    is_out_of_scope BOOLEAN DEFAULT 0,
                    scan_id TEXT,
                    metadata TEXT
                )
            """)

            # Parameters table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS parameters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    link_id INTEGER,
                    source TEXT,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (link_id) REFERENCES links(id)
                )
            """)

            # Scans table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id TEXT PRIMARY KEY,
                    target TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT DEFAULT 'running',
                    config TEXT,
                    stats TEXT
                )
            """)

            # Create indexes
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_links_url ON links(url)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_links_scan_id ON links(scan_id)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_links_category ON links(category)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_parameters_name ON parameters(name)")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def start_scan(self, target: str, config: Optional[Dict] = None) -> str:
        """
        Start a new scan.

        Args:
            target: Target URL or domain
            config: Scan configuration

        Returns:
            Scan ID
        """
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        config_json = json.dumps(config) if config else None
        
        with self.conn:
            self.conn.execute(
                "INSERT INTO scans (id, target, config) VALUES (?, ?, ?)",
                (scan_id, target, config_json)
            )
        
        return scan_id

    def complete_scan(self, scan_id: str, stats: Optional[Dict] = None):
        """
        Mark scan as complete.

        Args:
            scan_id: Scan ID
            stats: Scan statistics
        """
        stats_json = json.dumps(stats) if stats else None
        
        with self.conn:
            self.conn.execute(
                "UPDATE scans SET completed_at = CURRENT_TIMESTAMP, status = 'completed', stats = ? WHERE id = ?",
                (stats_json, scan_id)
            )

    def add_link(
        self,
        url: str,
        origin_url: Optional[str] = None,
        scan_id: Optional[str] = None,
        **kwargs
    ) -> int:
        """
        Add a link to the database.

        Args:
            url: Link URL
            origin_url: Origin URL where link was found
            scan_id: Scan ID
            **kwargs: Additional metadata (status_code, content_type, etc.)

        Returns:
            Link ID
        """
        metadata = {}
        fields = {
            'url': url,
            'origin_url': origin_url,
            'scan_id': scan_id,
        }
        
        # Extract known fields
        for field in ['method', 'status_code', 'content_type', 'content_length',
                      'response_time', 'category', 'is_prefixed', 'is_out_of_scope']:
            if field in kwargs:
                fields[field] = kwargs[field]
        
        # Remaining kwargs go to metadata
        for key, value in kwargs.items():
            if key not in fields:
                metadata[key] = value
        
        if metadata:
            fields['metadata'] = json.dumps(metadata)
        
        # Build SQL
        columns = ', '.join(fields.keys())
        placeholders = ', '.join(['?' for _ in fields])
        
        try:
            with self.conn:
                cursor = self.conn.execute(
                    f"INSERT INTO links ({columns}) VALUES ({placeholders})",
                    list(fields.values())
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Link already exists, update last_seen
            with self.conn:
                cursor = self.conn.execute(
                    "UPDATE links SET last_seen = CURRENT_TIMESTAMP WHERE url = ? RETURNING id",
                    (url,)
                )
                result = cursor.fetchone()
                return result[0] if result else None

    def add_parameter(
        self,
        name: str,
        link_id: Optional[int] = None,
        source: Optional[str] = None
    ) -> int:
        """
        Add a parameter to the database.

        Args:
            name: Parameter name
            link_id: Associated link ID
            source: Source of parameter discovery

        Returns:
            Parameter ID
        """
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO parameters (name, link_id, source) VALUES (?, ?, ?)",
                (name, link_id, source)
            )
            return cursor.lastrowid

    def get_links(
        self,
        scan_id: Optional[str] = None,
        category: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get links from database.

        Args:
            scan_id: Filter by scan ID
            category: Filter by category
            limit: Maximum number of results

        Returns:
            List of links
        """
        query = "SELECT * FROM links WHERE 1=1"
        params = []
        
        if scan_id:
            query += " AND scan_id = ?"
            params.append(scan_id)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY discovered_at DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

    def get_parameters(self, link_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get parameters from database.

        Args:
            link_id: Filter by link ID

        Returns:
            List of parameters
        """
        if link_id:
            cursor = self.conn.execute(
                "SELECT * FROM parameters WHERE link_id = ?",
                (link_id,)
            )
        else:
            cursor = self.conn.execute("SELECT DISTINCT name FROM parameters")
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def export_to_json(self, output_file: str, scan_id: Optional[str] = None):
        """
        Export links to JSON file.

        Args:
            output_file: Output file path
            scan_id: Filter by scan ID
        """
        links = self.get_links(scan_id=scan_id)
        
        with open(output_file, 'w') as f:
            json.dump(links, f, indent=2, default=str)

    def export_to_csv(self, output_file: str, scan_id: Optional[str] = None):
        """
        Export links to CSV file.

        Args:
            output_file: Output file path
            scan_id: Filter by scan ID
        """
        links = self.get_links(scan_id=scan_id)
        
        if not links:
            return
        
        fieldnames = links[0].keys()
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(links)

    def get_scan_history(self, target: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get scan history.

        Args:
            target: Filter by target

        Returns:
            List of scans
        """
        if target:
            cursor = self.conn.execute(
                "SELECT * FROM scans WHERE target = ? ORDER BY started_at DESC",
                (target,)
            )
        else:
            cursor = self.conn.execute("SELECT * FROM scans ORDER BY started_at DESC")
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_stats(self, scan_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get database statistics.

        Args:
            scan_id: Filter by scan ID

        Returns:
            Statistics dictionary
        """
        query_filter = f"WHERE scan_id = '{scan_id}'" if scan_id else ""
        
        stats = {}
        
        # Total links
        cursor = self.conn.execute(f"SELECT COUNT(*) FROM links {query_filter}")
        stats['total_links'] = cursor.fetchone()[0]
        
        # Links by category
        cursor = self.conn.execute(
            f"SELECT category, COUNT(*) as count FROM links {query_filter} GROUP BY category"
        )
        stats['by_category'] = {row[0] or 'uncategorized': row[1] for row in cursor.fetchall()}
        
        # Total parameters
        cursor = self.conn.execute("SELECT COUNT(DISTINCT name) FROM parameters")
        stats['total_parameters'] = cursor.fetchone()[0]
        
        # Total scans
        cursor = self.conn.execute("SELECT COUNT(*) FROM scans")
        stats['total_scans'] = cursor.fetchone()[0]
        
        return stats
