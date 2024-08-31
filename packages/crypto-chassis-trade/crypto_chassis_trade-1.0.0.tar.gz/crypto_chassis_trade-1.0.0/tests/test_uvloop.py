import asyncio
import os
import sys
import traceback

import pytest

if os.name != "nt":
    import uvloop

from crypto_chassis_trade.core.exchanges.okx import Okx, OkxInstrumentType

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="uvloop does not support windows at the moment")


async def main():
    try:
        symbol = "BTC-USDT"
        okx = Okx(
            instrument_type=OkxInstrumentType.SPOT,
            symbols={symbol},
            subscribe_bbo=True,
            subscribe_order=True,
        )

        await okx.start()

        await okx.stop()

        asyncio.get_running_loop().stop()

    except Exception:
        print(traceback.format_exc())
        sys.exit(1)


def test_start_stop():
    loop = uvloop.new_event_loop()  # pylint: disable=possibly-used-before-assignment
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()


if __name__ == "__main__":
    test_start_stop()
