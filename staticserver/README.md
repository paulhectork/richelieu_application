# STATICSSERVER

This is a super simple static file server. 

In development, files on a remote server are not available to the local app.
Instead of adding extra routes on the `backend` app that would oonly make sense
in the development context, this app serves as a local statics file server.

There are 2 routes:
- `/cartography/<filename>`: serve a cartography image
- `/iconography/<filename>`: serve an iconography image

Filenames are listed in the `Filename` table of the Richelieu database.

---

## Usage

In a shell (assuming that you have all your image files in `app/statics/`):

```bash
# install
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# run
python main.py
```

---

## License

GNU GPL 3.0
