FROM groonga/groonga:latest

# Add the patch fix
COPY stack-fix.c /lib/

# Prepare the libraries packages
RUN set -ex \
    && apk add --no-cache  --virtual .build-deps build-base \
    && gcc  -shared -fPIC /lib/stack-fix.c -o /lib/stack-fix.so \
    && apk del .build-deps

# Time Zone
RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone \
    && apk del tzdata

# export the environment variable of LD_PRELOAD
ENV LD_PRELOAD /lib/stack-fix.so

RUN mkdir /mnt/groonga

ENTRYPOINT ["groonga","-p","10043","-s","-l","w","--log-path","/dev/stdout","--query-log-path","/dev/stderr","/mnt/groonga/db"]
