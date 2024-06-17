-- Installation Steps
pip install -R requirements.txt

-- Docker Steps for mock APIs
docker pull jaypeng2015/show-me-the-money
docker run -d -p 3000:3000 jaypeng2015/show-me-the-money

-- Run Server
uvicorn main:app --reload

-- API end point
http://127.0.0.1:8000/api/balance-sheet