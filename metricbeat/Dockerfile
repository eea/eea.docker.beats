FROM docker.elastic.co/beats/metricbeat:6.3.1
USER root
RUN mv /usr/local/bin/docker-entrypoint /usr/local/bin/metricbeat-entrypoint 
COPY docker-entrypoint /usr/local/bin/docker-entrypoint
COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml
