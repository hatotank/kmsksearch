from poyonga import Groonga

g = Groonga(protocol="gqtp",port=10043)

files = {
         "Writers":"eg_grn_writers.json",
         "Months":"eg_grn_months.json",
         "Types":"eg_grn_types.json",
         "Backgrounds":"eg_grn_background.json",
         "Expressions":"eg_grn_expression.json",
         "Titles":"eg_grn_titles.json"
        }

for k,v in files.items():
  with open(v, encoding="utf-8") as f:
    data = f.read().replace('\n','')
    cmds = [
            ("load", {"table":k,"input_type":"json","values":data})
           ]

  for cmd, kwargs in cmds:
    ret = g.call(cmd, **kwargs)
    print(v,ret.status,ret.body)
    print("*" * 40)

files = ['eg_grn_scenario_1.json','eg_grn_scenario_2.json']

for v in files:
  with open(v, encoding="utf-8") as f:
    data = f.read().replace('\n','')
    cmds = [
            ("load", {"table":"Scenario","input_type":"json","values":data})
           ]

  for cmd, kwargs in cmds:
    ret = g.call(cmd, **kwargs)
    print(v,ret.status,ret.body)
    print("*" * 40)