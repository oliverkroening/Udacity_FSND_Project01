from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen


app = Flask(__name__)

AUTH0_DOMAIN = 'dev-j3q44hh5n3sv0ndq.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image' # API_IDENTIFIER

# https://auth0.com/docs/api/authentication#authorization-code-flow
# GET https://dev-j3q44hh5n3sv0ndq.us.auth0.com/authorize?
#   audience=image&
#   response_type=token&
#   client_id=fA2qQe9bYrZe8HbXrRwwya1c9WVheBr0&
#   redirect_uri=https://localhost:8080/login-results
# https://dev-j3q44hh5n3sv0ndq.us.auth0.com/authorize?audience=image&response_type=token&client_id=fA2qQe9bYrZe8HbXrRwwya1c9WVheBr0&redirect_uri=https://localhost:8080/login-results
# JWT for oliver.kroening@gmx.de:
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVLSTBCdG1Wa1BXVUxhdHh0VU0zSiJ9.eyJpc3MiOiJodHRwczovL2Rldi1qM3E0NGhoNW4zc3YwbmRxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTNmOWIxOTE4ZDgxODc3ZmJiMWRlOGQiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTY5ODY2NzczNiwiZXhwIjoxNjk4Njc0OTM2LCJhenAiOiJmQTJxUWU5YllyWmU4SGJYclJ3d3lhMWM5V1ZoZUJyMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmltYWdlcyJdfQ.bBhGj4Fs4OG-Ikv50_I-HAF11iSQ2ziACGMmXZ-lHtUkElYf-4FvEltBFPAcZBD2Bn_resMOm4n8JJnYdSqrDg-H43owFbCKGKpzjslXNP0Y9VJ-24Di-h_ZePsDHlAUrbVQ-ob3ZlwPfLhrs1vuuAuCConf_4UtYeXtwMD4j9kGyJbyF2hp3PXxKzUbQ6nks6KJgkWC1CpGHm3pJKO8Aqb0PtEg0wO41jGSVRpZ8sann_JZAOWJTRmay17lNmvaLY0yAjaYaIpoHoUBRWPuEH13onUCDsf1sU2AL9tXHzxACYSvgp1L-7fwN2OlwU3FDMge9Fw38MjOxnxRm7sWmQ

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

# @app.route('/headers')
# @requires_auth
# def headers(payload):
#     print(payload)
#     return 'Access Granted'

@app.route('/image')
@requires_auth('get:images')
def images(jwt):
    print(jwt)
    return 'not implemented'
