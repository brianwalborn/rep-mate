#!/bin/sh

# Replace only API_URL environment variable in config.js
# Using envsubst with explicit variable list to avoid substituting unintended variables
envsubst '${API_URL}' < /usr/share/nginx/html/config.js > /usr/share/nginx/html/config.js.tmp
mv /usr/share/nginx/html/config.js.tmp /usr/share/nginx/html/config.js

# Start nginx
nginx -g 'daemon off;'
