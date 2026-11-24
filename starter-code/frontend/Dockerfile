FROM nginx:stable-alpine

COPY index.html /usr/share/nginx/html/index.html
COPY scripts/ /usr/share/nginx/html/scripts/
COPY assets/ /usr/share/nginx/html/assets/
COPY nginx.conf /etc/nginx/conf.d/default.conf
