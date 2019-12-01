from poyonga import Groonga

g = Groonga(protocol="gqtp",port=10043)

cmds = [
        # table_remove
        ("table_remove", {"name":"Writers",     "dependent":"yes"}),
        ("table_remove", {"name":"Months",      "dependent":"yes"}),
        ("table_remove", {"name":"Types",       "dependent":"yes"}),
        ("table_remove", {"name":"Backgrounds", "dependent":"yes"}),
        ("table_remove", {"name":"Expressions", "dependent":"yes"}),
        ("table_remove", {"name":"Scenario",    "dependent":"yes"}),
        ("table_remove", {"name":"Titles",      "dependent":"yes"}),
        ("table_remove", {"name":"Terms",       "dependent":"yes"}),
        # table_create
        ("table_create", {"name":"Writers",     "flags":"TABLE_HASH_KEY", "key_type":"UInt32"}),
        ("table_create", {"name":"Months",      "flags":"TABLE_HASH_KEY", "key_type":"UInt32"}),
        ("table_create", {"name":"Types",       "flags":"TABLE_HASH_KEY", "key_type":"UInt32"}),
        ("table_create", {"name":"Backgrounds", "flags":"TABLE_HASH_KEY", "key_type":"UInt32"}),
        ("table_create", {"name":"Expressions", "flags":"TABLE_HASH_KEY", "key_type":"ShortText"}),
        ("table_create", {"name":"Scenario",    "flags":"TABLE_HASH_KEY", "key_type":"ShortText"}),
        ("table_create", {"name":"Titles",      "flags":"TABLE_HASH_KEY", "key_type":"UInt32"}),
        ("table_create", {"name":"Terms",       "flags":"TABLE_PAT_KEY",  "key_type":"ShortText", "default_tokenizer":"TokenUnigram", "normalizer":"NormalizerAuto"}),
        # column_create
        ("column_create", {"table":"Writers",     "name":"name",       "type":"ShortText"}),
        ("column_create", {"table":"Months",      "name":"name",       "type":"ShortText"}),
        ("column_create", {"table":"Types",       "name":"name",       "type":"ShortText"}),
        ("column_create", {"table":"Backgrounds", "name":"name",       "type":"ShortText"}),
        ("column_create", {"table":"Expressions", "name":"name",       "type":"ShortText"}),
        ("column_create", {"table":"Scenario",    "name":"id",         "type":"Titles",      "flags":"COLUMN_SCALAR"}),
        ("column_create", {"table":"Scenario",    "name":"speaker",    "type":"ShortText"}),
        ("column_create", {"table":"Scenario",    "name":"text",       "type":"ShortText"}),
        ("column_create", {"table":"Scenario",    "name":"background", "type":"Backgrounds", "flags":"COLUMN_SCALAR"}),
        ("column_create", {"table":"Scenario",    "name":"expression", "type":"Expressions", "flags":"COLUMN_SCALAR"}),
        ("column_create", {"table":"Scenario",    "name":"taps",       "type":"UInt32"}),
        ("column_create", {"table":"Titles",      "name":"type",       "type":"Types",       "flags":"COLUMN_SCALAR"}),
        ("column_create", {"table":"Titles",      "name":"capter",     "type":"UInt32"}),
        ("column_create", {"table":"Titles",      "name":"month",      "type":"Months",      "flags":"COLUMN_SCALAR"}),
        ("column_create", {"table":"Titles",      "name":"order",      "type":"UInt32"}),
        ("column_create", {"table":"Titles",      "name":"title",      "type":"ShortText"}),
        ("column_create", {"table":"Titles",      "name":"subtitle",   "type":"ShortText"}),
        ("column_create", {"table":"Titles",      "name":"episode",    "type":"ShortText"}),
        ("column_create", {"table":"Titles",      "name":"writer",     "type":"Writers",     "flags":"COLUMN_SCALAR"}),
        # column_create(Backgrounds,Titles)
        ("column_create", {"table":"Backgrounds", "name":"scenario_background", "flag":"COLUMN_INDEX", "type":"Scenario", "source":"background"}),
        ("column_create", {"table":"Titles",      "name":"scenario_id",         "flag":"COLUMN_INDEX", "type":"Scenario", "source":"id"}),
        # column_create(Terms)
        ("column_create", {"table":"Terms", "name":"scenario_text",    "flags":"COLUMN_INDEX|WITH_POSITION", "type":"Scenario",    "source":"text"}),
        ("column_create", {"table":"Terms", "name":"backgrounds_name", "flags":"COLUMN_INDEX|WITH_POSITION", "type":"Backgrounds", "source":"name"}),
        ("column_create", {"table":"Terms", "name":"titles_title",     "flags":"COLUMN_INDEX|WITH_POSITION", "type":"Titles",      "source":"title"}),
       ]

for cmd, kwargs in cmds:
  ret = g.call(cmd, **kwargs)
  if ret.status != 0:
    print(cmd,kwargs)
    print(ret.status)
    print(ret.body)
    print("*" * 40)
