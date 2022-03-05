<h2>Requirements: </h2>
<ul>
  <li><b>Python3</b></li>
  <li><b>Pip3</b></li>
</ul>

<br><br>
<h2>Getting started:</h2>
<b> - Create .env file</b>
<p>
  <i>Sample .env:</i><br>
  <hr>
TELEGRAM_BOT_API_TOKEN=<br>
ENVIRONMENT=local #or production<br>
DB_HOST=localhost<br>
DB_PORT=5432<br>
DB_NAME=<br>
DB_USER=<br>
DB_PASSWORD=<br>
GROUP=   # telegram group ID<br>
BOT_URL=t.me/<br>
<hr>
</p>
<br>
<code>$ mkdir files</code><br>
<code>$ mkdir files/photos</code><br>
<code>$ mkdir files/messages</code><br>
<code>$ mkdir files/payment</code><br>
<code>$ pip3 install -r requirements.txt</code><br>
<code>$ python3 manage.py migrate</code><br>
<code>$ python3 manage.py makemigrations app</code><br>
<code>$ python3 manage.py migrate app</code><br>
<code>$ python3 manage.py collectstatic</code><br>
<code>$ python3 manage.py createsuperuser</code><br>
<code>$ python3 manage.py runserver</code><br>
<br>
<hr color="black">
<br>
<h3>Running Bot:</h3>
<br>
<b> - In Local</b>
<blockquote>http://127.0.0.1:8000/{Your telegram bot token}</blockquote>
<b> - In Production </b>
<i>Setting webhook</i>
<blockquote>https://api.telegram.org/bot{Your telegram bot token}/setWebhook?url=https://{Your site url here}/{Your telegram bot token}</blockquote>
