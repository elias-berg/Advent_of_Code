.PHONY: 2024 create-template

create-template:
	python3 ./scripts/create_template.py

2024:
	python3 2024/manage.py runserver