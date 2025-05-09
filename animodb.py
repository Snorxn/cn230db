import sqlite3
import requests

# สร้างฐานข้อมูลและตาราง
conn = sqlite3.connect("anime.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS anime (
    id INTEGER PRIMARY KEY,
    title_romaji TEXT,
    title_english TEXT,
    title_native TEXT,
    average_score INTEGER,
    studios TEXT,
    episodes INTEGER,
    chapters INTEGER,
    genres TEXT
)
''')
conn.commit()

# GraphQL Query
query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      hasNextPage
    }
    media(type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
      averageScore
      episodes
      chapters
      genres
      studios {
        nodes {
          name
        }
      }
    }
  }
}
'''

url = "https://graphql.anilist.co"
page = 1
per_page = 50

while True:
    variables = {'page': page, 'perPage': per_page}
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    
    for item in data["data"]["Page"]["media"]:
        id = item["id"]
        title_romaji = item["title"].get("romaji")
        title_english = item["title"].get("english")
        title_native = item["title"].get("native")
        average_score = item.get("averageScore")
        episodes = item.get("episodes")
        chapters = item.get("chapters")
        genres = ", ".join(item.get("genres", []))
        studios = ", ".join([s["name"] for s in item.get("studios", {}).get("nodes", [])])

        cursor.execute('''
            INSERT OR REPLACE INTO anime (
                id, title_romaji, title_english, title_native,
                average_score, studios, episodes, chapters, genres
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id, title_romaji, title_english, title_native,
            average_score, studios, episodes, chapters, genres
        ))

    conn.commit()
    if not data["data"]["Page"]["pageInfo"]["hasNextPage"]:
        break
    page += 1

conn.close()
print("✅ บันทึกข้อมูลลง anime.db เรียบร้อยแล้ว")
