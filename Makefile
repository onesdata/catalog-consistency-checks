py_dirs := app
py_files := $(wildcard app/*.py)

env_ok: requirements.txt
	rm -rf env env_ok
	python3 -m venv env
	env/bin/pip install -r requirements.txt
	touch env_ok

.PHONY: fmt
fmt: env_ok
	env/bin/isort -sp .isort.cfg $(py_files)
	env/bin/black $(py_files)

.PHONY: check
check: env_ok
	env/bin/python -m mypy \
		--no-implicit-optional \
		--check-untyped-defs \
		--ignore-missing-imports \
		$(py_dirs)
	env/bin/python -m flake8 --select F $(py_dirs)
	env/bin/isort  -sp .isort.cfg  --check $(py_files)
	env/bin/black --check $(py_files)

.PHONY: test
test: check
	env/bin/python -m unittest discover $(py_dirs) -p "*.py" -v

.PHONY: clean
clean:
	rm -rf env env_ok

gather_creds:
	mkdir -p in
	echo "https://hack-friday.myshopify.com/admin/api/2020-10" > in/APP_API_URL
	echo "08189d71376d02872a66bdc51446a789" > in/APP_API_KEY
	echo "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" > in/APP_API_PASSWORD
