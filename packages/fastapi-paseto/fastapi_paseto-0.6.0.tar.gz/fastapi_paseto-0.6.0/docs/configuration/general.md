`authpaseto_secret_key`
:   The secret key needed for symmetric based signing algorithms, such as `HS*`. Defaults to `None`

`authpaseto_public_key`
:   The public key needed for asymmetric based signing algorithms, such as `RS*` or `EC*`. PEM format expected.
    Defaults to `None`

`authpaseto_private_key`
:   The private key needed for asymmetric based signing algorithms, such as `RS*` or `EC*`. PEM format expected.
    Defaults to `None`

`authpaseto_purpose`
:   Which purpose to use for the tokens. Options are `public` for asymmetric, `local` for symmetric. Defaults to `local`

`authpaseto_decode_leeway`
:   Define the leeway part of the expiration time definition, which means you can validate an expiration
    time which is in the past but not very far. Defaults to `0`

`authpaseto_encode_issuer`
:   Define the issuer to set the issuer in PASETO claims, only access token have issuer claim. Defaults to `None`

`authpaseto_decode_issuer`
:   Define the issuer to check the issuer in PASETO claims, only access token have issuer claim. Defaults to `None`

`authpaseto_decode_audience`
:   The audience or list of audiences you expect in a PASETO when decoding it. Defaults to `None`

`authpaseto_access_token_expires`
:   How long an access token should live before it expires. This takes value `integer` *(seconds)* or
    `datetime.timedelta`, and defaults to **15 minutes**. Can be set to `False` to disable expiration.

`authpaseto_refresh_token_expires`
:   How long an refresh token should live before it expires. This takes value `integer` *(seconds)* or
    `datetime.timedelta`, and defaults to **30 days**. Can be set to `False` to disable expiration.
