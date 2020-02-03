FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y openssh-server
RUN apt-get -y install python3
RUN apt-get -y install  --upgrade python3-pip
RUN apt-get -y install cron

ADD requirements.txt /home/
RUN pip3 install -r /home/requirements.txt

## Configure Cron
# Add crontab file in the cron directory
ADD crontab /etc/cron.d/sshd-script-cron

# Give execution rights on the cron job
RUN chmod a+x /etc/cron.d/sshd-script-cron 

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo 'root:dnfjurfW$Gws' | chpasswd

RUN chown -R root.root /home/

RUN groupadd sftpg
RUN useradd -g sftpg sftpu -d /home/sftp
RUN echo 'sftpu:Sbotlo$93kg' | chpasswd
RUN mkdir -p /home/sftp/upload
RUN chown -R root.sftpg /home/sftp/
RUN chown -R sftpu.sftpg /home/sftp/upload

ADD ./sshd_config /etc/ssh/sshd_config
ADD ./homelab-266121-2d848d8d72d7.json /home/
ADD ./UploadFiles.py /home/
RUN chmod a+x /home/UploadFiles.py

ADD ./run.sh /home/
RUN chmod a+x /home/run.sh

RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd


EXPOSE 22

CMD /home/run.sh