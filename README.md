# jitsi-meet-dnp
Dappnode package to self host a Jitsi meet instance https://jitsi.org/jitsi-meet/.


### Installation guide
[Source](https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-docker)

```
$ cp env.example .env
$ sh ./gen-passwords.sh
$ mkdir -p ~/.jitsi-meet-cfg/{web/letsencrypt,transcripts,prosody/config,prosody/prosody-plugins-custom,jicofo,jvb,jigasi,jibri}
$ docker-compose up -d
```

Open https://localhost:8443/

### TODO
Add support for:
- jigasi: Jigasi, the SIP (audio only) gateway.
- etherpad: Etherpad, shared document editing addon.
- jibri: Jibri, the broadcasting infrastructure.
