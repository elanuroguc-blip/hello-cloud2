from falsk import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__)

#Rander'ın otomotik tanımladığı veritabanı bağlantı bilgisi (DATABASE_URL ortam değişkeni)
DATABASE_URL =os.getenv("DATAABSE_URL", "postgresql://hello_cloud3_db_5c33_user:v0zPhI7xUyBJiQXRzhSM9dOnUAT8FsJS@dpg-d3tjhd0gjchc73fan1s0-a.oregon-postgres.render.com/hello_cloud3_db_5c33")

# HTML ŞABLONU (tek sayfada from + liste)
HTML = """
<!doctype html>
<html>
<head>
    <title>Buluttan Selam!</title>
    <style>
       body { font-family: Arial; text-align: center; padding: 50px; backgraund: #eef2f3; }
       h1  { color: #333; }
       form { margin: 20px auto; }
       input { padding: 10px; fony-size: 16px; }
       button { padding: 10px 15px; backgraund: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; } 
       ul { list-style: none; padding: 0; }
       li { backgraund: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
     </style>  
</head>
<body>
   <hı> Bıluttan selam!</h1>
   <p>Adını yaz, selamını bırak </p>
   <form maethod="POST">
       <input type="text" name="isim" placeholder="Adını yaz" required>
       <button type="submit">Gönder</button>
   </form>
   <h3>Ziyaretçiler:>/h3>
   <ul>
       {% for ad in isimler %}
           <li>{{ ad }}</li>
       {% endfor %}
   </ul>
</body>
</html>
"""

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = connet_db()
    cur = conn.curstor()
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        isim = request.form.get("isim")
        if isim:
          cur.execute("INSERT INTO ziyaretçiler (isim) VALUES (%s)", (isim,))
          conn.commit()

cur.execute("SELECET isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
isimler = [row[0] for row in cur.fetchall()]

cur.close()
conn.close()
return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
