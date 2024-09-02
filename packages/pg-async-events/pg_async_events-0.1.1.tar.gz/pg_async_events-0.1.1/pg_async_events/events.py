import json
import asyncio
import asyncpg

subscribers = {}
subscribers_lock = asyncio.Lock()

class PG:
    pass

pg = PG()

async def create_pool(db_config):
    return await asyncpg.create_pool(
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        host=db_config['host'],
        port=db_config['port'],
        min_size=db_config['max_connections'],
        max_size=db_config['max_connections']+1
    )

async def initialize(db_config):
    global pg
    pg.pool = await create_pool(db_config)
    pg.conn = await pg.pool.acquire()

async def ensure_pg_conn_ready():
    while not hasattr(pg, 'conn') or pg.conn is None:
        await asyncio.sleep(1)

async def notify_handler(connection, pid, channel, payload):
    message = json.loads(payload)
    async with subscribers_lock:
        for queue in subscribers[channel]:
            await queue.put(message)

async def add_listener(queue_name):
    try:
        await ensure_pg_conn_ready()
        await pg.conn.add_listener(queue_name, notify_handler)
    except asyncpg.exceptions.PostgresError as e:
        return

async def notify(queue_name, payload):
    # issue the NOTIFY command
    async with pg.pool.acquire() as conn:
        try:
            payload_str = json.dumps(payload).replace("'", "''")
            await conn.execute(f"NOTIFY {queue_name}, '{payload_str}'")
        except asyncpg.exceptions.PostgresError as e:
            return

async def subscribe(queue_name):
    global subscribers
    async with subscribers_lock:
        if queue_name not in subscribers:
            subscribers[queue_name] = []
            await add_listener(queue_name)

    queue = asyncio.Queue()

    async with subscribers_lock:
        subscribers[queue_name].append(queue)

    try:
        while True:
            message = await queue.get()
            yield message
    finally:
        async with subscribers_lock:
            subscribers[queue_name].remove(queue)
