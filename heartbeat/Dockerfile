FROM docker.elastic.co/beats/heartbeat-oss:6.8.3
USER root
RUN mv /usr/local/bin/docker-entrypoint /usr/local/bin/heartbeat-entrypoint 
COPY docker-entrypoint /usr/local/bin/docker-entrypoint
RUN chown heartbeat /usr/local/bin/docker-entrypoint \
  &&  mv /usr/share/heartbeat/heartbeat.yml /usr/share/heartbeat/heartbeat.default.yml \
  && touch /usr/share/heartbeat/heartbeat.yml \
  && chown heartbeat  /usr/share/heartbeat/heartbeat.*

USER heartbeat

