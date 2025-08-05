import sqlite3

conn = sqlite3.connect('coffee_shop.db')
cursor = conn.cursor()
cursor.execute('SELECT name, image_url FROM products ORDER BY id LIMIT 20')
products = cursor.fetchall()

print('First 20 products with their unique images:')
for i, (name, image_url) in enumerate(products, 1):
    image_part = image_url.split('/')[-1][:30] if image_url else 'No image'
    print(f'{i:2d}. {name[:40]:<40} -> {image_part}')

conn.close()
