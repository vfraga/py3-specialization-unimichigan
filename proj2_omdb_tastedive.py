import requests
import json

PERMANENT_CACHE_FNAME = "permanent_cache.txt"
TEMP_CACHE_FNAME = "this_page_cache.txt"


def _write_to_file(cache, fname):
    with open(fname, 'w') as outfile:
        outfile.write(json.dumps(cache, indent=2))


def _read_from_file(fname):
    try:
        with open(fname, 'r') as infile:
            res = infile.read()
            return json.loads(res)
    except:
        return {}


def add_to_cache(cache_file, cache_key, cache_value):
    temp_cache = _read_from_file(cache_file)
    temp_cache[cache_key] = cache_value
    _write_to_file(temp_cache, cache_file)


def clear_cache(cache_file=TEMP_CACHE_FNAME):
    _write_to_file({}, cache_file)


def make_cache_key(baseurl, params_d, private_keys=["api_key"]):
    """Makes a long string representing the query.
    Alphabetize the keys from the params dictionary so we get the same order each time.
    Omit keys with private info."""
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def get(baseurl, params={}, private_keys_to_ignore=["api_key"], permanent_cache_file=PERMANENT_CACHE_FNAME, temp_cache_file=TEMP_CACHE_FNAME):
    full_url = requests.requestURL(baseurl, params)
    cache_key = make_cache_key(baseurl, params, private_keys_to_ignore)
    # Load the permanent and page-specific caches from files
    permanent_cache = _read_from_file(permanent_cache_file)
    temp_cache = _read_from_file(temp_cache_file)
    if cache_key in temp_cache:
        print("found in temp_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        return requests.Response(temp_cache[cache_key], full_url)
    elif cache_key in permanent_cache:
        print("found in permanent_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        return requests.Response(permanent_cache[cache_key], full_url)
    else:
        print("new; adding to cache")
        # actually request it
        resp = requests.get(baseurl, params)
        # save it
        add_to_cache(temp_cache_file, cache_key, resp.text)
        return resp


def get_movies_from_tastedive(qname):
    base_url = "https://tastedive.com/api/similar"
    qdict = {'q': qname, 'type': 'movies', 'limit': 5}
    return requests_with_caching.get(base_url, qdict).json()


def extract_movie_titles(json_in):
    return [movie['Name'] for movie in json_in['Similar']['Results']]


def get_related_titles(lst_in):
    rtn_lst = []
    for movie in lst_in:
        temp_in = extract_movie_titles(get_movies_from_tastedive(movie))
        for temp_mov in temp_in:
            if temp_mov not in rtn_lst:
                rtn_lst.append(temp_mov)
            elif temp_mov in rtn_lst:
                continue
    return rtn_lst


def get_movie_data(mov_title):
    base_url = "http://www.omdbapi.com/"
    qdict = {'t': mov_title, 'r': 'json'}
    return requests_with_caching.get(base_url, qdict).json()


def get_movie_rating(mov_info_dict):
    for rating in mov_info_dict['Ratings']:
            if rating['Source'] == 'Rotten Tomatoes':
                return int(rating['Value'][:-1])
    return 0


def get_sorted_recommendations(mov_lst):
    related_lst = get_related_titles(mov_lst)
    rating_dict = {}
    for movie in related_lst:
        rating_dict[movie] = get_movie_rating(get_movie_data(movie))
    return [movie[0] for movie in sorted(rating_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
    
