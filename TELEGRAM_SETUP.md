# Telegram Setup

Do not put your bot token, API keys, or Telegram numeric user ID into this repository.

1. Open Telegram and message `@BotFather`.
2. Run `/newbot`.
3. Save the bot token privately, for example in a password manager.
4. Get your numeric Telegram user ID using `@userinfobot` or an equivalent trusted Telegram ID bot.
5. Run one of the installed Hermes gateway setup commands:

   ```powershell
   hermes gateway setup
   ```

   This equivalent setup section is also available:

   ```powershell
   hermes setup gateway
   ```

6. Enter the token only in the Hermes setup prompt or in Hermes' secure local config/env location. Do not paste it into source code.
7. Start the Hermes gateway in the foreground:

   ```powershell
   hermes gateway run
   ```

   `hermes gateway start` is for an installed background service. Use it only after running `hermes gateway install`.

   ```powershell
   hermes gateway install
   hermes gateway start
   ```

8. Send one test message to your Telegram bot.
9. Take a screenshot showing the bot reply.
10. Redact the token from all screenshots before submitting.

Useful checks:

```powershell
hermes gateway --help
hermes gateway status
```

