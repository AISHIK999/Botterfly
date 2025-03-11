# Botterfly 🦋
## A telegram userbot for managing Telegram accounts

* Written Python and uses Telethon library
* If you have any suggestions, please connect with me on [Telegram](https://t.me/AISHIK999)

**The environments variables are:**
1. Telegram oriented variables
   Obtained from [Telegram](https://my.telegram.org/apps)

   Log in to get the following variables
    * **API_ID**
    * **API_HASH**
   
   Run `python3 sessionGen.py` to get the following variable

    * **STRING_SESSION**
```
pip install -r requirements.txt
```

```
python3 -m userbot
```

**To host the userbot in VPS, follow the instructions below:**
1. Clone the repository
    ```
    git clone https://github.com/AISHIK999/Botterfly.git templar
   ```
   ```
   cd templar
   ```
   Perform a test run
   ```
   python3 -m userbot
   ```
2. Install Docker Compose
    ```
    sudo sudo apt-get install docker-compose
    ```
3. Run the docker container
   ```
    sudo docker-compose up --build
   ```
   This command is to be run every time any changes are made to the repo (e.g., editing plugins, .env etc)
4. To stop the container, run the following command:
   ```
   sudo docker-compose stop
   ```
   To resume, use 
   ```
    sudo docker-compose start
   ``` 