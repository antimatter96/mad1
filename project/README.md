Make sure Python 3 is installed

Install all the requried dependecies

```bash
pip install -r requirements.txt
```

Migrate

```
flask db upgrade
```

Run

```
python3.9 app.py
```

The site is up and running at : `localhost:8080`

You can obtain a api token at `localhost:8080/generate_token`

API is defined in api.yml

Eg

```
curl --request GET \
  --url http://localhost:8080/api/list/1 \
  --header 'x-api-token: 76d1d29655361c8ec04623e40a2fecfacf742dbf43d4712a914c4e24f9b26fe8' \
```
