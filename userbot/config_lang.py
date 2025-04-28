import os

LANGUAGE = os.environ.get("LANGUAGE", None)

if LANGUAGE:
    LANGUAGE = LANGUAGE.upper()
else:
    LANGUAGE = "DEFAULT"

if LANGUAGE not in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    print("[Dil]: Bilinməyən bir dil seçdiniz. Buna görə DEFAULT işlədilir.")
    LANGUAGE = "DEFAULT"
