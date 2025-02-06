from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import  Request, HTTPException
import jwt
import secrets



