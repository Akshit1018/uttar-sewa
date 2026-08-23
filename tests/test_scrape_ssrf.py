from backend.services.public_enrichment import PublicHttp


class _Recorder:
    last_kwargs = None

    def __init__(self, **kwargs):
        _Recorder.last_kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def get(self, url, **_kwargs):
        class _Resp:
            status_code = 200
            text = "ok"

            def raise_for_status(self):
                return None

            def json(self):
                return {}

        return _Resp()


def test_public_http_does_not_follow_redirects(monkeypatch):
    monkeypatch.setattr("backend.services.public_enrichment.httpx.Client", _Recorder)
    http = PublicHttp()
    http.get_text("https://en.wikipedia.org/wiki/Karma")
    assert _Recorder.last_kwargs["follow_redirects"] is False
    http.get_json("https://en.wikipedia.org/api/rest_v1/page/summary/Karma")
    assert _Recorder.last_kwargs["follow_redirects"] is False
