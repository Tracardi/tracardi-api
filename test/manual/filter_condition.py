import asyncio

from tracardi.process_engine.tql.parser import Parser
from tracardi.process_engine.tql.transformer.filter_transformer import FilterTransformer


async def main():
    parser = Parser(Parser.read('grammar/filter_condition.lark'), start='expr')

    q = 'active != true'
    # tree = parser.parse('id = [1,2]')
    # tree = parser.parse("B not exists AND id = [1,2]")
    # tree = parser.parse("(a.e BETWEEN 1.3 AND 1 and c=1) or B not exists")
    tree = parser.parse(q)
    x = FilterTransformer().transform(tree)
    # x = await event_db.search(x)
    print(q)
    print(x)


asyncio.run(main())
