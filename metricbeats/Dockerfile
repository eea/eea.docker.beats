FROM docker.elastic.co/beats/metricbeat:6.3.0
USER root
RUN mv /usr/local/bin/docker-entrypoint /usr/local/bin/metricbeat-entrypoint 
COPY docker-entrypoint /usr/local/bin/docker-entrypoint
RUN chown metricbeat /usr/local/bin/docker-entrypoint \
  &&  chown metricbeat /usr/share/metricbeat/metricbeat.yml
USER metricbeat

