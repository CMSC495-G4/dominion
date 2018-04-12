#!/bin/bash

KEY_PATH=/tmp/key
echo -e $REMOTE_KEY > $KEY_PATH
ssh -i $KEY_PATH $REMOTE_USER@$REMOTE_HOSTNAME ls -l