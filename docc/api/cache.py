# coding=utf-8

from dogpile.cache import make_region

region = make_region().configure(
    'dogpile.cache.memory'
)
