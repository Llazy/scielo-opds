import time
from models import Alphabetical, Publisher, Book
from opds import LinkRel, ContentType, make_link
from pyramid.view import view_config

@view_config(route_name='root', renderer='opds')
def root(request):
    """ OPDS Catalog root /opds/
    """
    link = [make_link(LinkRel.SELF, ContentType.NAVIGATION, '/opds/')]
    entry = []
    entry.append({
        '_id': 'http://books.scielo.org/opds/new', 
        'title' : 'New Releases', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [make_link(LinkRel.NEW, ContentType.ACQUISITION, 
            '/opds/new')]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/publisher',
        'title' : 'Publishers', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [make_link(LinkRel.SUBSECTION, ContentType.NAVIGATION, 
            '/opds/publisher')]
        })
    entry.append({
        '_id': 'http://books.scielo.org/opds/alpha', 
        'title' : 'Alphabetical', 
        'updated' : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime()),
        'links' : [make_link(LinkRel.SUBSECTION, ContentType.NAVIGATION, 
            '/opds/alpha')]
        })
    return {'entry': entry, 'links': link}


@view_config(route_name='alpha_catalog', renderer='opds')
def alpha_catalog(request):
    """ OPDS Catalog Alpha /opds/alpha
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/alpha')]

    entry = []
    for alpha in Alphabetical.filter():
        alpha['links'] = [make_link(LinkRel.SUBSECTION, 
            ContentType.ACQUISITION, '/opds/alpha/{}'.format(alpha['_id']))]
        entry.append(alpha)

    return {
        '_id': 'http://books.scielo.org/opds/alpha',
        'title': 'SciELO Books - Alphabetical',
        'links': link,
        'entry': entry}

@view_config(route_name='alpha_filter', renderer='opds')
def alpha_filter(request):
    """ OPDS Alpha filter for books
    """
    alpha = request.matchdict['id']
    link = [make_link('up', ContentType.NAVIGATION, '/opds/alpha'),
        make_link('self', ContentType.NAVIGATION, 
            '/opds/alpha/{}'.format(alpha))]

    entry = []
    for book in Book.filter(filter_initial=alpha):
        book['links'] = [make_link(LinkRel.ALTERNATE, ContentType.ACQUISITION,
            '/opds/book/{}'.format(book['_id']))]
        entry.append(book)

    return {
        '_id': 'http://books.scielo.org/opds/alpha/{}'.format(alpha),
        'title': 'SciELO Books - Filter starting with "{}"'.format(alpha),
        'links': link,
        'entry': entry}

@view_config(route_name='publisher_catalog', renderer='opds')
def publisher_catalog(request):
    """ OPDS Catalog Publishers /opds/publisher
    """
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/publisher')]

    entry = []
    for pub in Publisher.filter():
        pub['links'] = [make_link(LinkRel.SUBSECTION, ContentType.ACQUISITION,
            '/opds/publisher/{}'.format(pub['_id']))]
        entry.append(pub)

    return {
        '_id': 'http://books.scielo.org/opds/publisher',
        'title': 'SciELO Books - Publishers',
        'links': link,
        'entry': entry}

@view_config(route_name='publisher_filter', renderer='opds')
def publisher_filter(request):
    """ OPDS Catalog Publisher filter for books
    """
    pub = request.matchdict['id']
    link = [make_link('up', ContentType.NAVIGATION, '/opds/publisher'),
        make_link('self', ContentType.NAVIGATION, 
            '/opds/publisher/{}'.format(pub))]

    entry = []
    for book in Book.filter(filter_publisher=pub):
        book['links'] = [make_link(LinkRel.ALTERNATE, ContentType.ACQUISITION,
            '/opds/book/{}'.format(book['_id']))]
        entry.append(book)

    return {
        '_id': 'http://books.scielo.org/opds/publisher/{}'.format(pub),
        'title': 'SciELO Books - Filter for publisher "{}"'.format(pub),
        'links': link,
        'entry': entry}


@view_config(route_name='new', renderer='opds')
def new(request):
    link = [make_link('up', ContentType.NAVIGATION, '/opds/'),
        make_link('self', ContentType.NAVIGATION, '/opds/new')]

    entry = []
    for book in Book.filter(sort='new'):
        book['links'] = [make_link(LinkRel.ALTERNATE, ContentType.ACQUISITION,
            '/opds/book/{}'.format(book['_id']))]
        entry.append(book)

    return {
        '_id': 'http://books.scielo.org/opds/new',
        'title': 'SciELO Books - New Releases',
        'links': link,
        'entry': entry}