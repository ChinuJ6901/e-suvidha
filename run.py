import os
from app import create_app

app = create_app()
app.secret_key = "a3b9c2f4e6d8g1h0j2k5l7m9n8p3q6r4"


if __name__ == "__main__":
    # Get the port from the environment variable (required for Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
