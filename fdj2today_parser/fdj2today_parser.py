import re
from time import mktime
from datetime import datetime, timedelta
import feedparser


def request_fudosan_articles(exec_span):
    instance = Parser()
    return instance.run(exec_span=exec_span)


class Parser:

    URL_REGEX = re.compile('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')

    def __init__(self):
        self._rss_url = 'http://rss.exblog.jp/rss/exblog/fdj2today/index.xml'

    def run(self, exec_span):
        self._set_target_time(exec_span)
        entries = self._get_entries()
        return self._parse_entries(entries)

    def _set_target_time(self, exec_span):
        self.target_time = datetime.now() + timedelta(hours=-exec_span)

    def _get_entries(self):
        rss = feedparser.parse(self._rss_url)
        return rss.entries

    def _parse_entries(self, entries):
        target_entries = filter(self._check_updated, entries)
        parsed_entries = (self._parse_each_entry(e) for e in target_entries)
        return self._flatten_to_links(parsed_entries)

    def _check_updated(self, entry):
        # TODO:: JSTへの対応をもうちょっとスマートにする
        updated_unixtime = mktime(entry.updated_parsed)+9*60*60
        updated_time = datetime.fromtimestamp(updated_unixtime)
        return updated_time >= self.target_time

    def _parse_each_entry(self, entry):
        detail = entry['summary_detail']['value']
        links = detail.split('<br />\n<br />\n')
        parsed_links = map(self._split_each_link, links)
        return (l for l in parsed_links if len(l['urls']) >= 1)

    def _split_each_link(self, link):
        return {
            'title': self._parse_title(link),
            'urls': self._find_urls(link)
            }

    def _parse_title(self, link):
        splits = link.split('●')
        raw_title = re.sub(r'(<p>|<br />\n|■)', '', splits[0])
        url_removed = self.URL_REGEX.sub('', raw_title)
        title = url_removed.replace('\u3000', ' ')
        return title.strip()

    def _find_urls(self, message):
        return self.URL_REGEX.findall(message)

    def _flatten_to_links(self, entries):
        for links in entries:
            for link in links:
                yield link
