from tests.unit.conftest import MockGetResponse


def create_blog_response(
        next_link: str = None,
        chapters: list[tuple[str, str]] = None
) -> MockGetResponse:
    links = []
    if next_link is not None:
        links.append({'rel': 'next', 'href': next_link})
    entries = []
    for chapter in chapters or []:
        title = chapter[0]
        content = chapter[1]
        entries.append({
            'content': {'$t': content},
            'link': [
                {'rel': 'alternate', 'title': title, 'href': 'http://www.example.com'}
            ]
        })
    feed = {'link': links, 'entry': entries}
    response = {'feed': feed}
    mock_get_response = MockGetResponse(response)
    return mock_get_response
