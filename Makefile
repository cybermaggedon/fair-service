
# Create version tag from git tag
VERSION=$(shell git describe | sed 's/^v//')
REPO=cybermaggedon/fair-service
DOCKER=docker

all: evs-fair build

build: evs-fair
	${DOCKER} build -t ${REPO}:${VERSION} -f Dockerfile .
	${DOCKER} tag ${REPO}:${VERSION} ${REPO}:latest

push:
	${DOCKER} push ${REPO}:${VERSION}
	${DOCKER} push ${REPO}:latest

