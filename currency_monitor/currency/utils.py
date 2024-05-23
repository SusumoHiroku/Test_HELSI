import iso4217parse


def get_currency_info(code):
    try:
        currency = iso4217parse.parse(code)
        if currency:
            return currency[0].name, currency[0].alpha3
    except Exception as e:
        print(f"Error parsing currency code {code}: {e}")
    return 'UNKNOWN', 'UNKNOWN'
