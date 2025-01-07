ifeq (cmd, $(firstword $(MAKECMDGOALS)))
  runargs := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
  $(eval $(runargs):;@true)
  ifeq ($(runargs),)
	runargs := code-review bash
  endif
endif

build:
	docker build . -t code-review -f Dockerfile

run:
	docker compose up

restart:
	docker compose stop && docker compose up -d

stop:
	docker compose stop

cmd:
	docker compose run $(runargs)
