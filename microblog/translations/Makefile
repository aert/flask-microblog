
extract:
	cd ../; pybabel extract -F babel.cfg  -k lazy_gettext -o translations/messages.pot .

init:
	cd ../; pybabel init -i translations/messages.pot -d translations/ -l fr

update:
	cd ../; pybabel update -i translations/messages.pot -d translations/
