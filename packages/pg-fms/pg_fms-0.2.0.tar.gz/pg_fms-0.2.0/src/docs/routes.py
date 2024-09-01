from flask import Flask, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
def landing_page():
    """Landing page for the application."""
    title: str = "Home"
    url: str = "https://pg-fms.vercel.app"
    return render_template("home.jinja2", title=title, url=url)


@app.route("/*", methods=["GET"])
def catch_all():
    """Catch all route for the application."""
    return render_template("dom/404.jinja2")
