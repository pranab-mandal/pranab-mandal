# Setup (5 steps)

1. On GitHub create a **public repo named exactly `pranab-mandal`** (same as your username) and tick "Add a README".
2. Upload every file from this folder into it (keep `.github/workflows/update.yml` in that path).
3. Create a token: Settings > Developer settings > Personal access tokens (classic) > scopes `repo` and `read:user`.
4. In the repo: Settings > Secrets and variables > Actions > New secret > name `ACCESS_TOKEN`, paste the token.
5. Actions tab > "Update profile stats" > Run workflow. Stats refresh every 6 hours after that.

Change the text: edit `info()` in `build_svg.py`, then run `python build_svg.py`.
Change the portrait: `pip install pillow numpy opencv-python-headless rembg onnxruntime`, then `python make_ascii.py my_photo.jpg`
(tune COLS and CROP at the top of the file), then `python build_svg.py`.
