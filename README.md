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

## One Time PyCharm Setup

Setup `python` interpreter to virtual env as:

    Settings -> Project: <Project Name> -> Python Interpreter -> Add Interpreter -> Add Local Interpreter -> Select Existing -> Python -> <Project Root>/.venv/bin/python

To run `pytest` tests in `PyCharm`, make the project root directory as test root directory by

    Right Click Project Root directory -> Mark Directory As -> Test Sources Root

## Commands

### Install dependencies

    make init

### Run python script to convert entire blog post(s) to individual epubs

    pipenv run python main.py --dir /tmp --url '<<BLOG_URL>>/feeds/posts/default?alt=json'

example

    pipenv run python main.py --dir /tmp --url 'http://blogs.harishkannarao.com/feeds/posts/default?alt=json'

### Run python script to convert entire blog post(s) to single epub

    pipenv run python main.py --dir /tmp --single-file --name example_name --url '<<BLOG_URL>>/feeds/posts/default?alt=json'

example

    pipenv run python main.py --dir /tmp --single-file --name harish_blogs --url 'http://blogs.harishkannarao.com/feeds/posts/default?alt=json'

### Run python script to load individual blog post

    pipenv run python main.py --dir /tmp --load-individual-page --name example_name --url '<<BLOG_URL>>/feeds/posts/default?alt=json'

example

    pipenv run python main.py --dir /tmp --load-individual-page --name harish_blogs --url 'http://blogs.harishkannarao.com/feeds/posts/default?alt=json'

#### Other Url formats to filter the blogs

Filter blogs by text search

    '<<BLOG_URL>>/feeds/posts/default?alt=json&q=search_text'

Filter blogs by published date range

    '<<BLOG_URL>>/feeds/posts/default?alt=json&published-min=2020-01-01T00:00:00Z&published-max=2020-06-01T00:00:00Z'

Filter blogs by updated date range

    '<<BLOG_URL>>/feeds/posts/default?alt=json&updated-min=2020-01-01T00:00:00Z&updated-max=2020-06-01T00:00:00Z'

Filter blogs by categories

    '<<BLOG_URL>>/feeds/posts/default?alt=json&category=foo'

### Run tests

    make test

### Verify flake8

    make flake8
    
### Create requirements.txt

    make requirements

### Run all commands

    make run_all
