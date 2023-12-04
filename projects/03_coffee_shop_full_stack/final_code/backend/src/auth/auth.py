import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-j3q44hh5n3sv0ndq.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
#### Done ####
def get_token_auth_header():
    '''
    Function to obtain the access token from the authorization header.
    remark: this function is created and implemented according to 
    the practices in the IAM module of the Full-Stack Nanodegree program!
    source: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
    
    - INPUT:
        - None
    - OUTPUT:
        - token: extracted token (JWT) from authorization header
    '''
    # get authorization header from request
    auth = request.headers.get('Authorization', None)

    # raise 401 error in case there is no authorization header in the request
    if auth is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    # parse the header by splitting in different parts
    parts = auth.split()
    
    # check for 'bearer' token
    if parts[0].lower() != 'bearer':
        # raise 401 error in case there is no bearer token
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        # raise 401 error in case there is no expected token
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        # raise 401 error in case there is no bearer token 
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # assign and return token from parsed authorization header
    token = parts[1]
    return token

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in 
    the payload permissions array return true otherwise
'''
#### Done ####
def check_permissions(permission, payload):
    '''
    Function to check permissions extracted from the payload of the request
    according to the required permissions of the API endpoint that should
    be executed.
    remark: this function is created and implemented according to 
    the practices in the IAM module of the Full-Stack Nanodegree program!
    source: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
    
    - INPUT:
        - permission: required function of API endpoint
        - payload: decoded payload extracted from the authorization header
    - OUTPUT:
        - True if the required permissions match the permissions in the payload
    '''
    # check for permissions in payload
    # raise 403 error in case there are no permissions included in JWT
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 403)
    # raise 403 error (unauthorized) in case the permissions in the payload
    # do not match the required permissions of the API endpoint.
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    # return True in case there are not authentication errors during the check
    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
#### Done ####
def verify_decode_jwt(token):
    '''
    Function to decode and verify the token extracted from the 
    authorization header. 
    The function returns the payload of the token or raises errors
    in case there are some issues in the verification process
    remark: this function is created and implemented according to 
    the practices in the IAM module of the Full-Stack Nanodegree program!
    source: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
    
    - INPUT:
        - token: token from the authorization header
    - OUTPUT:
        - payload: decoded payload from JWT    
    '''
    # Open Auth0-domain and verify the token using Auth0 /.well-known/jwks.json
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    
    # get RSA-keys from header
    rsa_key = {}
    if 'kid' not in unverified_header:
        # raise 401 error in case there is no key id (kid)
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # get infromation from key id and store in RSA-key
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # return decoded payload from JWT in case there is a RSA-key
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

        # raise 401 error in case token has expired
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        # raise 401 error in case the the audience and issuer caused an error
        # during the decoding of the JWT.
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims.'
            }, 401)
        
        # raise 400 error in case the payload could not be parsed 
        # due to bad request.
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    
    # raise 400 error if there is no appropriate key in JWT due to bad request
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the 
    requested permission
    return the decorator which passes the decoded payload to the decorated 
    method
'''
#### Done ####
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            '''
            Wrapper function to get the token from the authorization header
            and verify the extracted JWT. 
            After the payload is extracted the function checks the permission
            that is stated in the payload.
            remark: this function as well as the linked functions 
                - verify_decode_jwt()
                - check_permissions()
                are constructed according to the practices in the IAM module of
                the Full-Stack Nanodegree program!
                source: https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
            '''
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            try:
                check_permissions(permission, payload)
            except:
                abort(403)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator