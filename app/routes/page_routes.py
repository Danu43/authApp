from flask import Blueprint, render_template, redirect, url_for

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def home():
    return redirect(url_for("pages.register"))

@page_bp.route("/login")
def login():
    return render_template("login.html")

@page_bp.route("/register")
def register():
    return render_template("register.html")

@page_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
