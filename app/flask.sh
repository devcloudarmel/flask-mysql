#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=testproduction
flask run --host=0.0.0.0 --port=5000 &
FLASK_PID=$!

# Wait for a few seconds to ensure the server starts
sleep 5

# Example test command
curl http://localhost:5000/books

# Kill the Flask server after tests or other commands
kill $FLASK_PID
