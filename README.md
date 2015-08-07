# smartnode-frontend
###install
* sudo apt-get install python-virtualenv
* cd smartnode && virtualenv venv
* pip install -r requirements.txt
* rethinkdb

###run
* rethinkdb(database:smartnode, table:mac)
* . venv/bin/activate && python main.py
### To do
* support MQTT, COAP and XMPP
* asynchronous
