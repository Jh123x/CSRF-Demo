# CSRF Demo

A mini CSRF Demo to demonstrate the effects of CSRF

# Requirements

1. `Flask` install with `pip install flask`
1. `Flask-sqlalchemy` install with `pip install Flask-SQLAlchemy`

# How to use this Demo

1. Launch `app.py` within `victim.com` and `attacker.com`
1. Go the the url for `victim.com` (Default [`http://localhost:5000/`](http://localhost:5000/))
1. Login using one Alice's account (username: `alice` password: `helloworld`)
   - Note: Please do not logout
1. Go the url for `attacker.com` (Default [`http://localhost:4000/`](http://localhost:4000/))
1. Click on the button
1. You will be redirected to victim.com and 1000 will be transferred to Bob

# How to mitigate this?

- Create forms using [flask-WTF](https://flask-wtf.readthedocs.io/en/stable/quickstart.html#creating-forms)
- Make use of [flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) to use CSRF Tokens and embed them into your forms
  - For more information visit [the docs](https://flask-wtf.readthedocs.io/en/stable/csrf.html)

```python
# Enable it by doing
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

```html
<!-- Add the input below to your form-->
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
```
