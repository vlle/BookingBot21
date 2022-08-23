## BookingBot21

This is a Telegram bot for booking School Objects.

### Prerequisites:
1. Python 3.6+ version
2. bash shell
3. HTTP Token ID to paste in config/bot.ini

### How to build

1. Paste your BOT token in config/bot.ini (message @BotFather to get token)
2. Paste your admin id in config/bot.ini
3. ``cd prototype/``
4. ``./release.sh ``


### Basic UI
1. ``/start`` to start bot
2. ``/secret_admin`` to administrate users & bookings (view logic at `` app/handlers/settings.py``)
3. ``/change_login`` to.. change your login! 🥸
4. ``/cancel`` to get back to Main Menu

### Functionality

- It can book register bot users with their login & telegram id. 
- Bot stores Booking, User and Objects data in SQLite3 Database.
- Bot has regex to prohibit user from incorrect data. Almost everywhere 🙂
> 1. You can view Database structure in prototype/database/ folder.
> 2. Feel free to edit init_database.sh to adapt this bot to your objects.

### Room for improvements
- Currently bot can not show start_time & end_time of your bookings
- There is no reminder for user about his booking. But it should be easy to implement.
- Bot currently can't check if something was booked 🙁 oh well
- To book something you have to write HOURS. 
> 1. Good: 16-18, 19-20
> 2. Bad: 16-43, 19-29
- English translation. I am pretty lazy for this. 
> If you REALLY need translation: send me an email at ```workerco@student.21-school.ru```


### UI Showcase:
![Alt Text](ui_demo.gif)


### Code authors
- curtrika@student.21-school.ru: Nikita, author of database-related code
- arrowwhi@student.21-school.ru: Ivan, author of telegram main bot-logic
- kyneshal@student.21-school.ru: Ivan, support & Web UI author. He also made cool presentation about our project! Check it at ``presentation `` dir
- workerco@student.21-school.ru: Artemii, author of this repository & telegram-db integrator. I also made some cosmetical improvements & added secret_admin logic

