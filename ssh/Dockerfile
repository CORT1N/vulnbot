FROM debian:12.10-slim

RUN apt-get update && \
    apt-get install -y openssh-server sudo

RUN mkdir /var/run/sshd

RUN useradd -m debug-user && \
    mkdir -p /home/debug-user/.ssh && \
    chown -R debug-user:debug-user /home/debug-user

COPY id_rsa.pub /home/debug-user/.ssh/authorized_keys

RUN chmod 700 /home/debug-user/.ssh && \
    chmod 600 /home/debug-user/.ssh/authorized_keys && \
    chown -R debug-user:debug-user /home/debug-user/.ssh

RUN sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/^#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

RUN echo 'debug-user ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

EXPOSE 2222

CMD ["/usr/sbin/sshd", "-D"]