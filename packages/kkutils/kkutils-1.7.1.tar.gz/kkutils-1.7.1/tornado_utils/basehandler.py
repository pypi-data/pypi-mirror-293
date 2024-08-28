#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2018-04-14 14:21:15
'''

import copy
import datetime
import hashlib
import json
import logging
import math
import re
import time
import traceback
import urllib.parse
import uuid

import tornado.web
from bson import ObjectId
from utils import Dict, JSONEncoder, Motor, cached_property


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.logger = logging.getLogger()
        self.ua = self.request.headers.get('User-Agent', '')
        self.referer = self.request.headers.get('Referer', '')
        self.host = self.request.headers.get('Host', self.request.host)
        self.scheme = self.request.headers.get('Scheme', self.request.protocol)

    def _request_summary(self):
        return f"{self.request.method} {self.request.uri} ({self.ip}) ({self.referer})"

    def __getattr__(self, key):
        value = getattr(self.app, key)
        setattr(self, key, value)
        return value

    @staticmethod
    def get_domain(host):
        if re.match('https?://', host):
            host = urllib.parse.urlparse(host).netloc
        arr = host.split('.')
        if re.search(r'\.(com|net|gov|org|edu)\.(\w+)$', host):
            return '.'.join(arr[-3:])
        else:
            return '.'.join(arr[-2:])

    def check_referer(self, referers=None, allow_blank=True, raise_error=True, strict=False):
        referer = self.referer if strict else urllib.parse.urlparse(self.referer).netloc
        if not referer and allow_blank:
            return True

        if isinstance(referers, str):
            referers = [referers]

        for domain in referers:
            if domain.startswith('*.') and referer.endswith(domain[2:]):
                return True
            elif domain.startswith('*') and referer.endswith(domain[1:]):
                return True
            elif referer == domain:
                return True

        if raise_error:
            self.logger.warning(f'authorized referers: {referers}, referer: {self.referer}')
            raise tornado.web.HTTPError(403)
        else:
            return False

    def sign(self, url, prefix='digua', n=None):
        t = hex(int(time.time()))[2:]
        n = n or uuid.uuid4().hex[:8]
        s = hashlib.md5(f'{prefix}_{t}_{n}'.encode()).hexdigest()[:8]
        ret = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(ret.query)
        query['t'] = t
        query['n'] = n
        query['s'] = s
        url = urllib.parse.urlunparse((ret.scheme, ret.netloc, ret.path, ret.params,
                                       urllib.parse.urlencode(query, doseq=True), ret.fragment))
        return url

    def check_sign(self, prefix='digua', expire=3600):
        self.args.t = self.args.t[0] if isinstance(self.args.t, list) else self.args.t
        if not (self.args.t and self.args.n and self.args.s):
            raise tornado.web.HTTPError(403)

        if time.time() - int(self.args.t, 16) >= expire:
            raise tornado.web.HTTPError(403)

        key = f'{prefix}_{self.args.t}_{self.args.n}'.encode()
        if self.args.s[:8] != hashlib.md5(key).hexdigest()[:8]:
            raise tornado.web.HTTPError(403)

        return True

    async def del_cached_user(self, user=None):
        user = user or self.current_user
        self._cache.delete(f'{self.prefix}_user_{user.token}')
        self._cache.delete(f'{self.prefix}_user_{user.id}')

    async def get_cached_user(self, token=None, id=None):
        key = f'{self.prefix}_user_{token or id}'
        user = self._cache.get(key)
        if user:
            return user
        query = {'token': token} if token else {'id': int(id)}
        user = await self.db.users.find_one(query)
        if user:
            self._cache.set(key, user, 60)
        return user

    async def get_current_user(self):
        token = self.args.get('token', self.get_cookie('token'))
        if token and hasattr(self.app, 'db'):
            user = await self.get_cached_user(token=token)
            if user:
                if self.args.token and not self.get_cookie('token'):
                    self.set_cookie('token', self.args.token, expires_days=365)
                return user
        return Dict()

    async def prepare(self):
        self.current_user = await self.get_current_user()

    @cached_property
    def ip(self):
        if 'X-Forwarded-For' in self.request.headers:
            return self.request.headers['X-Forwarded-For'].split(',')[0]
        elif 'X-Real-Ip' in self.request.headers:
            return self.request.headers['X-Real-Ip']
        else:
            return self.request.remote_ip

    @cached_property
    def port(self):
        port = self.request.headers.get('X-Real-Port', '')
        if port.isdigit():
            return int(port)

    @cached_property
    def mobile(self):
        regexp = re.compile(r'Mobile|Android|iPhone|Windows Phone|iPad|Opera Mobi|iPod|UCBrowser|MQQBrowser|Quark|MicroMessenger', re.I)
        return True if regexp.search(self.ua) else False

    @cached_property
    def weixin(self):
        weixin_re = re.compile(r'MicroMessenger', re.I)
        return True if weixin_re.search(self.ua) else False

    @cached_property
    def cache_key(self):
        key = 'mobile' if self.mobile else 'pc'
        return f'{self.prefix}_{key}_{hashlib.md5(self.request.uri.encode()).hexdigest()}'

    def write(self, chunk):
        if isinstance(chunk, (dict, list)):
            chunk = json.dumps(chunk, cls=JSONEncoder)
            self.set_header('Content-Type', 'application/json')
        return super().write(chunk)

    def write_error2(self, status_code, **kwargs):
        if kwargs.get('exc_info'):
            msg = ''.join(traceback.format_exception(*kwargs["exc_info"]))
            self.logger.error(msg)
        super().write_error(status_code, **kwargs)

    def render(self, template_name, **kwargs):
        if self.get_argument('f', None) == 'json':
            self.finish(kwargs)
        else:
            super().render(template_name, **kwargs)

    @staticmethod
    def _convert(value):
        if re.match(r'^-?\d+$', value):
            return int(value)
        elif re.match(r'^-?\d+(\.?\d+)?$', value):
            return float(value)
        elif re.match(r'^true|false$', value.lower()):
            return value.lower() == 'true'
        else:
            return value

    @cached_property
    def args(self):
        return self.get_args()

    def get_args(self, **kwargs):
        if self.request.body and self.request.headers.get('Content-Type', '').find('application/json') >= 0:
            try:
                kwargs.update(json.loads(self.request.body))
            except Exception:
                self.logger.warning(self.request.body)

        for key, value in self.request.arguments.items():
            value = list(filter(None, map(lambda x: x.decode('utf8', 'ignore').strip(), value)))
            if value:
                kwargs[key] = value[0] if len(value) == 1 else value

        for key in ['page', 'size', 'order']:
            if kwargs.get(key) and isinstance(kwargs[key], str):
                kwargs[key] = self._convert(kwargs[key])

        self.args = Dict(kwargs)
        return copy.deepcopy(self.args)

    def add_args(self, **kwargs):
        ret = urllib.parse.urlparse(self.request.uri)
        query = urllib.parse.parse_qs(ret.query)
        query.update(kwargs)
        return urllib.parse.urlunparse((ret.scheme, ret.netloc, ret.path, ret.params,
                                        urllib.parse.urlencode(query, doseq=True), ret.fragment))

    def filter(self, query, include=[], exclude=[]):
        exclude = list(set(exclude) | set(['page', 'size', 'sort', 'order', 'f']))
        if include:
            query = dict(filter(lambda x: x[0] in include or x[0].startswith('$'), query.items()))
        query = dict(filter(lambda x: x[0] not in exclude, query.items()))
        return query

    def format(self, query, schema):
        for key, _type in schema.items():
            if not (isinstance(query.get(key), str) and _type in [int, float, ObjectId, datetime]):
                continue
            values = [x.strip() for x in query[key].strip().split('~')]
            if _type in [int, float, ObjectId]:
                values = [_type(v) if v else None for v in values]
            else:
                for i, value in enumerate(values):
                    if value:
                        value = re.sub(r'[^\d]', '', value)
                        value += (14 - len(value)) * '0'
                        values[i] = datetime.datetime.strptime(value, '%Y%m%d%H%M%S')
                    else:
                        values[i] = None
            if len(values) == 1:
                query[key] = values[0]
            else:
                if values[0] is not None and values[-1] is not None:
                    query[key] = {'$gte': values[0], '$lte': values[-1]}
                elif values[0] is not None:
                    query[key] = {'$gte': values[0]}
                elif values[-1] is not None:
                    query[key] = {'$lte': values[-1]}
        return Dict(query)

    async def _post_query(self, cursor, collection, query):
        if query:
            self.args.total = await getattr(self.db, collection).count_documents(query)
        else:
            self.args.total = await getattr(self.db, collection).estimated_document_count()
        self.args.pages = int(math.ceil(self.args.total / float(self.args.size)))
        return await cursor.to_list()

    def query(self, collection, query=None, projection=None, include=[], exclude=[], schema=None):
        schema = copy.deepcopy(schema or {})
        schema.setdefault('_id', ObjectId)
        query = copy.deepcopy(query or self.args)
        query = self.filter(query, include=include, exclude=exclude)
        query = self.format(query, schema)
        cursor = getattr(self.db, collection).find(query, projection)

        self.args.setdefault('order', -1)
        self.args.setdefault('page', 1)
        self.args.setdefault('size', 20)
        if self.args.sort:
            cursor = cursor.sort(self.args.sort, self.args.order)

        self.logger.info(f'{self.db.name}.{collection} query: {query}, sort: {self.args.sort}')
        cursor = cursor.skip((self.args.page - 1) * self.args.size).limit(self.args.size)

        if isinstance(self.db, Motor):
            return self._post_query(cursor, collection, query)
        else:
            if query:
                self.args.total = getattr(self.db, collection).count_documents(query)
            else:
                self.args.total = getattr(self.db, collection).estimated_document_count()
            self.args.pages = int(math.ceil(self.args.total / float(self.args.size)))
            return list(cursor)
