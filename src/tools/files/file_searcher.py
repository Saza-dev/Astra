import os
from typing import List
from crewai.tools import tool
import json

class FileIndexer:
    """Handles file indexing and searching operations"""
    
    def __init__(self, drives: List[str]):
        self.drives = drives
        self.index_cache = {}
    
    def build_index(self, max_depth: int = 3) -> dict:
        """Build file index with depth limit for performance"""
        file_index = {}
        
        for drive in self.drives:
            if not os.path.exists(drive):
                continue
                
            for root, dirs, files in os.walk(drive):
                # Limit depth for performance
                depth = root.replace(drive, '').count(os.sep)
                if depth > max_depth:
                    dirs.clear()  # Don't go deeper
                    continue
                
                # Skip system/hidden folders
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Windows', 'Program Files', '$Recycle.Bin']]
                
                for file in files:
                    file_lower = file.lower()
                    if file_lower not in file_index:
                        file_index[file_lower] = []
                    file_index[file_lower].append(os.path.join(root, file))

                for d in dirs:
                    dir_lower = d.lower()
                    if dir_lower not in file_index:
                        file_index[dir_lower] = []
                    file_index[dir_lower].append(os.path.join(root, d))
                    
        return file_index
    
    def search(self, query: str, search_type: str = 'contains', max_results: int = 10) -> List[str]:
        """Search for files matching the query"""
        if not self.index_cache:
            self.index_cache = self.build_index()
        
        results = []
        query_lower = query.lower()
        
        for filename, paths in self.index_cache.items():
            if len(results) >= max_results:
                break
                
            match = False
            if search_type == 'contains':
                match = query_lower in filename
            elif search_type == 'startswith':
                match = filename.startswith(query_lower)
            elif search_type == 'endswith':
                match = filename.endswith(query_lower)
            elif search_type == 'exact':
                match = filename == query_lower
            
            if match:
                results.extend(paths[:max_results - len(results)])
        
        return results

# Global indexer instance
indexer = FileIndexer(drives=["D:/", "E:/"])

@tool("file_search_tool")
def file_search_tool(query: str, search_type: str = "contains", return_first: bool = True) -> str:
    """
    Search for files in configured drives.
    Args:
        query: Filename or partial name to search for
        search_type: 'contains', 'startswith', 'endswith', or 'exact'
        return_first: If True, returns only the first result
    Returns:
        JSON string with search results
    """
    try:
        if not query or len(query) < 2:
            return json.dumps({"error": "Query too short. Please provide at least 2 characters."})
        
        results = indexer.search(query, search_type, max_results=5)
        
        if not results:
            # Try alternative search types
            for alt_type in ['startswith', 'endswith']:
                if alt_type != search_type:
                    results = indexer.search(query, alt_type, max_results=5)
                    if results:
                        break
        if results:
            if return_first:
                return json.dumps({
                    "found": True,
                    "path": results[0],
                    "total_found": len(results)
                })
            else:
                return json.dumps({
                    "found": True,
                    "paths": results[:5],
                    "total_found": len(results)
                })
        else:
            return json.dumps({
                "found": False,
                "message": f"No files found matching '{query}'"
            })
            
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})
