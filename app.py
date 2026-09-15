from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "homedna.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS home (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            area REAL,
            bedrooms INTEGER,
            bathrooms INTEGER
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            room_type TEXT,
            area REAL,
            status TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity REAL,
            unit TEXT,
            price REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# HTML TEMPLATE
# ============================================================

def page(title, content):

    return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{title} | HomeDNA</title>

<style>

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: Arial, Helvetica, sans-serif;
    background: #f5f7fb;
    color: #172033;
}}

.sidebar {{
    position: fixed;
    left: 0;
    top: 0;
    width: 240px;
    height: 100vh;
    background: #101827;
    color: white;
    padding: 25px 15px;
}}

.logo {{
    font-size: 25px;
    font-weight: bold;
    padding: 10px 15px 35px;
}}

.logo span {{
    font-size: 32px;
}}

.nav a {{
    display: block;
    color: #cbd5e1;
    text-decoration: none;
    padding: 14px 15px;
    margin: 5px 0;
    border-radius: 10px;
}}

.nav a:hover {{
    background: #263449;
    color: white;
}}

.main {{
    margin-left: 240px;
    min-height: 100vh;
}}

.header {{
    background: white;
    padding: 30px 40px;
    border-bottom: 1px solid #e5e7eb;
}}

.header h1 {{
    font-size: 30px;
}}

.header p {{
    color: #6b7280;
    margin-top: 7px;
}}

.content {{
    padding: 35px 40px;
}}

.hero {{
    background: linear-gradient(135deg, #172033, #334155);
    color: white;
    padding: 35px;
    border-radius: 20px;
    margin-bottom: 25px;
}}

.hero h2 {{
    font-size: 32px;
    margin-bottom: 10px;
}}

.hero p {{
    color: #dbe3ef;
    margin-bottom: 20px;
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}}

.stat {{
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.04);
}}

.stat-icon {{
    font-size: 30px;
    margin-bottom: 15px;
}}

.stat p {{
    color: #6b7280;
    margin-bottom: 7px;
}}

.stat h2 {{
    font-size: 28px;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
}}

.card {{
    background: white;
    padding: 30px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.04);
}}

.card h2 {{
    margin-bottom: 20px;
}}

.card p {{
    color: #6b7280;
    margin-bottom: 15px;
}}

form {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}}

input, select {{
    width: 100%;
    padding: 13px;
    border: 1px solid #d1d5db;
    border-radius: 9px;
    font-size: 14px;
    background: white;
}}

button, .button {{
    border: none;
    background: #172033;
    color: white;
    padding: 13px 20px;
    border-radius: 9px;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
}}

button:hover, .button:hover {{
    background: #334155;
}}

.full {{
    grid-column: 1 / -1;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}}

th {{
    color: #6b7280;
    font-size: 13px;
}}

.delete {{
    color: #dc2626;
    text-decoration: none;
}}

.badge {{
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    background: #eef2ff;
    color: #3730a3;
    font-size: 12px;
}}

.total {{
    font-size: 42px;
    font-weight: bold;
}}

.feature {{
    padding: 20px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    margin-top: 10px;
}}

.feature h3 {{
    margin-bottom: 8px;
}}

@media(max-width: 1000px) {{

    .stats {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .grid {{
        grid-template-columns: 1fr;
    }}

}}

@media(max-width: 650px) {{

    .sidebar {{
        position: relative;
        width: 100%;
        height: auto;
    }}

    .main {{
        margin-left: 0;
    }}

    .stats {{
        grid-template-columns: 1fr;
    }}

    form {{
        grid-template-columns: 1fr;
    }}

    .content {{
        padding: 20px;
    }}

    .header {{
        padding: 25px 20px;
    }}

}}

</style>

</head>

<body>


<aside class="sidebar">

    <div class="logo">
        <span>⌂</span> HomeDNA
    </div>

    <div class="nav">

        <a href="/">🏠 Dashboard</a>

        <a href="/home">🏡 My Home</a>

        <a href="/rooms">🚪 Rooms</a>

        <a href="/materials">🧱 Raw Materials</a>

        <a href="/budget">💰 Budget</a>

    </div>

</aside>


<main class="main">

    <header class="header">

        <h1>{title}</h1>

        <p>
            Your digital home management system
        </p>

    </header>


    <section class="content">

        {content}

    </section>

</main>


<script>

console.log("HomeDNA loaded successfully");

</script>

</body>

</html>
"""


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    conn = get_db()

    home = conn.execute(
        "SELECT * FROM home ORDER BY id DESC LIMIT 1"
    ).fetchone()

    room_count = conn.execute(
        "SELECT COUNT(*) AS count FROM rooms"
    ).fetchone()["count"]

    material_count = conn.execute(
        "SELECT COUNT(*) AS count FROM materials"
    ).fetchone()["count"]

    total_expense = conn.execute(
        "SELECT COALESCE(SUM(amount),0) AS total FROM expenses"
    ).fetchone()["total"]

    conn.close()

    home_name = home["name"] if home else "Your Home"

    area = home["area"] if home else "-"
    bedrooms = home["bedrooms"] if home else "-"
    bathrooms = home["bathrooms"] if home else "-"

    content = f"""

<div class="hero">

    <h2>
        Welcome to {home_name}
    </h2>

    <p>
        HomeDNA helps you manage your home,
        rooms, materials and expenses from one place.
    </p>

    <a class="button" href="/home">
        Manage Home
    </a>

</div>


<div class="stats">

    <div class="stat">

        <div class="stat-icon">📐</div>

        <p>Home Area</p>

        <h2>{area} sq.ft</h2>

    </div>


    <div class="stat">

        <div class="stat-icon">🛏️</div>

        <p>Bedrooms</p>

        <h2>{bedrooms}</h2>

    </div>


    <div class="stat">

        <div class="stat-icon">🚿</div>

        <p>Bathrooms</p>

        <h2>{bathrooms}</h2>

    </div>


    <div class="stat">

        <div class="stat-icon">💰</div>

        <p>Total Expenses</p>

        <h2>₹{total_expense:,.2f}</h2>

    </div>

</div>


<div class="grid">

    <div class="card">

        <h2>🚪 Rooms</h2>

        <p>
            Track every room in your home.
        </p>

        <h1>{room_count}</h1>

        <br>

        <a href="/rooms" class="button">
            Manage Rooms
        </a>

    </div>


    <div class="card">

        <h2>🧱 Raw Materials</h2>

        <p>
            Keep track of construction and
            household materials.
        </p>

        <h1>{material_count}</h1>

        <br>

        <a href="/materials" class="button">
            Manage Materials
        </a>

    </div>

</div>


<div class="card">

    <h2>✨ HomeDNA</h2>

    <div class="feature">

        <h3>🏠 Digital Home Profile</h3>

        <p>
            Store your home's important information
            in one central location.
        </p>

    </div>


    <div class="feature">

        <h3>📊 Smart Management</h3>

        <p>
            Monitor rooms, materials and expenses
            through a single dashboard.
        </p>

    </div>


    <div class="feature">

        <h3>💡 Future Ready</h3>

        <p>
            HomeDNA can be extended with AI,
            smart-home integration and predictive
            maintenance.
        </p>

    </div>

</div>

"""

    return page("Home Dashboard", content)


# ============================================================
# HOME
# ============================================================

@app.route("/home", methods=["GET", "POST"])
def home():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        location = request.form["location"]
        area = request.form["area"]
        bedrooms = request.form["bedrooms"]
        bathrooms = request.form["bathrooms"]

        conn.execute("DELETE FROM home")

        conn.execute("""
            INSERT INTO home
            (name, location, area, bedrooms, bathrooms)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            location,
            area,
            bedrooms,
            bathrooms
        ))

        conn.commit()

        conn.close()

        return redirect("/")

    home_data = conn.execute(
        "SELECT * FROM home ORDER BY id DESC LIMIT 1"
    ).fetchone()

    conn.close()

    if home_data:

        name = home_data["name"]
        location = home_data["location"]
        area = home_data["area"]
        bedrooms = home_data["bedrooms"]
        bathrooms = home_data["bathrooms"]

    else:

        name = ""
        location = ""
        area = ""
        bedrooms = ""
        bathrooms = ""

    content = f"""

<div class="card">

    <h2>🏡 My Home Profile</h2>

    <form method="POST">

        <input
            name="name"
            placeholder="Home name"
            value="{name}"
            required
        >

        <input
            name="location"
            placeholder="Location"
            value="{location}"
        >

        <input
            type="number"
            name="area"
            placeholder="Area (sq.ft)"
            value="{area}"
        >

        <input
            type="number"
            name="bedrooms"
            placeholder="Bedrooms"
            value="{bedrooms}"
        >

        <input
            type="number"
            name="bathrooms"
            placeholder="Bathrooms"
            value="{bathrooms}"
        >

        <button type="submit">
            Save Home
        </button>

    </form>

</div>

"""

    return page("My Home", content)


# ============================================================
# ROOMS
# ============================================================

@app.route("/rooms", methods=["GET", "POST"])
def rooms():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        room_type = request.form["room_type"]
        area = request.form["area"]
        status = request.form["status"]

        conn.execute("""
            INSERT INTO rooms
            (name, room_type, area, status)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            room_type,
            area,
            status
        ))

        conn.commit()

    room_data = conn.execute(
        "SELECT * FROM rooms ORDER BY id DESC"
    ).fetchall()

    conn.close()

    rows = ""

    for room in room_data:

        rows += f"""

<tr>

<td>{room["name"]}</td>

<td>{room["room_type"]}</td>

<td>{room["area"]} sq.ft</td>

<td>
<span class="badge">
{room["status"]}
</span>
</td>

<td>
<a class="delete"
href="/rooms/delete/{room["id"]}">
Delete
</a>
</td>

</tr>

"""

    if not rows:

        rows = """
<tr>
<td colspan="5">
No rooms added yet.
</td>
</tr>
"""

    content = f"""

<div class="card">

<h2>➕ Add Room</h2>

<form method="POST">

<input
name="name"
placeholder="Room name"
required
>

<input
name="room_type"
placeholder="Room type"
required
>

<input
type="number"
name="area"
placeholder="Area (sq.ft)"
required
>

<select name="status">

<option>Planned</option>

<option>In Progress</option>

<option>Completed</option>

</select>

<button type="submit">
Add Room
</button>

</form>

</div>


<div class="card">

<h2>🚪 Your Rooms</h2>

<table>

<thead>

<tr>

<th>Name</th>
<th>Type</th>
<th>Area</th>
<th>Status</th>
<th>Action</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>

"""

    return page("Rooms", content)


@app.route("/rooms/delete/<int:id>")
def delete_room(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM rooms WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/rooms")


# ============================================================
# MATERIALS
# ============================================================

@app.route("/materials", methods=["GET", "POST"])
def materials():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        price = request.form["price"]

        conn.execute("""
            INSERT INTO materials
            (name, category, quantity, unit, price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            category,
            quantity,
            unit,
            price
        ))

        conn.commit()

    material_data = conn.execute()
        "SELECT * FROM materials ORDER BY id DESC"
    ).fetchall()

    conn.close()

    rows = ""

    for material in material_data:

        rows += f"""

<tr>

<td>{material["name"]}</td>

<td>{material["category"]}</td>

<td>
{material["quantity"]}
{material["unit"]}
</td>

<td>
₹{material["price"]:,.2f}
</td>

<td>

<a class="delete"
href="/materials/delete/{material["id"]}">
Delete
</a>

</td>

</tr>

"""

    if not rows:

        rows = """
<tr>
<td colspan="5">
No materials added yet.
</td>
</tr>
"""

    content = f"""

<div class="card">

<h2>➕ Add Raw Material</h2>

<form method="POST">

<input
name="name"
placeholder="Material name"
required
>

<input
name="category"
placeholder="Category"
required
>

<input
type="number"
step="0.01"
name="quantity"
placeholder="Quantity"
required
>

<input
name="unit"
placeholder="Unit (kg, bags, pieces)"
required
>

<input
type="number"
step="0.01"
name="price"
placeholder="Price"
required
>

<button type="submit">
Add Material
</button>

</form>

</div>


<div class="card">

<h2>🧱 Material Inventory</h2>

<table>

<thead>

<tr>

<th>Material</th>
<th>Category</th>
<th>Quantity</th>
<th>Price</th>
<th>Action</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>

"""

    return page("Raw Materials", content)


@app.route("/materials/delete/<int:id>")
def delete_material(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM materials WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/materials")


# ============================================================
# BUDGET
# ============================================================

@app.route("/budget", methods=["GET", "POST"])
def budget():

    conn = get_db()

    if request.method == "POST":

        description = request.form["description"]
        category = request.form["category"]
        amount = request.form["amount"]

        conn.execute("""
            INSERT INTO expenses
            (description, category, amount)
            VALUES (?, ?, ?)
        """, (
            description,
            category,
            amount
        ))

        conn.commit()

    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    total = conn.execute(
        "SELECT COALESCE(SUM(amount),0) AS total FROM expenses"
    ).fetchone()["total"]

    conn.close()

    rows = ""

    for expense in expenses:

        rows += f"""

<tr>

<td>{expense["description"]}</td>

<td>{expense["category"]}</td>

<td>
₹{expense["amount"]:,.2f}
</td>

<td>

<a class="delete"
href="/budget/delete/{expense["id"]}">
Delete
</a>

</td>

</tr>

"""

    if not rows:

        rows = """
<tr>
<td colspan="4">
No expenses added yet.
</td>
</tr>
"""

    content = f"""

<div class="card">

<p>Total Home Expenses</p>

<div class="total">
₹{total:,.2f}
</div>

</div>


<div class="card">

<h2>➕ Add Expense</h2>

<form method="POST">

<input
name="description"
placeholder="Expense description"
required
>

<input
name="category"
placeholder="Category"
required
>

<input
type="number"
step="0.01"
name="amount"
placeholder="Amount"
required
>

<button type="submit">
Add Expense
</button>

</form>

</div>


<div class="card">

<h2>💰 Expense History</h2>

<table>

<thead>

<tr>

<th>Description</th>
<th>Category</th>
<th>Amount</th>
<th>Action</th>

</tr>

</thead>

<tbody>

{rows}

</tbody>

</table>

</div>

"""

    return page("Budget", content)


@app.route("/budget/delete/<int:id>")
def delete_expense(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/budget")


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    init_db()

    print("")
    print("===================================")
    print("        HomeDNA is running")
    print("===================================")
    print("")
    print("Open your browser:")
    print("http://127.0.0.1:5000")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )