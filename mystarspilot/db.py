# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from github3.repos.repo import Repository
import kyotocabinet as kc
import json
import os
import re


class StarredDB(object):
    
    def __init__(self, star_pilot_home, mode):
        self._db = kc.DB()
        self._db_file = os.path.join(
            star_pilot_home, "mystars.kct#opts=sc#zcomp=gz")
        if mode == 'r':
            self._mode = kc.DB.OREADER
        elif mode == 'w':
            self._mode = kc.DB.OWRITER | kc.DB.OCREATE
        elif mode == 't':
            self._mode = kc.DB.OWRITER | kc.DB.OTRUNCATE
        
    def __enter__(self):
        
        self._db.open(self._db_file, self._mode)
        return self
        
    def __exit__(self, type, value, traceback):
        self._db.close()
        
    def _generate_key(self, domain, name):
        try:
            return u"{}:{}".format(domain, name)
        except UnicodeDecodeError:
            return u"{}:{}".format(domain, unicode(name, 'utf8'))
        
    def _calculate_ngrams(self, word, n):
      return [ u''.join(gram) for gram in zip(*[word[i:] for i in range(n)])]
    
    def _update_index(self, index_key, value_key):
        index = self._db.get(index_key)
        if index:
            if not value_key in index:
                self._db.append(index_key, "|{}".format(value_key))
        else:
            self._db.set(index_key, value_key)
            
    def _search_index(self, domain_prefix, term, search_results):
    
        index_key = self._generate_key(domain_prefix, term.lower())
        repo_keys = self._db.get_str(index_key)

        if repo_keys:
            for key in repo_keys.split('|'):
                search_results.append(key)
            
    def update(self, repository):
        
        full_name = repository.full_name
        name = repository.name
        language = repository.language
        description = repository.description
        
        repo_key = self._generate_key("r", repository.full_name)
        
        if language:
            lang_index_key = self._generate_key("idxl", language.lower())
            self._update_index(lang_index_key, repo_key)
            
        keywords = re.compile("[_\-]").split(name)
        if description:
            keywords += re.compile("[\s_\-]").split(description)
            
        for keyword in keywords:
            for n in range(2, len(keyword)+1):
                for word in self._calculate_ngrams(keyword, n):
                    keyword_index_key = self._generate_key("idxk", word.lower())
                    self._update_index(keyword_index_key, repo_key)
                    
        self._db.set(repo_key, json.dumps(repository.to_json()))
        
    def search(self, languages, keywords):
        
        language_results = []
        if languages:
            for search in languages:
                self._search_index("idxl", search, language_results)
        
        keywords_results = []
        if keywords:
            for keyword in keywords:
                for term in re.compile("[_\-]").split(keyword):
                    results = []
                    self._search_index("idxk", term, results)
                    keywords_results.append(results)
        
        if languages and keywords:
            # python > 2.6
            search_results = list(set(
                language_results).intersection(*keywords_results))  
        else:
            if len(keywords_results) > 1:
                # python > 2.6
                final_keywords_results = list(set(
                    keywords_results[0]).intersection(*keywords_results[1:]))  
            else:
                final_keywords_results = []
                for results in keywords_results:
                    for r in results:
                        final_keywords_results.append(r)
                        
            search_results = language_results + final_keywords_results
            
        repo_results = self._db.get_bulk_str(search_results)
        
        if repo_results:
            return [Repository(json.loads(repo)) for repo in repo_results.values()]
        else:
            return []
