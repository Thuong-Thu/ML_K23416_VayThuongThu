from flask import Flask, render_template_string, request
import mysql.connector
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64, threading, webbrowser

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def getConnect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port = 3306,
            password="thuvt23406@",
            database="sakila"
        )
        print("Đã kết nối thành công với MySQL.")
        return conn
    except Exception as e:
        print("Lỗi kết nối:", e)
        return None


def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    return df


conn = getConnect()


def classify_by_film(film_title):
    sql = f"""
        SELECT DISTINCT 
            f.title AS FilmName,
            c.customer_id AS CustomerID,
            CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
            c.email AS Email
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        WHERE f.title = '{film_title}'
        ORDER BY CustomerName;
    """
    df = queryDataset(conn, sql)
    print(f"\n(1) DANH SÁCH KHÁCH HÀNG THUÊ PHIM '{film_title}':")
    if df.empty:
        print("Không có khách hàng nào thuê phim này.")
    else:
        print(df.to_string(index=False))
    return df


def classify_by_category(category_name):
    sql = f"""
        SELECT DISTINCT 
            cat.name AS CategoryName,
            c.customer_id AS CustomerID,
            CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
            c.email AS Email
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        WHERE cat.name = '{category_name}'
        ORDER BY CustomerName;
    """
    df = queryDataset(conn, sql)
    print(f"\n(2) DANH SÁCH KHÁCH HÀNG THUÊ PHIM THỂ LOẠI '{category_name}':")
    if df.empty:
        print("Không có khách hàng nào thuê thể loại này.")
    else:
        print(df.to_string(index=False))
    return df


def cluster_customers_kmeans(k):
    sql = """
        SELECT 
            c.customer_id AS CustomerID,
            CONCAT(c.first_name, ' ', c.last_name) AS CustomerName,
            COUNT(r.rental_id) AS TotalRentals,
            SUM(p.amount) AS TotalPayment
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY c.customer_id;
    """
    df = queryDataset(conn, sql)
    X = df[['TotalRentals', 'TotalPayment']].values
    model = KMeans(n_clusters=k, init='k-means++', max_iter=500, random_state=42)
    df['Cluster'] = model.fit_predict(X)

    print(f"\n(3) KẾT QUẢ GOM CỤM KHÁCH HÀNG (K = {k}):")
    for cid in sorted(df['Cluster'].unique()):
        print(f"\n--- CỤM {cid} ---")
        print(df[df['Cluster'] == cid][['CustomerID', 'CustomerName', 'TotalRentals', 'TotalPayment']].to_string(index=False))
        print("-----------------------------------")
    return df


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    mode = request.form.get("mode", "cluster")
    result_df = pd.DataFrame()
    image = None
    clusters = {}
    search_query = request.form.get("search", "").strip()

    if mode == "film":
        title = request.form.get("film_title", "").strip()
        if title:
            result_df = classify_by_film(title)
    elif mode == "category":
        cat = request.form.get("category_name", "").strip()
        if cat:
            result_df = classify_by_category(cat)
    else:
        k = int(request.form.get("k_value", 4))
        df = cluster_customers_kmeans(k)

        if search_query:
            df = df[df['CustomerName'].str.lower().str.contains(search_query.lower()) |
                    df['CustomerID'].astype(str).str.contains(search_query)]

        clusters = {cid: df[df['Cluster'] == cid] for cid in sorted(df['Cluster'].unique())}

        # Biểu đồ scatter K-Means
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(df['TotalRentals'], df['TotalPayment'], c=df['Cluster'], cmap='rainbow', s=60)
        ax.set_xlabel("Total Rentals")
        ax.set_ylabel("Total Payment")
        ax.set_title(f"K-Means Customer Clusters (K={k})")
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        image = base64.b64encode(buf.read()).decode('utf-8')

    html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Phân tích khách hàng - Sakila</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="bg-light">
        <div class="container py-4">
            <h2 class="text-center mb-4 text-primary">Phân tích khách hàng trong cơ sở dữ liệu Sakila</h2>
            <form method="POST" class="row g-3 mb-4">
                <div class="col-md-3">
                    <select name="mode" class="form-select" onchange="this.form.submit()">
                        <option value="cluster" {% if mode=='cluster' %}selected{% endif %}>Phân cụm K-Means</option>
                        <option value="film" {% if mode=='film' %}selected{% endif %}>Theo tên phim</option>
                        <option value="category" {% if mode=='category' %}selected{% endif %}>Theo thể loại</option>
                    </select>
                </div>

                {% if mode == 'film' %}
                    <div class="col-md-4">
                        <input type="text" name="film_title" class="form-control" placeholder="Nhập tên phim..." value="{{ request.form.get('film_title','') }}">
                    </div>
                {% elif mode == 'category' %}
                    <div class="col-md-4">
                        <input type="text" name="category_name" class="form-control" placeholder="Nhập tên thể loại..." value="{{ request.form.get('category_name','') }}">
                    </div>
                {% else %}
                    <div class="col-md-2">
                        <input type="number" name="k_value" class="form-control" value="{{ request.form.get('k_value',4) }}" min="2" max="10">
                    </div>
                    <div class="col-md-4">
                        <input type="text" name="search" class="form-control" placeholder="Tìm khách hàng theo tên hoặc ID..." value="{{ request.form.get('search','') }}">
                    </div>
                {% endif %}

                <div class="col-md-2">
                    <button class="btn btn-primary w-100">Xem kết quả</button>
                </div>
            </form>

            {% if image %}
                <div class="text-center mb-4">
                    <img src="data:image/png;base64,{{ image }}" class="img-fluid border rounded shadow-sm"/>
                </div>
            {% endif %}

            {% if mode == 'cluster' and clusters %}
                {% for cid, g in clusters.items() %}
                    <h4 class="text-success mt-4">Cụm {{ cid }}</h4>
                    <table class="table table-bordered table-striped">
                        <thead class="table-info">
                            <tr>
                                {% for col in g.columns %}
                                    <th>{{ col }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for _, row in g.iterrows() %}
                                <tr>
                                    {% for val in row %}
                                        <td>{{ val }}</td>
                                    {% endfor %}
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% endfor %}
            {% elif not result_df.empty %}
                <table class="table table-bordered table-striped">
                    <thead class="table-primary">
                        <tr>
                            {% for col in result_df.columns %}
                                <th>{{ col }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for _, row in result_df.iterrows() %}
                            <tr>
                                {% for val in row %}
                                    <td>{{ val }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, mode=mode, image=image, clusters=clusters, result_df=result_df, request=request)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("Flask đang chạy tại http://127.0.0.1:5000")
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
