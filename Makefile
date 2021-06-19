all: generate

generate: tasks.py
	cp tasks.py tasks && chmod +x tasks

clean:
	rm tasks
