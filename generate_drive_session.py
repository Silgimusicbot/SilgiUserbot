from pydrive.auth import GoogleAuth


def main():
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("secret.json")
    if gauth.credentials is None:
        # Doğrulama
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Vaxt
        gauth.Refresh()
    else:
        # Qeydedilən
        gauth.Authorize()
    # Keçərli
    gauth.SaveCredentialsFile("secret.json")


if __name__ == '__main__':
    main()
