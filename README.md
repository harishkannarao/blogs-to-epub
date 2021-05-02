# blogs-to-epub

python script to convert Blogger's blog post(s) as epub book(s).

Credit goes to the authors and contributors of the following repositories:

* [psf/requests](https://github.com/psf/requests)
* [aerkalov/ebooklib](https://github.com/aerkalov/ebooklib)

## Tools Required

* python `3.9`
* make `3.81`
* git `latest`
* pycharm `latest`

## Commands

### Install dependencies

    make init

### Run python script to convert entire blog post(s) to epub

    pipenv run python main.py --dir /tmp --url '<<BLOG_URL>>/feeds/posts/default?alt=json'

example

    pipenv run python main.py --dir /tmp --url 'http://blogs.harishkannarao.com/feeds/posts/default?alt=json'

#### Other Url formats to filter the blogs

Filter blogs by text search

    '<<BLOG_URL>>/feeds/posts/default?alt=json&q=search_text'

Filter blogs by published date range

    '<<BLOG_URL>>/feeds/posts/default?alt=json&published-min=2020-01-01T00:00:00Z&published-max=2020-06-01T00:00:00Z'

Filter blogs by updated date range

    '<<BLOG_URL>>/feeds/posts/default?alt=json&updated-min=2020-01-01T00:00:00Z&updated-max=2020-06-01T00:00:00Z'

Filter blogs by categories

    '<<BLOG_URL>>/feeds/posts/default?alt=json&category=foo'

### Verify flake8

    make flake8
    
### Create requirements.txt

    make requirements
