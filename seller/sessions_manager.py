import time
import uuid

class SessionsManager:
    def __init__(self):
        self.sessions = {}
        self.SESSION_TIMEOUT = 30  # 5 minutes

    def manage_session(self, data):
        if 'session_id' in data['body']:
            if data['body']['session_id'] in self.sessions:
                session_id = data['body']['session_id']
                self.sessions[data['body']['session_id']]["updated_at"] = time.time()
                print('SESSION exists::', session_id)
                return {'exists': True, 'session_id': session_id}
            else:
                session_id = str(uuid.uuid4())
                time_now = time.time()
                self.sessions[session_id] = {'created_at': time_now, 'updated_at': time_now}
                print('Invalid session. New session_id: ', session_id)
                return {'exists': False, 'session_id': session_id}
        else:
            print('No session')
            session_id = str(uuid.uuid4())
            time_now = time.time()
            self.sessions[session_id] = {'created_at': time_now, 'updated_at': time_now}
            print('No session. New sessionid:', session_id)
            return {'exists': False, 'session_id': session_id}


    def session_cleaner(self):
        while True:
            current_time = time.time()
            expired_sessions = [sid for sid, session in self.sessions.items() if
                                current_time - session['created_at'] > self.SESSION_TIMEOUT]

            for sid in expired_sessions:
                del self.sessions[sid]

            print(f"Cleaned up {len(expired_sessions)} expired sessions.")
            time.sleep(60)  # Check every minute