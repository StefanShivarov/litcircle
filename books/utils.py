import requests
from decouple import config

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
GOOGLE_BOOKS_API_KEY = config('GOOGLE_BOOKS_API_KEY')


def search_google_books(query, page=1, page_size=20):
    start_index = (page - 1) * page_size
    params = {
        'q': query,
        'startIndex': start_index,
        'maxResults': page_size,
        'key': GOOGLE_BOOKS_API_KEY
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
    data = response.json()
    total_items = data.get('totalItems', 0)
    results = []

    for item in data.get('items', []):
        volume_info = item.get('volumeInfo', {})
        book = {
            'google_books_id': item.get('id'),
            'title': volume_info.get('title', 'No title')[:200],
            'authors': ', '.join(volume_info.get('authors', []))[:200],
            'description': volume_info.get('description', '')[:200],
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
        }
        results.append(book)
    return results, total_items


def fetch_google_book(google_books_id):
    url = f"{GOOGLE_BOOKS_API_URL}/{google_books_id}"
    params = {
        'key': GOOGLE_BOOKS_API_KEY,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None
    
    item = response.json()
    volume_info = item.get('volumeInfo', {})
    return {
        'google_books_id': item.get('id'),
        'title': volume_info.get('title', 'No title'),
        'authors': ', '.join(volume_info.get('authors', [])),
        'description': volume_info.get('description', ''),
        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
    }
