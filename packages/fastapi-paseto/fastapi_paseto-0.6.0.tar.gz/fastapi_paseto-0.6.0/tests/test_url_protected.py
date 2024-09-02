from typing import Sequence
import pytest
from fastapi_paseto_auth import AuthPASETO
from fastapi_paseto_auth.exceptions import AuthPASETOException
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings


@pytest.fixture(scope="function")
def client():
    app = FastAPI()

    @app.exception_handler(AuthPASETOException)
    def authpaseto_exception_handler(request: Request, exc: AuthPASETOException):
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.get("/paseto-required")
    def paseto_required(Authorize: AuthPASETO = Depends()):
        Authorize.paseto_required()
        return {"hello": "world"}

    @app.get("/paseto-optional")
    def paseto_optional(Authorize: AuthPASETO = Depends()):
        Authorize.paseto_required(optional=True)
        if Authorize.get_paseto_subject():
            return {"hello": "world"}
        return {"hello": "anonym"}

    @app.get("/paseto-refresh-required")
    def fresh_paseto_refresh_required(Authorize: AuthPASETO = Depends()):
        Authorize.paseto_required(refresh_token=True)
        return {"hello": "world"}

    @app.get("/fresh-paseto-required")
    def fresh_paseto_required(Authorize: AuthPASETO = Depends()):
        Authorize.paseto_required(fresh=True)
        return {"hello": "world"}

    client = TestClient(app)
    return client


@pytest.mark.parametrize(
    "url", ["/paseto-required", "/paseto-refresh-required", "/fresh-paseto-required"]
)
def test_missing_header(client, url):
    class SettingsOne(BaseSettings):
        authpaseto_token_location: Sequence[str] = ["headers"]
        authpaseto_secret_key: str = "testing"

    @AuthPASETO.load_config
    def get_settings_one():
        return SettingsOne()

    response = client.get(url)
    assert response.status_code == 401
    assert response.json() == {"detail": "PASETO Authorization Token required"}


@pytest.mark.parametrize(
    "url", ["/paseto-required", "/paseto-optional", "/fresh-paseto-required"]
)
def test_only_access_token_allowed(client, url, Authorize):
    token = Authorize.create_refresh_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Access token required but refresh provided"}


def test_paseto_required(client: TestClient, Authorize: AuthPASETO):
    url = "/paseto-required"
    token = Authorize.create_access_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_paseto_optional(client: TestClient, Authorize: AuthPASETO):
    url = "/paseto-optional"
    # if header not define return anonym user
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"hello": "anonym"}

    token = Authorize.create_access_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_refresh_required(client: TestClient, Authorize: AuthPASETO):
    url = "/paseto-refresh-required"
    # only refresh token allowed
    token = Authorize.create_access_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Refresh token required but access provided"}

    token = Authorize.create_refresh_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_fresh_paseto_required(client: TestClient, Authorize: AuthPASETO):
    url = "/fresh-paseto-required"
    # only fresh token allowed
    token = Authorize.create_access_token(subject="test")
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "PASETO access token is not fresh"}

    token = Authorize.create_access_token(subject="test", fresh=True)
    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
