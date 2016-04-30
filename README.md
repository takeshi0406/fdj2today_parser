# fdj2today_parser

[（株）不動産データ＆ジャーナル社の提供する不動産ニュースブログ](http://fdj2today.exblog.jp/)のRSSを簡単にチェックするためのPython3系のためのライブラリです

## Installation

```
pip install git+https://github.com/takeshi0406/fdj2today_parser
```

## Usage

次のようなコードで簡単にチェックすることができます。

``` python
import fdj2today_parser as fdj2
# 24時間前までの記事で紹介されているリンクを取得する
articles = fdj2.request_fudosan_articles(exec_span=24)

for a in articles:
    print(a['title'], a['urls'])
```
