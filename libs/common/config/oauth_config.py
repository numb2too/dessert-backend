"""OAuth 配置管理"""

from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def register_oauth_providers(app):
    """註冊 OAuth 提供者"""
    oauth.init_app(app)

    # 註冊 Google OAuth
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    return oauth
