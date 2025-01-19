Locally:

```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python app.py
```

Using Docker:

```
docker build -t weblog .
docker run -p 8000:8000 weblog
```