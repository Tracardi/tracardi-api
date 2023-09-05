from pprint import pprint

import asyncio

from tracardi.process_engine.tql.parser import Parser
from tracardi.process_engine.tql.transformer.filter_transformer import FilterTransformer


async def main():
    parser = Parser(Parser.read('grammar/filter_condition.lark'), start='expr')

    q = ('consents.marketing.revoke exists')
    # q = '(app.bot = false AND aux = 1) OR x>0'
    # q = '(app.bot = false OR aux = 1 OR c=1) AND (x>0 AND a=1)'
    # tree = parser.parse('id = [1,2]')
    # tree = parser.parse("B not exists AND id = [1,2]")
    # tree = parser.parse("(a.e BETWEEN 1.3 AND 1 and c=1) or B not exists")
    tree = parser.parse(q)
    pprint(tree)
    x = FilterTransformer().transform(tree)
    # x = await event_db.search(x)
    print(q)
    pprint(x)


asyncio.run(main())
