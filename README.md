

# Flipkart-Auth

1. requirements
  Flask
  requests
  
2. Use ngrok to generate a callback URL to http://localhost:8001
```
./ngrok http 8001
```
3. Register a Flipkart App at the Flipkart Developer Admin Portal.
  Add the Redirect URL as:
  <ngrok_url>+'/callback'

4. Add this redirect URL to settings.py file (rename 'settings_example.py' to 'settings.py'), along with the Application ID and Application Secret.

5. Run the app
```
python app.py
```

6. Navigate to <ngrok_url>
7. Press the Connect butotn to start the Flipkart-oauth flow
