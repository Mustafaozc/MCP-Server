import httpx
import asyncio
import uuid

async def call_search_web(search_term: str):
    url = "http://127.0.0.1:8000/mcp/"
    call_id = str(uuid.uuid4())

    payload = {
        "type": "tool_call",
        "tool": "search_web",
        "args": {
            "search_term": search_term
        },
        "id": call_id
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            print("\n🔎 Arama Sonuçları:")
            for item in result.get("result", []):
                print(f" - {item}")
            print()

        except httpx.HTTPError as e:
            print(f"HTTP hatası: {e}")
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")

async def terminal_ui():
    print("=== Web Search MCP Client ===")
    while True:
        search_term = input("Aranacak kelime (çıkmak için q): ").strip()
        if search_term.lower() in ("q", "quit", "exit"):
            print("👋 Çıkılıyor...")
            break

        await call_search_web(search_term)

if __name__ == "__main__":
    asyncio.run(terminal_ui())
