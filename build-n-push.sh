#!/bin/bash
# $1 is the version
# $2 is the prefix

if [ "$#" -ne 2 ]; then
  echo "Incorrect parameters"
  echo "Usage: build.sh <version> <prefix>"
  exit 1
fi

VERSION=$1
PREFIX=$2
SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

"$SCRIPTDIR"/build.sh "$VERSION" "$PREFIX"

for DIR in "$SCRIPTDIR"/*; do
  if [ -d "$DIR" ] && [ -f "$DIR/Dockerfile" ]; then
    IMAGE=${DIR/$SCRIPTDIR\//}
    docker push "$PREFIX/$IMAGE:$VERSION"

    # Update the kubernetes files.
    echo "updating $IMAGE.yaml with image $PREFIX/$IMAGE:$VERSION"
    sed -i "" -e "s|image: .*$|image: $PREFIX/$IMAGE:$VERSION|" "$SCRIPTDIR/kubernetes/$IMAGE.yaml"
  fi
done
