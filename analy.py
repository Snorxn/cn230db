import sqlite3

# เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

# 1. Top 10 อนิเมะที่มีคะแนนเฉลี่ยสูงสุด
cursor.execute('''
    SELECT title_romaji, average_score
    FROM anime
    WHERE average_score IS NOT NULL
    ORDER BY average_score DESC
    LIMIT 10
''')
top_anime = cursor.fetchall()
print("🎖️ Top 10 Anime by Rating:")
for i, (title, score) in enumerate(top_anime, 1):
    print(f"{i}. {title} — {score}")

# 2. ค่าเฉลี่ยของคะแนนทั้งหมด
cursor.execute('SELECT AVG(average_score) FROM anime WHERE average_score IS NOT NULL')
avg_score = cursor.fetchone()[0]
print(f"\n📊 Average Score: {avg_score:.2f}")

# 3. จำนวนอนิเมะทั้งหมด
cursor.execute('SELECT COUNT(*) FROM anime')
total = cursor.fetchone()[0]
print(f"\n📚 Total Anime Count: {total}")

# 4. สตูดิโอที่ผลิตอนิเมะมากที่สุด
cursor.execute('SELECT studios FROM anime WHERE studios IS NOT NULL')
studios_raw = cursor.fetchall()

# สร้าง dictionary สำหรับนับจำนวนสตูดิโอ
studio_count = {}
for row in studios_raw:
    for studio in row[0].split(', '):
        if studio:
            if studio in studio_count:
                studio_count[studio] += 1
            else:
                studio_count[studio] = 1

print("\n🏢 Top 10 Studios by Number of Anime:")
sorted_studios = sorted(studio_count.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (studio, count) in enumerate(sorted_studios, 1):
    print(f"{i}. {studio}: {count} anime")

# 5. ประเภทอนิเมะยอดนิยม (genres)
cursor.execute('SELECT genres FROM anime WHERE genres IS NOT NULL')
genres_raw = cursor.fetchall()

# สร้าง dictionary สำหรับนับจำนวนประเภท
genre_count = {}
for row in genres_raw:
    for genre in row[0].split(', '):
        if genre:
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1

print("\n🎭 Top 10 Genres:")
sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:10]
for i, (genre, count) in enumerate(sorted_genres, 1):
    print(f"{i}. {genre}: {count} anime")

# 6. จำนวนอนิเมะที่ไม่มีคะแนนหรือจำนวนตอน
cursor.execute('SELECT COUNT(*) FROM anime WHERE average_score IS NULL')
missing_score = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM anime WHERE episodes IS NULL')
missing_episodes = cursor.fetchone()[0]
print(f"\n❌ Missing average_score: {missing_score}")
print(f"❌ Missing episodes: {missing_episodes}")

# 7. อนิเมะประเภท Comedy ที่มีคะแนนสูงสุด
cursor.execute('''
    SELECT title_romaji, average_score
    FROM anime
    WHERE genres LIKE '%Comedy%'
      AND average_score IS NOT NULL
    ORDER BY average_score DESC
    LIMIT 10
''')
top_comedy = cursor.fetchall()
print("\n😂 Top 10 Comedy Anime by Rating:")
for i, (title, score) in enumerate(top_comedy, 1):
    print(f"{i}. {title} — {score}")

conn.close()
