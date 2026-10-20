"""Shared-password authentication for legacy routes and the Jinja frontend."""
import hashlib
import json
import secrets

from flask import request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


class PasswordAuth:
    cookie_name = 'edupo_access'
    max_age = 8 * 60 * 60

    def __init__(self, passwords):
        self.passwords = passwords

    def serializer(self):
        # Shared across workers/restarts; changing the password file revokes cookies.
        key = hashlib.sha256(json.dumps(sorted(self.passwords()),
                                        ensure_ascii=False).encode()).digest()
        return URLSafeTimedSerializer(key, salt='edupo-access-v1')

    def valid_password(self, password):
        return bool(password) and any(
            secrets.compare_digest(password.encode(), candidate.encode())
            for candidate in self.passwords() if candidate)

    def authenticated(self):
        # Explicit credentials take precedence, including an incorrect password.
        authorization = request.headers.get('Authorization')
        if authorization is not None:
            scheme, _, password = authorization.partition(' ')
            return scheme.lower() == 'bearer' and self.valid_password(password)
        if 'password' in request.form:
            return self.valid_password(request.form['password'])
        if 'password' in request.args:
            return self.valid_password(request.args['password'])
        if not self.passwords():
            return False
        try:
            return self.serializer().loads(request.cookies.get(self.cookie_name, ''),
                                           max_age=self.max_age) == 'authenticated'
        except (BadSignature, SignatureExpired):
            return False

    def set_cookie(self, response):
        response.set_cookie(
            self.cookie_name, self.serializer().dumps('authenticated'),
            max_age=self.max_age, httponly=True, secure=(request.is_secure or request.host.split(':')[0] in
                    {'edupo.cz', 'www.edupo.cz', 'quest.ms.mff.cuni.cz'}),
            samesite='Strict', path=request.script_root or '/')

    def clear_cookie(self, response):
        response.delete_cookie(self.cookie_name, path=request.script_root or '/')
