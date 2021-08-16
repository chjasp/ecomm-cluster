from psaw import PushshiftAPI
import pandas as pd
import datetime as dt

def retrieve(sub, y, m, d):

	api = PushshiftAPI()
	start_time = int(dt.datetime(y, m, d).timestamp())

	gen = api.search_comments(after=start_time, subreddit=sub)

	max_response_cache = 10000
	cache = []

	for c in gen:
		cache.append(c.body)

		if len(cache) >= max_response_cache:
			break

	return pd.DataFrame(cache, columns=['text'])
