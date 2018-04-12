#!/bin/bash

KEY_PATH=/tmp/key
echo -e $REMOTE_KEY > $KEY_PATH
chmod 700 $KEY_PATH
scp -R -o "StrictHostKeyChecking no" -i $KEY_PATH .:$REMOTE_USER@$REMOTE_HOSTNAME:~/dominion
ssh -o "StrictHostKeyChecking no" -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME ls -l ~/dominion
