from email.quoprimime import quote
import urllib.request,json
from .models import Quote

base_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
    get_quote_url=base_url.format()

    with urllib.request.urlopen(get_quote_url) as url:
        quote_data=url.read()
        quote_response=json.loads(quote_data)

        quote_object=None
        if quote_response:
            quote = quote_response.get('quote')
            author = quote_response.get('author')

            quote_object=Quote(quote,author)
            print(quote_object)

    return quote_object
