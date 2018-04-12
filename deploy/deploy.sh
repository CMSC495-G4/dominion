#!/bin/bash

KEY_PATH=/tmp/key
echo -e $REMOTE_KEY > $KEY_PATH
ssh -o "StrictHostKeyChecking no" -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME ls -l