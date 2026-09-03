from app import create_app

# The factory builds the app; this module only exists to run it locally.
# Gunicorn imports 'app' directly and never touches the __main__ block.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)