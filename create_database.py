import sqlite3

def create_database():
    """Veritabanını oluştur ve örnek verilerle doldur"""
    print("Veritabanı oluşturuluyor...")
    
    # Veritabanına bağlan (yoksa oluşturur)
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    
    # Products tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            description TEXT,
            stock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("Products tablosu oluşturuldu.")
    
    # Örnek ürünleri ekle
    sample_products = [
        ("iPhone 15", 45000.0, "Elektronik", "Apple'ın son model telefonu", 15),
        ("Samsung Galaxy S24", 40000.0, "Elektronik", "Samsung'un flaghip telefonu", 20),
        ("MacBook Pro", 85000.0, "Bilgisayar", "Apple'ın profesyonel laptop'u", 8),
        ("Dell XPS 13", 35000.0, "Bilgisayar", "Dell'in ince ve hafif laptop'u", 12),
        ("Sony Headphones", 3500.0, "Ses", "Kablosuz kulaklık", 30),
        ("Nike Air Max", 2800.0, "Ayakkabı", "Spor ayakkabı", 50),
        ("Adidas Ultraboost", 3200.0, "Ayakkabı", "Koşu ayakkabısı", 25),
        ("Kahve Makinesi", 1500.0, "Ev Aletleri", "Otomatik kahve makinesi", 10),
        ("Blender", 800.0, "Ev Aletleri", "Güçlü blender", 18),
        ("Kitap - Python", 120.0, "Kitap", "Python programlama kitabı", 100)
    ]
    
    # Verileri ekle
    cursor.executemany(
        "INSERT INTO products (name, price, category, description, stock) VALUES (?, ?, ?, ?, ?)", 
        sample_products
    )
    
    print(f"{len(sample_products)} adet örnek ürün eklendi.")
    
    # Değişiklikleri kaydet
    conn.commit()
    
    # Kontrol için eklenen verileri göster
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    print("\nEklenen ürünler:")
    print("-" * 60)
    for product in products:
        print(f"ID: {product[0]}, Ad: {product[1]}, Fiyat: {product[2]} TL, Kategori: {product[3]}")
    
    # Bağlantıyı kapat
    conn.close()
    print(f"\nVeritabanı başarıyla oluşturuldu: products.db")

if __name__ == "__main__":
    create_database()
