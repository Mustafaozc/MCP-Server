import asyncio
import sqlite3
import json
from typing import Any, Dict, List

# MCP kütüphaneleri
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


class SimpleProductServer:
    def __init__(self, db_path: str = "products.db"):
        self.db_path = db_path  # Veritabanı dosyasının yolu
        self.server = Server("product-server")  # MCP server oluştur
        self._setup_handlers()  # Handler'ları ayarla
    
    def _setup_handlers(self):
        """MCP server handler'larını ayarla"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Claude'un kullanabileceği araçları listele"""
            return [
                types.Tool(
                    name="get_all_products",
                    description="Tüm ürünleri JSON formatında getir",
                    inputSchema={
                        "type": "object",
                        "properties": {},  # Parametre gerektirmiyor
                        "required": []
                    }
                ),
                types.Tool(
                    name="get_product_by_id",
                    description="ID'ye göre belirli bir ürünü getir",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "product_id": {
                                "type": "integer",
                                "description": "Getirilecek ürünün ID'si"
                            }
                        },
                        "required": ["product_id"]
                    }
                ),
                types.Tool(
                    name="search_products",
                    description="Ürün adına göre arama yap",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "search_term": {
                                "type": "string",
                                "description": "Aranacak ürün adı"
                            }
                        },
                        "required": ["search_term"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Araç çağrılarını işle"""
            
            # Veritabanına bağlan
            try:
                conn = sqlite3.connect(self.db_path)
                conn.row_factory = sqlite3.Row  # Sonuçları dictionary gibi kullanabilmek için
                cursor = conn.cursor()
                
                if name == "get_all_products":
                    # Tüm ürünleri getir
                    cursor.execute("SELECT * FROM products")
                    products = [dict(row) for row in cursor.fetchall()]
                    
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(products, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "get_product_by_id":
                    # Belirli ID'li ürünü getir
                    product_id = arguments["product_id"]
                    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
                    product = cursor.fetchone()
                    
                    if product:
                        result = dict(product)
                    else:
                        result = {"error": f"ID {product_id} ile ürün bulunamadı"}
                    
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2, ensure_ascii=False)
                    )]
                
                elif name == "search_products":
                    # Ürün adına göre arama yap
                    search_term = arguments["search_term"]
                    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{search_term}%",))
                    products = [dict(row) for row in cursor.fetchall()]
                    
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(products, indent=2, ensure_ascii=False)
                    )]
                
                else:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({"error": f"Bilinmeyen araç: {name}"})
                    )]
                    
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"Veritabanı hatası: {str(e)}"})
                )]
            finally:
                # Bağlantıyı kapat
                conn.close()

    async def run(self):
        """Server'ı çalıştır"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="product-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


async def main():
    """Ana fonksiyon - Server'ı başlat"""
    print("Product MCP Server başlatılıyor...")
    print("Veritabanı dosyası: products.db")
    print("Ctrl+C ile durdurmak için...")
    
    server = SimpleProductServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
