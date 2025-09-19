.PHONY: fmt lint type test build

fmt:
\truff format

lint:
\truff check --fix --show-fixes

type:
\tmypy workflows

test:
\tpytest -q

build:
\techo "Build placeholders"
