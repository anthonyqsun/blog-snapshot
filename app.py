from flask import *
from os import urandom
import Database
import MarkdownParser


db = Database.BlogDatabase("db")
parser = MarkdownParser.MarkdownParser(db)

mdfiles=['making.md', 'tester.md']

for file in mdfiles:
    parser.populate(f"static/md/{file}")


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/")
def root():
    return render_template("home.html", posts=db.getDirectoryPosts())

@app.route("/<var>")
def post(var):
    if db.checkIfMissing(var):
        return render_template("404.html", posts=db.getDirectoryPosts()[:3])
    return render_template("post.html", content=db.getPostFormatted(var))

if __name__ == "__main__":
    app.run(debug=True)