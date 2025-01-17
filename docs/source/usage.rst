=====
Usage
=====

Developing Your Bot
-----------------

1. Create your bot by subclassing ``AizyBot``
2. Implement your trading strategy in the ``bot_action`` method
3. Use the built-in ``TestEngine`` for local testing

Here's a minimal example:

.. code-block:: python

    from src.AizyBot import AizyBot
    from src.CandleData import CandleData

    class MyTradingBot(AizyBot):
        async def bot_action(self, candle: CandleData) -> None:
            # Your trading logic here
            if some_condition:
                await self.place_order("buy", quantity, price, "BTC/USD")

Local Testing
------------

Before deploying your bot, thoroughly test it using our ``TestEngine``:

.. code-block:: python

    from src.TestEngine import TestEngine

    async def main():
        # Test for 2 hours with 1-minute candles
        await TestEngine.test(
            MyTradingBot,
            duration=120,    # minutes
            interval=1       # minute candles
        )

    if __name__ == "__main__":
        import asyncio
        asyncio.run(main())

The TestEngine will:

* Simulate market conditions
* Execute your trading logic
* Provide performance metrics
* Help identify potential issues

Deploying to Aizy Platform
------------------------

Once your bot is tested and ready:

1. Visit the `Aizy Platform <https://aizy.app>`_
2. Log in to your account
3. Navigate to "My Bots" section
4. Click "Upload New Bot"
5. Follow the upload instructions
6. Set your rental price and terms

Your bot will be available for other traders to rent and use on their accounts. You'll earn passive income from rental fees while helping other traders succeed.

.. note::
    Make sure your bot follows our `best practices <https://docs.aizy.app/best-practices>`_ and `guidelines <https://docs.aizy.app/guidelines>`_ before uploading.

Monitoring Your Bot
-----------------

After deployment, you can:

* Track your bot's performance
* Monitor rental statistics
* Receive notifications about trades
* Update your bot as needed

Visit your `dashboard <https://aizy.app/dashboard>`_ to manage your bots and view earnings.
