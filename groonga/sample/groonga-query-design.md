# Groongaクエリーデザイン

## クエリ全体(一部変動)

```none
select \
--table "Scenario" \
--output_columns "id.capter,id.title,id.subtitle,id.episode,speaker,highlight_html(text),taps,background.name,id.type.name,expression.name,id.month.name,_key" \
--sort_keys "id.capter,_key" \
--command_version 2 \
--limit 10 \
--drilldowns[expression].keys "expression.name" \
--drilldowns[expression].sort_keys "id.capter,id.order,taps" \
--drilldowns[expression].limit 999999 \
--drilldowns[speaker].keys "speaker" \
--drilldowns[speaker].sort_keys "_key" \
--drilldowns[speaker].limit"] = 999999
--drilldowns[writer].keys "id.writer._key,id.writer.name" \
--drilldowns[writer].output_columns "_value.id.writer._key,_value.id.writer.name,_nsubrecs" \
--drilldowns[writer].sort_keys "_value.id.writer._key" \
--drilldowns[writer].limit 999999 \
--drilldowns[month].keys "id.month._key,id.month.name" \
--drilldowns[month].output_columns "_value.id.month._key,_value.id.month.name,_nsubrecs" \
--drilldowns[month].sort_keys "_value.id.month._key" \
--drilldowns[month].limit 999999
--drilldowns[type].keys "id.type._key,id.type.name" \
--drilldowns[type].output_columns "_value.id.type._key,_value.id.type.name,_nsubrecs" \
--drilldowns[type].sort_keys "_value.id.type._key" \
--drilldowns[type].limit 999999 \
--query 'text@"検索文字"'
--filter 'id.writer.name == "日日日" && id.type.name == "メイン"'
--offset 10
```

---

## Selectクエリ内容(オプション)

### テーブル指定

- [ドキュメント:table](http://groonga.org/ja/docs/reference/commands/select.html#table)

シナリオテーブルを指定

```none
--table Scenario
```

### 検索文字指定

- [ドキュメント:query](http://groonga.org/ja/docs/reference/commands/select.html#query)
  - [ドキュメント:クエリー構文](http://groonga.org/ja/docs/reference/grn_expr/query_syntax.html)

検索文字が複数ある場合

```none
--query 'text:@"検索文字１" + text:@"検索文字２"'
```

検索文字が１つの場合

```none
--query 'text:@"検索文字"'
```

### 出力カラム指定

- [ドキュメント:output_columns](http://groonga.org/ja/docs/reference/commands/select.html#output-columns)

内訳：チャプターID、タイトル、サブタイトル、エピーソード、話し手、内容、タップ回数(推定)、背景名、ストーリータイプ名、表現名、月名

```none
--output_columns "id.capter,id.title,id.subtitle,id.episode,speaker,highlight_html(text),taps,background.name,id.type.name,expression.name,id.month.name"
```

### 並び順

- [ドキュメント:sort_keys](http://groonga.org/ja/docs/reference/commands/select.html#select-sort-keys)

内訳：チャプターID、チャプター内順番、タップ回数

```none
--sort_keys "id.capter,id.order,taps"
```

### コマンドバージョン

- [ドキュメント:command_version](http://groonga.org/ja/docs/reference/command/command_version.html#command-version)

コマンドバージョン指定((highlight_htmlを使用するため)

```none
--command_version 2
```

### 出力レコードの最大値指定

- [ドキュメント:limit](http://groonga.org/ja/docs/reference/commands/select.html#limit)

出力数を10に設定

```none
--limit 10
```

### フィルター指定

- [ドキュメント:filter](http://groonga.org/ja/docs/reference/commands/select.html#search-condition-filter)

フィルタ複数指定された場合

```none
--filter 'id.writer.name == "日日日" && id.type.name == "メイン"'
```

フィルタが１のみの場合

```none
--filter 'id.writer.name == "日日日"'
```

### オフセット(ページ)指定

- [ドキュメント:offset](http://groonga.org/ja/docs/reference/commands/select.html#offset)

出力レコード開始位置(検索結果が出力件数以上の場合指定(10 * ページ数))

```none
--offset 20
```

## ドリルダウン系(複数項目使用)

### ドリルダウン項目指定

- [ドキュメント:drilldowns[${LABEL}].keys](http://groonga.org/ja/docs/reference/commands/select.html#drilldowns-label-keys)

ドリルダウンの項目として、ライターIDとライター名を指定

```none
--drilldowns[writer].keys "id.writer._key,id.writer.name"
```

### ドリルダウン出力カラム指定

- [ドキュメント:drilldowns[${LABEL}].output_columns](http://groonga.org/ja/docs/reference/commands/select.html#drilldowns-label-output-columns)

出力カラムとしてライターID、ライター名、集約数を指定

```none
--drilldowns[writer].output_columns "_value.id.writer._key,_value.id.writer.name,_nsubrecs"
```

### ドリルダウン並び順指定

- [ドキュメント:drilldown_sort_keys](http://groonga.org/ja/docs/reference/commands/select.html#drilldown-sort-keys)

並び順としてライターIDを指定

```none
--drilldowns[writer].sort_keys "_value.id.writer._key"
```

### ドリルダウングループ最大値指定

- [ドキュメント:drilldown_limit](http://groonga.org/ja/docs/reference/commands/select.html#select-drilldown-limit)

集約最大値を指定

```none
--drilldowns[writer].limit 999999
```
