# kmsksearch - 君咲全文検索

## 概要

Groongaによる「あんさんぶるガールズ！！\~Memories~」のシナリオ本文を検索できるシステム

## 必要条件

Dockerコンテナで動きます

- [Docker](https://www.docker.com/) がインストールされていること
- [Docker Compose](https://docs.docker.com/compose/) がインストールされていること

### コンテナ内訳

- uwsgi
- nginx
- groonga

## 環境構築

### 手順1 : プロジェクトをコピー

```none
git clone https://github.com/hatotank/kmsksearch
```

※Groongaのデータベースは、作成済みのサンプルデータベース(約300M)を使用しています。

### 手順2 : 実行(docker-composeが動きます)

```none
cd kmsksearch
make run
```

### 手順3 : ブラウザから接続、検索

```none
http://localhost/kmsksearch/
```

### 手順4 : 終了(コンテナ終了)

```none
make stoprm
```

---

## Groongaコンテナのサンプルデータベースについて

Gronngaのコンテナはデータベースを新規作成せず、既存のデータベースをマウントし、読み込むようにしております。
したがって新規作成の場合は、先にGroongaのデータベースを作成しておく必要があります。
※説明上ファイルのパーミッション等は無視しております。

### 手順1 : Groongaをインストール

以下のドキュメントを元にインストール(OSはUbuntuを想定)

[http://groonga.org/ja/docs/install/ubuntu.html](http://groonga.org/ja/docs/install/ubuntu.html)

※**groonga-server-gqtp**パッケージを追加でインストールしてください。

### 手順2 : スキーマの作成とデータロード

Groongaのテーブル作成とデータロード(初回DDLでテーブル削除エラーが出ますが無視してください)

```none
systemctl start groonga-server-gqtp.service
cd kmsksearch/gronnga/sample
python3 kmsksearch_gqtp_sample_ddl.py
python3 kmsksearch_gqtp_sample_insert.py
```

※サンプルデータは[初咲](https://twitter.com/ktoruans)様の[EGSP](http://hirot.org/kmsk/egsp/)シナリオを使用しております。

- [みどりと石油王](http://hirot.org/kmsk/egsp/ppmqk6z5)
- [春風ななと忍び寄る影](http://hirot.org/kmsk/egsp/n8tfu3ke)

※君咲全文検索のスキーマ、クエリー詳細は以下を参照。

- [groonga-schema-design](./groonga/sample/groonga-schema-design.md)
- [groonga-query-design](./groonga/sample/groonga-query-design.md)

### 手順3 : 作成したデータベースをコピー

作成したデータベースをkmsksearch/gronnga/dbにコピー
コピー後、環境構築の手順2へ

```none
cp /var/lib/groonga/db/* kmsksearch/gronnga/db/
```

---

## 使えるかどうかのメモ集(2019/11/22現在)

- メモ1 : Docker Hub からgroonga/groongaを落としてサーバモード(-s オプション)で起動し検索をするとエラーとなる(テーブル作成等は正常に動作する)
  - --> こちらのページを参照 [http://okamuuu.hatenablog.com/entry/2017/11/13/185903](http://okamuuu.hatenablog.com/entry/2017/11/13/185903)