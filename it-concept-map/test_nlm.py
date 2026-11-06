
import asyncio
from notebooklm import NotebookLMClient

async def main():
    try:
        async with NotebookLMClient.from_storage() as client:
            nb = await client.notebooks.create("test-hello")
            print(f"Created notebook: {nb.id}")
            await client.notebooks.delete(nb.id)
            print("Deleted OK")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

asyncio.run(main())
