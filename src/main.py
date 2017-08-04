from crunchyroll.apis.meta import MetaApi
api = MetaApi()
print([s.name for s in api.list_anime_series(limit=5)])
