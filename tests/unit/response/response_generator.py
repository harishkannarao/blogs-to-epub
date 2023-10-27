from tests.unit.conftest import MockGetResponse


def create_blog_response(next_link: str = None) -> MockGetResponse:
    links = []
    if next_link is not None:
        links.append({'rel': 'next', 'href': next_link})
    feed = {'link': links}
    response = {'feed': feed}
    mock_get_response = MockGetResponse(response)
    return mock_get_response
