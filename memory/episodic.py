from typing import Any, List, Dict
from langgraph.store.postgres.aio import AsyncPostgresStore



class Episodic():
    def __init__(self, store: AsyncPostgresStore):
        self.store = store
    
    async def get_episodic(self, namespace: tuple[str], key: str) -> Dict:
        item = await self.store.aget(
            namespace=namespace,
            key=key
        )
        return item

    async def update_episodic(self, namespace: tuple[str], key: str, value: dict[str, Any]) -> None:
        return await self.store.put(
            namespace=namespace,
            key=key,
            value=value
        )

    async def search_episodic(self, namespace: tuple[str], query: str, limit: int) -> Dict:
        result = await self.store.asearch(
            namespace=namespace,
            query=query,
            limit=limit
        )
        return result

    async def delete_episodic(self, namespace: tuple[str], key: str) -> None:
        return await self.store.adelete(
            namespace=namespace,
            key=key
        )

    async def list_namespace(self) -> List:
        namespaces = await self.store.list_namespaces()
        struktur_memory = []
        for namespace in namespaces:
            struktur_memory.append(namespace)

        return struktur_memory


