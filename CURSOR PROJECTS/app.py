from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import json
from datetime import datetime
import base64
from email.mime.text import MIMEText
import re
from config import config
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import lru_cache
import time
from google.auth.transport.requests import Request
from flask_caching import Cache
from cachetools import TTLCache
import gc

# Initialize Flask-Caching
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Initialize memory cache for credentials
credentials_cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour TTL

def create_app(config_name='default'):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # OAuth 2.0 configuration
    SCOPES = app.config['GMAIL_SCOPES']
    CLIENT_SECRETS_FILE = app.config['CLIENT_SECRETS_FILE']

    def create_flow():
        return Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=url_for('oauth2callback', _external=True)
        )

    @lru_cache(maxsize=100)
    def get_gmail_service():
        if 'credentials' not in session:
            return None
        credentials = Credentials(
            token=session['credentials']['token'],
            refresh_token=session['credentials']['refresh_token'],
            token_uri=session['credentials']['token_uri'],
            client_id=session['credentials']['client_id'],
            client_secret=session['credentials']['client_secret'],
            scopes=session['credentials']['scopes']
        )
        return build('gmail', 'v1', credentials=credentials)

    @app.route('/')
    def index():
        if 'credentials' in session:
            return redirect(url_for('emails'))
        return render_template('index.html')

    @app.route('/authorize')
    def authorize():
        try:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri=url_for('oauth2callback', _external=True)
            )
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            session['state'] = state
            return redirect(authorization_url)
        except Exception as e:
            app.logger.error(f"Authorization error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/oauth2callback')
    def oauth2callback():
        try:
            state = session['state']
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                state=state,
                redirect_uri=url_for('oauth2callback', _external=True)
            )
            authorization_response = request.url
            flow.fetch_token(authorization_response=authorization_response)
            credentials = flow.credentials
            session['credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            return redirect(url_for('emails'))
        except Exception as e:
            app.logger.error(f"OAuth callback error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/logout')
    def logout():
        session.clear()
        get_gmail_service.cache_clear()  # Clear the service cache
        credentials_cache.clear()
        gc.collect()  # Force garbage collection
        return redirect(url_for('index'))

    @app.route('/emails')
    def emails():
        if 'credentials' not in session:
            return redirect(url_for('authorize'))
        return render_template('emails.html')

    @app.route('/get_emails')
    def get_emails():
        if 'credentials' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        try:
            service = get_gmail_service()
            if not service:
                return jsonify({'error': 'Service not available'}), 401

            # Get list of messages
            results = service.users().messages().list(userId='me', maxResults=10).execute()
            messages = results.get('messages', [])

            # Batch request for message details
            batch = service.new_batch_http_request()
            email_data = {}
            
            def callback(request_id, response, exception):
                if exception is not None:
                    app.logger.error(f"Error in batch request: {str(exception)}")
                    return
                email_data[request_id] = response

            for message in messages:
                batch.add(
                    service.users().messages().get(userId='me', id=message['id']),
                    callback=callback
                )

            batch.execute()

            emails = []
            for message in messages:
                msg = email_data.get(message['id'])
                if not msg:
                    continue

                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                try:
                    parsed_date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
                    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = date

                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,
                    'date': formatted_date
                })

            return jsonify({'emails': emails})

        except Exception as e:
            app.logger.error(f"Error in get_emails: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/get_email/<email_id>')
    def get_email(email_id):
        if 'credentials' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        try:
            service = get_gmail_service()
            if not service:
                return jsonify({'error': 'Service not available'}), 401

            message = service.users().messages().get(userId='me', id=email_id).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                body = ''
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body += base64.urlsafe_b64decode(part['body']['data']).decode()
            else:
                body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode()

            body = re.sub(r'<[^>]+>', '', body)
            body = re.sub(r'\s+', ' ', body)
            body = body.strip()

            return jsonify({
                'email': {
                    'id': email_id,
                    'subject': subject,
                    'sender': sender,
                    'date': date,
                    'body': body
                }
            })

        except Exception as e:
            app.logger.error(f"Error in get_email: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'default'))
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 