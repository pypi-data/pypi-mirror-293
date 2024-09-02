import asyncio
import contextlib
import multiprocessing

import pytest

from aioredis3.connection import Connection, ConnectionPool
from aioredis3.exceptions import ConnectionError

pytestmark = pytest.mark.asyncio


@contextlib.contextmanager
async def exit_callback(callback, *args):
    try:
        yield
    finally:
        await callback(*args)


@pytest.mark.xfail()
class TestMultiprocessing:
    # Test connection sharing between forks.
    # See issue #1085 for details.

    # use a multi-connection client as that's the only type that is
    # actually fork/process-safe
    @pytest.fixture()
    async def r(self, create_redis):
        redis = await create_redis(
            single_connection_client=False,
        )
        yield redis
        await redis.flushall()

    async def test_close_connection_in_child(self, master_host):
        """
        A connection owned by a parent and closed by a child doesn't
        destroy the file descriptors so a parent can still use it.
        """
        conn = Connection(host=master_host)
        await conn.send_command("ping")
        assert await conn.read_response() == b"PONG"

        def target(conn):
            async def atarget(conn):
                await conn.send_command("ping")
                assert conn.read_response() == b"PONG"
                await conn.disconnect()

            asyncio.get_event_loop().run_until_complete(atarget(conn))

        proc = multiprocessing.Process(target=target, args=(conn,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        # The connection was created in the parent but disconnected in the
        # child. The child called socket.close() but did not call
        # socket.shutdown() because it wasn't the "owning" process.
        # Therefore the connection still works in the parent.
        await conn.send_command("ping")
        assert await conn.read_response() == b"PONG"

    async def test_close_connection_in_parent(self, master_host):
        """
        A connection owned by a parent is unusable by a child if the parent
        (the owning process) closes the connection.
        """
        conn = Connection(host=master_host)
        await conn.send_command("ping")
        assert await conn.read_response() == b"PONG"

        def target(conn, ev):
            ev.wait()
            # the parent closed the connection. because it also created the
            # connection, the connection is shutdown and the child
            # cannot use it.
            with pytest.raises(ConnectionError):
                asyncio.get_event_loop().run_until_complete(conn.send_command("ping"))

        ev = multiprocessing.Event()
        proc = multiprocessing.Process(target=target, args=(conn, ev))
        proc.start()

        await conn.disconnect()
        ev.set()

        proc.join(3)
        assert proc.exitcode == 0

    @pytest.mark.parametrize("max_connections", [1, 2, None])
    async def test_pool(self, max_connections, master_host):
        """
        A child will create its own connections when using a pool created
        by a parent.
        """
        pool = ConnectionPool.from_url(
            f"redis://{master_host}", max_connections=max_connections
        )

        conn = await pool.get_connection("ping")
        main_conn_pid = conn.pid
        async with exit_callback(pool.release, conn):
            await conn.send_command("ping")
            assert await conn.read_response() == b"PONG"

        def target(pool):
            async def atarget(pool):
                async with exit_callback(pool.disconnect):
                    conn = await pool.get_connection("ping")
                    assert conn.pid != main_conn_pid
                    async with exit_callback(pool.release, conn):
                        assert await conn.send_command("ping") is None
                        assert await conn.read_response() == b"PONG"

            asyncio.get_event_loop().run_until_complete(atarget(pool))

        proc = multiprocessing.Process(target=target, args=(pool,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        # Check that connection is still alive after fork process has exited
        # and disconnected the connections in its pool
        conn = pool.get_connection("ping")
        async with exit_callback(pool.release, conn):
            assert await conn.send_command("ping") is None
            assert await conn.read_response() == b"PONG"

    @pytest.mark.parametrize("max_connections", [1, 2, None])
    async def test_close_pool_in_main(self, max_connections, master_host):
        """
        A child process that uses the same pool as its parent isn't affected
        when the parent disconnects all connections within the pool.
        """
        pool = ConnectionPool.from_url(
            f"redis://{master_host}", max_connections=max_connections
        )

        conn = await pool.get_connection("ping")
        assert await conn.send_command("ping") is None
        assert await conn.read_response() == b"PONG"

        def target(pool, disconnect_event):
            async def atarget(pool, disconnect_event):
                conn = await pool.get_connection("ping")
                async with exit_callback(pool.release, conn):
                    assert await conn.send_command("ping") is None
                    assert await conn.read_response() == b"PONG"
                    disconnect_event.wait()
                    assert await conn.send_command("ping") is None
                    assert await conn.read_response() == b"PONG"

            asyncio.get_event_loop().run_until_complete(atarget(pool, disconnect_event))

        ev = multiprocessing.Event()

        proc = multiprocessing.Process(target=target, args=(pool, ev))
        proc.start()

        await pool.disconnect()
        ev.set()
        proc.join(3)
        assert proc.exitcode == 0

    async def test_aioredis3_client(self, r):
        """A aioredis3 client created in a parent can also be used in a child"""
        assert await r.ping() is True

        def target(client):
            run = asyncio.get_event_loop().run_until_complete
            assert run(client.ping()) is True
            del client

        proc = multiprocessing.Process(target=target, args=(r,))
        proc.start()
        proc.join(3)
        assert proc.exitcode == 0

        assert await r.ping() is True
