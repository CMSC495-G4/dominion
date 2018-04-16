#!/bin/bash -ex

KEY_PATH=/tmp/key
REMOTE_PATH=/home/$REMOTE_USER/dominion

rm -rf coverage.xml __pycache__
echo -e $REMOTE_KEY > $KEY_PATH
chmod 700 $KEY_PATH

ssh -q -o "StrictHostKeyChecking no" -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME bash <<EOF
  sudo rm -rf $REMOTE_PATH
EOF

scp -q -r -o "StrictHostKeyChecking no" -i $KEY_PATH . $REMOTE_USER@$REMOTE_HOSTNAME:$REMOTE_PATH
ssh -q -o "StrictHostKeyChecking no" -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME bash <<EOF
  pushd $REMOTE_PATH/deploy
  bash run.sh
EOF

