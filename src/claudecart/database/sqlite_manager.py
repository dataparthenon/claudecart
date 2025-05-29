import json
import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


class SQLiteManager:
    """
    SQLite database manager for ClaudeCart product database.
    
    This class handles the connection, creation, and querying of the SQLite
    database that stores product information, including details, pricing,
    and inventory status.
    """
    
    def __init__(self, db_path: str = "data/claudecart.db"):
        """
        Initialize the SQLite manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
        
    def _ensure_db_exists(self) -> None:
        """Ensure database file and tables exist."""
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        # Connect to database and create tables if they don't exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            price REAL,
            sku TEXT,
            description TEXT,
            rating REAL,
            review_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create product_features table for product features
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_features (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            feature TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        ''')
        
        # Create product_specifications table for detailed specs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_specifications (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            spec_name TEXT,
            spec_value TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def load_seed_data(self, seed_files: List[str]) -> None:
        """
        Load seed data from JSON files into the database.
        
        Args:
            seed_files: List of paths to JSON seed data files
        """
        # Function to be implemented
        pass
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Get product information by ID.
        
        Args:
            product_id: ID of the product to retrieve
            
        Returns:
            Product information dictionary or None if not found
        """
        # Function to be implemented
        pass
    
    def search_products(
        self, 
        query: str, 
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for products based on criteria.
        
        Args:
            query: Search query string
            category: Filter by category
            min_price: Minimum price filter
            max_price: Maximum price filter
            brand: Filter by brand
            
        Returns:
            List of matching product dictionaries
        """
        # Function to be implemented
        pass