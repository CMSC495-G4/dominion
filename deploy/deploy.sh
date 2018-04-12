#!/bin/bash -ex

KEY_PATH=/tmp/key
echo -e $REMOTE_KEY > $KEY_PATH
chmod 700 $KEY_PATH
scp -q -r -o "StrictHostKeyChecking no" -i $KEY_PATH .:$REMOTE_USER@$REMOTE_HOSTNAME:/home/$REMOTE_USER/dominion
ssh -q -o "StrictHostKeyChecking no" -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME ls -l /home/$REMOTE_USER/dominion
