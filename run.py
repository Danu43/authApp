from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting HTTPS Flask server...")
    app.run(
    host="127.0.0.1",
    port=5000,
    ssl_context="adhoc",
    debug=True
)
