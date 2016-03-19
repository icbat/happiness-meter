echo "### Installing bower via NPM ###"
npm install -g bower
echo "### Installing NPM dependencies ###"
npm install
echo "### Installing Bower dependencies ###"
bower install
echo "### Starting server ###"
python api/server.py --port $PORT --host 0.0.0.0
