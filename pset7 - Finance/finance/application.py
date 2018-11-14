from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id= :id", id = id)[0]["cash"]
    portfolio = db.execute("SELECT symbol, SUM(shares) FROM history WHERE id = :id GROUP BY symbol HAVING SUM(shares) > 0",id = id)
    for entry in portfolio:
        symbol = lookup(entry["symbol"])
        entry["price"] = symbol["price"]
        entry["total"] = entry["price"] * entry["SUM(shares)"]
    total = 0
    for entry in portfolio:
        total += entry["total"]
    total += cash
    return render_template("index.html", output = portfolio, cash = cash, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    elif request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("must enter ticker symbol and shares to purchase")
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")
        id = session["user_id"]
        symbol = lookup(request.form.get("symbol"))
        purchaseprice = int(request.form.get("shares")) * symbol.get("price")
        availablebalance = db.execute("SELECT cash FROM users WHERE id= :id", id = id)
        remainingbalance = availablebalance[0]["cash"] - purchaseprice
        if remainingbalance < 0:
            return (apology("insufficient funds to complete transaction"))
        else:
            db.execute("UPDATE users SET cash = :remainingbalance WHERE id = :id", id = id, remainingbalance=remainingbalance)
            db.execute("INSERT INTO history (id,symbol,shares,price,date) VALUES (:id,:symbol,:shares,:price,datetime('now'))",id=id, symbol=symbol.get("symbol"),shares=int(request.form.get("shares")),price=symbol.get("price"))
        return redirect("/")



@app.route("/history")
@login_required
def history():
    id=session["user_id"]
    transactions = db.execute("SELECT symbol, shares, price, date FROM history WHERE id = :id ORDER BY date DESC", id=id)
    for entry in transactions:
        symbol = lookup(entry["symbol"])
        entry["price"] = symbol["price"]
        entry["total"] = entry["price"] * entry["shares"]
    return render_template("history.html", output=transactions )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must enter valid stock symbol")
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("symbol does not exist")
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
    # User reached route via POST (as by submitting a form via POST)
        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("password"):
            return apology("must provide username/password")
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match")
        hash = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
        if not result:
            return apology("username already taken")
        session["user_id"] = result
        return redirect("login")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        if lookup(request.form.get("symbol")) == None:
            return apology("not a valid symbol")
        if not request.form.get("shares"):
            return apology("must provide the number of shares")
        if request.form.get("shares").isalpha():
            return apology("shares must be numeric")

        id = session["user_id"]
        symbol = lookup(request.form.get("symbol"))
        rows = db.execute("SELECT SUM(shares) FROM history WHERE id = :id AND symbol = :symbol GROUP BY symbol HAVING SUM(shares) > 0", id=id, symbol=symbol["symbol"])
        availableshares = rows[0]["SUM(shares)"]
        sellshares = int(request.form.get("shares"))
        if availableshares < sellshares:
            return apology("not enough shares to complete transaction")
        sellprice = sellshares * symbol.get("price")
        remainingshares = availableshares - sellshares
        currentcash = db.execute("SELECT cash FROM users WHERE id= :id", id = id)[0]["cash"]
        db.execute("UPDATE users SET cash = :currentcash + :sellprice WHERE id= :id", id=id, currentcash=currentcash, sellprice=sellprice)
        db.execute("INSERT INTO history (id,symbol,shares,price,date) VALUES (:id,:symbol,:shares,:price,datetime('now'))",id=id,symbol=symbol.get("symbol"),shares=int(request.form.get("shares")),price=symbol.get("price"))
        return redirect("/")
    else:
        id = session["user_id"]
        portfolio = db.execute("SELECT symbol, SUM(shares) FROM history WHERE id = :id GROUP BY symbol HAVING SUM(shares) > 0",id=id)
        for entry in portfolio:
            symbol = lookup(entry["symbol"])
        return render_template("sell.html", output=portfolio)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
