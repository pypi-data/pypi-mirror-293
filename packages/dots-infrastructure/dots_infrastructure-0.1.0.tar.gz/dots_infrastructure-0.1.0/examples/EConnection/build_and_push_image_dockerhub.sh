VERSION=0.0.1
REPOSITORY="dotsenergyframework/helics-example-charger"

docker build -f ../../DockerfileEConnection -t ${REPOSITORY}:${VERSION} ../../.

docker push ${REPOSITORY}:${VERSION}

