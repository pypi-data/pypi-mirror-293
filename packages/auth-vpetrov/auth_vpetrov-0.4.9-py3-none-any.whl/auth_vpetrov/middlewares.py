"""
Necessary middlewares for the app.
"""
import requests
from os import getenv
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from user_vpetrov.schemas import User, Admin
from . import exceptions


host = getenv("AUTH_HOST") if getenv("AUTH_HOST") else "http://172.18.0.11:3001"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{host}/create/user")
oauth2_scheme_admin = OAuth2PasswordBearer(
    tokenUrl=f"{host}/create/admin")

def require_admin_user(token: Annotated[str, Depends(oauth2_scheme_admin)],):
    """
    Middleware to require an admin user.
    """
    url = f"{host}/auth/validate/admin"
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, headers=headers, timeout=5)
    if response.status_code == 200:
        admin = response.json()
        if not admin:
            raise exceptions.AuthorizationException()
        return Admin(**admin)
    print(f"Error: {response.status_code}")
    raise exceptions.ServiceNotAvailable()


def require_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Middleware to require a user.
    """
    url = f"{host}/auth/validate/user"
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.post(url, headers=headers, timeout=5)
    if response.status_code == 200:
        user = response.json()
        if not user:
            raise exceptions.AuthorizationException()
        return User(**user)

    print(f"Error: {response.status_code}")
    raise exceptions.ServiceNotAvailable()
