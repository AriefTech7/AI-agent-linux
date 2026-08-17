import os
from typing import Any,Dict
from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()

class WebSearchTool:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    def __clean_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        # Membersihkan respons dari karakter tidak diinginkan
        results = response.get("results", [])
        clean_result = []
        for r in results[0:5]:  # Ambil maksimal 5 hasil
            clean_result.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
                "score": r.get("score"),
            })

        return {
            "query": response.get("query"),
            "answer": response.get("answer"),
            "results": clean_result
        }

    def search_basic(self,query: str) -> Dict[str, Any]:
        # melakukan pencarian basic menggunakan Tavily
        result_basic = self.client.search(
            query=query,
            max_results=5,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False,
            include_images=False
        )
        
        return self.__clean_response(result_basic)
    
    def search_advanced(self,query: str) -> Dict[str, Any]:
        # melakukan pencarian advanced menggunakan Tavily
        result_advanced = self.client.search(
            query=query,
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True
        )
        return self.__clean_response(result_advanced)
    
    def search_fast(self,query: str) -> Dict[str, Any]:
        # melakukan pencarian fast menggunakan Tavily
        result_fast = self.client.search(
            query=query,
            max_results=5,
            search_depth="fast",
            include_answer=True,
            include_raw_content=False,
            include_images=False
        )
        return self.__clean_response(result_fast)
    
