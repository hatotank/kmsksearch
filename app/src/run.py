from flask import Flask
from flask import render_template, request, escape
from poyonga import Groonga
from flask_paginate import Pagination, get_page_parameter
import urllib

app = Flask(__name__)

# グローバル
app.jinja_env.globals['G_APP_TITLE'] = "Kmsksearch 君咲全文検索"

def delparameter(filtername,arg1):
  '''
  カスタムフィルタ：クエリ削除
  '''
  tmp = filtername.copy()
  try:
    del tmp[arg1]
  except:
    None
  return urllib.parse.urlencode(tmp)

def addparameter(filtername,arg1,arg2):
  '''
  カスタムフィルタ：クエリ追加
  '''
  tmp = filtername.copy()
  tmp[arg1] = arg2
  return urllib.parse.urlencode(tmp)

@app.route('/')
def index():
  '''
  ルートページ
  '''
  return render_template('_index.html')

@app.route('/search')
def kmsksearch():
  '''
  検索ページ
  '''
  # 初期化
  PER_PAGE = 10
  DRILLDROWN_LIMIT = 999999
  request_dict = {}
  groonga_query_dict = {}  
  query_para_dict = {}
  filter_dict = {}
  view_filter_list = []

  # フィルタ追加
  app.jinja_env.filters['delparameter'] = delparameter
  app.jinja_env.filters['addparameter'] = addparameter

  # リクエストパラメーター入れ替え
  request_dict['page']       = request.args.get(get_page_parameter(), 1, type=int)
  request_dict['word_no_sanitize'] =  request.args.get('word',       '', type=str)
  request_dict['word']       = escape(request.args.get('word',       '', type=str))
  request_dict['writer']     = escape(request.args.get('writer',     '', type=str))
  request_dict['type']       = escape(request.args.get('type',       '', type=str))
  request_dict['month']      = escape(request.args.get('month',      '', type=str))
  request_dict['speaker']    = escape(request.args.get('speaker',    '', type=str))
  request_dict['background'] = escape(request.args.get('background', '', type=str))
  request_dict['expression'] = escape(request.args.get('expression', '', type=str))
  request_dict['cancel']     = escape(request.args.get('cancel',     '', type=str))

  # 検索ワード存在チェックと禁止文字チェック
  if not request_dict['word']:
    return render_template('_index.html',message="検索キーワードを指定してください。")
  else:
    # ハピエレと日日日先生に怒られるので、一文字で以下の文字は検索させない
    # 全角：、。「」（）
    # 半角：()
    if len(request_dict['word']) == 1:
      forbidden_char_list = ['、','。','「','」','（','）','(',')']
      if request_dict['word'] in forbidden_char_list:
        return render_template('_index.html',message="検索できない文字が含まれています。")
    query_para_dict['word'] = request_dict['word']

  # グルンガのメインクエリ作成
  groonga_query_dict["table"] = "Scenario"
  groonga_query_dict["output_columns"] = "id.capter,id.title,id.subtitle,id.episode,speaker,highlight_html(text),taps,background.name,id.type.name,expression.name,id.month.name"
  groonga_query_dict["sort_keys"] = "id.capter,_key"
  groonga_query_dict["command_version"] = 2
  groonga_query_dict["limit"] = PER_PAGE
  groonga_query_dict["drilldowns[expression].keys"] = "expression.name"
  groonga_query_dict["drilldowns[expression].sort_keys"] = "_key"
  groonga_query_dict["drilldowns[expression].limit"] = DRILLDROWN_LIMIT
  groonga_query_dict["drilldowns[speaker].keys"] = "speaker"
  groonga_query_dict["drilldowns[speaker].sort_keys"] = "_key"
  groonga_query_dict["drilldowns[speaker].limit"] = DRILLDROWN_LIMIT
  groonga_query_dict["drilldowns[writer].keys"] = "id.writer._key,id.writer.name"
  groonga_query_dict["drilldowns[writer].output_columns"] = "_value.id.writer._key,_value.id.writer.name,_nsubrecs"
  groonga_query_dict["drilldowns[writer].sort_keys"] = "_value.id.writer._key"
  groonga_query_dict["drilldowns[writer].limit"] = DRILLDROWN_LIMIT
  groonga_query_dict["drilldowns[month].keys"] = "id.month._key,id.month.name"
  groonga_query_dict["drilldowns[month].output_columns"] = "_value.id.month._key,_value.id.month.name,_nsubrecs"
  groonga_query_dict["drilldowns[month].sort_keys"] = "_value.id.month._key"
  groonga_query_dict["drilldowns[month].limit"] = DRILLDROWN_LIMIT
  groonga_query_dict["drilldowns[type].keys"] = "id.type._key,id.type.name"
  groonga_query_dict["drilldowns[type].output_columns"] = "_value.id.type._key,_value.id.type.name,_nsubrecs"
  groonga_query_dict["drilldowns[type].sort_keys"] = "_value.id.type._key"
  groonga_query_dict["drilldowns[type].limit"] = DRILLDROWN_LIMIT
#  groonga_query_dict["drilldowns[background].keys"] = "background._key,background.name"
#  groonga_query_dict["drilldowns[background].output_columns"] = "_value.background._key,_value.background.name,_nsubrecs"
#  groonga_query_dict["drilldowns[background].sort_keys"] = "_value.background._key"
#  groonga_query_dict["drilldowns[background].limit"] = DRILLDROWN_LIMIT

  # ANDクエリ
  querystring = ''
  for i,v in enumerate(request_dict['word_no_sanitize'].strip().split()):
    if i > 0:
      querystring += ' + '

    querystring += 'text:@"{}"'.format(v)
  groonga_query_dict["query"] = querystring

  # グルンガのフィルタクエリ前処理(全解除の場合処理はしない)
  filter_pattern_dict = {
    'writer':'id.writer.name == "{}"',
    'type':'id.type.name == "{}"',
    'month':'id.month.name == "{}"',
    'expression':'expression.name == "{}"',
    'speaker':'speaker == "{}"',
#    'background':'background.name == "{}"',
  }
  if request_dict['cancel'] != 'on':
    for k in filter_pattern_dict:
      if request_dict.get(k):
        filter_dict[request_dict.get(k)] = filter_pattern_dict[k].format(request_dict.get(k))
        query_para_dict[k] = request_dict.get(k)

  # グルンガのフィルタクエリ作成と絞り込みメッセージ作成
  filter_msg = ""
  if filter_dict:
    groonga_query_dict['filter'] = ' && '.join(filter_dict.values())
    filter_msg = " ({}で絞り込み)".format('、'.join(filter_dict.keys()))

  # ページ処理用のクエリ文字作成
  query_string = urllib.parse.urlencode(query_para_dict)

  # グルンガのページクエリ作成
  if int(request_dict['page']) > 1:
    groonga_query_dict['offset'] = 10 * (int(request_dict['page'])-1)

  # グルンガ実行
  g = Groonga(host="groonga",protocol="gqtp",port=10043)
  cmds = [
    (
      "select", groonga_query_dict
    )
  ]
  for cmd, kwargs in cmds:
    ret = g.call(cmd, **kwargs)

  # グルンガ実行結果(ステータスコード0以外はエラー、件数が取得出来ない場合もエラー)
  if ret.status != 0:
    return render_template('_index.html',message="内部でエラー({})が発生しました。".format(ret.status))
  result = ret.body
  try:
    result_count = ret.body[0][0][0]
  except:
    return render_template('_index.html',message="内部でエラー({})が発生しました。".format(ret.status))

  # 共通系結果をセット
  common_dict = {
    'status':ret.status,
    'elapsed':ret.elapsed,
    'count':result_count,
    'word':request_dict['word'],
  }

  # 結果をセット
  records = []
  key = ['id','title','subtitle','episode','speaker','text','taps','background','type','expression','month','key']
  for lst in result[0][2:]:
    records.append(dict(zip(key,lst)))

  # 結果ドリルダウンをセット
  drilldown_pattern_dict = {
    'writer':['_order','writer','count'],
    'type':['_order','type','count'],
    'month':['_order','month','count'],
    'expression':['expression','count'],
    'speaker':['speaker','count'],
#    'background':['background','count'],
  }
  drilldown_records_dict = {}
  for pkey,plist in drilldown_pattern_dict.items():
    tmplist = []
    for glst in result[1][pkey][2:]:
      tmplist.append(dict(zip(plist,glst)))
    drilldown_records_dict[pkey] = tmplist

  # flask_paginate
  pagination = Pagination(
    page=request_dict['page'], 
    total=result_count,
    per_page=PER_PAGE,
    css_framework='bootstrap4',
    href="search?page={}&" + query_string,
    record_name="「{}」".format(request_dict['word'].strip()),
    found=filter_msg,  # use filter
    display_msg="{record_name}で検索、<b>{total}</b> 件ヒット [<b>{start} - {end}</b> 件を表示]{found}"
  )

  return render_template('_search.html',
    pagination=pagination, # flask_paginate
    common_dict=common_dict,
    records=records,
    drilldown_records_dict=drilldown_records_dict,
    query_para_dict=query_para_dict
  )

if __name__ == '__main__':
  app.run()
