import asyncio
import os
import pprint
import sys
import time
import traceback

from crypto_chassis_trade.core.exchanges.okx import Okx, OkxInstrumentType
from crypto_chassis_trade.core.models.order import Order


async def main():
    try:
        # Default log level is WARNING. Here is how to change it:
        # logger = Logger(name="crypto_chassis_trade", level=LogLevel.TRACE)
        # ExchangeBase.set_logger(logger)

        symbol = "BTC-USDT"
        instrument_type = OkxInstrumentType.SPOT  # OkxInstrumentType.MARGIN
        margin_type = None  # MarginType.ISOLATED, MarginType.CROSS
        okx = Okx(
            instrument_type=instrument_type,
            symbols={symbol},  # a comma-separated string or an iterable of strings. Use '*' to represent all symbols that are open for trade.
            subscribe_bbo=True,
            # subscribe_trade= True,
            # fetch_historical_trade_at_start= True,
            # subscribe_ohlcv= True,
            # fetch_historical_ohlcv_at_start= True,
            subscribe_order=True,
            # fetch_historical_order_at_start= True,
            # subscribe_fill= True,
            # fetch_historical_fill_at_start= True,
            # subscribe_position= True,
            # subscribe_balance= True,
            is_demo_trading=True,  # https://www.okx.com/docs-v5/en/#overview-demo-trading-services
            api_key=os.environ.get("OKX_API_KEY", ""),
            api_secret=os.environ.get("OKX_API_SECRET", ""),
            api_passphrase=os.environ.get("OKX_API_PASSPHRASE", ""),
            margin_type=margin_type,
        )

        await okx.start()

        pprint.pp(okx.get_bbos())
        print("\n")

        client_order_id = str(int(time.time() * 1000))
        okx.create_order(
            order=Order(
                symbol=symbol,
                client_order_id=client_order_id,
                is_buy=True,
                price="10000",
                quantity=okx.get_all_instrument_information()[symbol].order_quantity_min,
            )
        )

        pprint.pp(okx.get_orders())
        print("\n")

        await asyncio.sleep(1)

        pprint.pp(okx.get_orders())
        print("\n")

        okx.cancel_order(symbol=symbol, client_order_id=client_order_id)
        await asyncio.sleep(1)

        pprint.pp(okx.get_orders())

        await okx.stop()
        asyncio.get_running_loop().stop()

    except Exception:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        asyncio.get_running_loop().stop()
