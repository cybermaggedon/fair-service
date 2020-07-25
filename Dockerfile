
FROM fedora:32

RUN dnf install -y python3-pip && dnf clean all && \
	pip3 install pyfair scipy pandas matplotlib

COPY evs-fair /usr/local/bin/

EXPOSE 8080

CMD /usr/local/bin/evs-fair

