import secrets
from typing import Literal
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.api.deps import dbConnDep
from app.core.config import settings
from app.core.db import user_table
from app.core.security import create_access_token
from app.crud import find_user_by_email

router = APIRouter()


@router.get("/authorize/{provider}")
def oauth2_authorize(provider: Literal["google", "github"], request: Request):
    provider_data = settings.OAUTH2_PROVIDERS.get(provider)
    if provider_data is None:
        raise HTTPException(status_code=404, detail="provider not found")
    # generate a random string for the state parameter
    request.session["oauth2_state"] = (
        secrets.token_urlsafe()
    )  # to be checked back in the call back
    qs = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": request.url_for("oauth2_callback", provider=provider),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": request.session["oauth2_state"],
        }
    )

    # redirect the user to the OAuth2 provider authorization URL
    return RedirectResponse(url=provider_data["authorize_url"] + "?" + qs)


@router.get(
    "/callback/{provider}"
)  # this route is added on the provider as our client redirect_url
async def oauth2_callback(
    provider: Literal["google", "github"], request: Request, db_conn: dbConnDep
):
    provider_data = settings.OAUTH2_PROVIDERS.get(provider)
    if provider_data is None:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth/callback?error=provider_not_found"
        )

    query_params = request.query_params
    # if there was an authentication error, flash the error messages and exit
    if "error" in query_params:
        error_description = query_params.get(
            "error_description", query_params.get("error")
        )
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/auth/callback?error={error_description}"
        )

    # state parameter has to match the one we created in the authorization request so they won't fool us
    if query_params["state"] != request.session.get("oauth2_state"):
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/auth/callback?error=invalid_state"
        )
    # look for the authorization code so we can use it to get the access_token
    if "code" not in query_params:
        return RedirectResponse(f"{settings.FRONTEND_URL}/auth/callback?error=no_code")

    # exchange the authorization code for an access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            provider_data["token_url"],
            data={
                "client_id": provider_data["client_id"],
                "client_secret": provider_data["client_secret"],
                "code": query_params["code"],
                "grant_type": "authorization_code",
                "redirect_uri": request.url_for("oauth2_callback", provider=provider),
            },
            headers={"Accept": "application/json"},
        )
    if token_response.status_code != 200:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth/callback?error=token_exchange_failed"
        )
    oauth2_token = token_response.json().get("access_token")
    if not oauth2_token:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth/callback?error=missing access_token"
        )

    # use the access token to get the user's email address(scope)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            provider_data["userinfo"]["url"],
            headers={
                "Authorization": "Bearer " + oauth2_token,
                "Accept": "application/json",
            },
        )
    if response.status_code != 200:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth/callback?error=an error occured getting userinfo"
        )
    email = provider_data["userinfo"]["email"](response.json())

    # find or create the user in the database and log them in
    user = find_user_by_email(db_conn, email)
    if user is None:
        stmt = user_table.insert().values(username=email.split("@")[0], email=email)
        result = db_conn.execute(stmt)
        db_conn.commit()
        user_id = result.inserted_primary_key[0]
    else:
        user_id = user.uid
    access_token = create_access_token(user_id)
    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/auth/callback?token={access_token}"
    )
