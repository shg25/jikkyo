# Jikkyo Tweet Tokenizer

## おことわり

- 2018年11月〜2022年4月に使ってたものを掘り出しているので何かと古い
- 2023年2月7日現在も使えることは確認済み
- 2023年2月9日に Twitter API が有料化されるので来週はもうダメかも

## 主な用途

- ラジオの実況ツイートを拾って形態素解析

## 環境

以下を`pip`で`install`
```
emoji                1.4.2
Janome               0.4.0.neologd20200813
pytz                 2022.5
requests-oauthlib    1.3.0
```

### 環境の補足

- `Janome`の`neologd`だけはファイルをDLしてきて`install`
- 2023年2月現在、NEologdの更新はもう止まってるみたいなので他の辞書を使った方が良さそう
- `Python 3.9.4`で動作確認した


## 準備

`config.py`を編集

- `CONSUMER_KEY` `CONSUMER_SECRET` `ACCESS_TOKEN` `ACCESS_TOKEN_SECRET`
  - Twitter API おなじみ四種の神器
  - Twitter Developer Platform から取得
- `SINCE` `UNTIL`
  - ツイート検索範囲
- `HASH_TAG`
  - 検索ワード
  - ハッシュタグじゃなくても大丈夫
- `OUTPUT_PATH`
  - どこのフォルダに書き出すか

## ツイート検索

以下を実行
```
python search.py
```

### 実行結果を確認

`OUTPUT_PATH`に以下のファイルが出力される

- `tweets.txt`
  - 1ツイート1行でツイート内容を出力
  - ハッシュタグ（検索ワード）は解析の邪魔になるので除去
- `tweets.csv`
  - 1ツイート1行でツイート内容+ユーザー名やツイートIDを出力
- `report.csv`
  - 簡易的なサマリーを出力


## 検索したツイートを形態素解析

以下を実行
```
python analysis.py
```

### 実行結果を確認

`OUTPUT_PATH`に`words.csv`ファイルが出力される

- `tweets.txt`を形態素解析した結果をカウント降順で表示
- 絵文字や「ｗｗｗｗ」みたいな邪魔なワードはプログラム内で除外している
