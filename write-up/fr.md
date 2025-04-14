# VulnBot - A vulnerable Discord Bot

Ce Bot est divisé en 3 sous-challenges :

1. **Hack in Bot**
2. **Hidden Bot**
3. **Je s'appelle Broot**

*Le port 22 de la machine cible ne fait pas partie du challenge.*

## Hack In Bot

*Catégorie* : **Miscellanous**

*Ne laissez pas les développeurs déployer, par pitié...\
Notre développeur de bot agréé ESGI a encore frappé, et nous a laissé un magnifique bot sur le discord du CTF. Qu'est ce qui cloche chez lui ?*

**HINT** : `Debug mode`

Quand on arrive sur le Discord du CTF, on voit qu'un bot est en ligne. Sa decription de profil nous invite à utiliser la commande `.vuln_help` On voit aussi qu'un channel *command_bot* est ouvert.

On utilise donc la première commande, ce qui nous renvoie :

```md
[DEBUG]: This bot is currently in debug mode, some permissions are too permissive.
You can use .unlock in the command channel to get access to hidden channels.
```

On essaie donc `.unlock` qui nous donne effectivemment accès au channel *hidden_commands* qui nous était invisible jusqu'ici.

En refaisant `.vuln_help`, on se rend compte qu'on nous donne accès à plus de commandes ici :

```md
[DEBUG]: You are in the debug channel!
Here are the new commands you can use:
- .ls [option(s)]: List files in the current directory.
- .cat <file> : Displays the content of the specified file.
- .net : Displays the server's IP address.
```

Avec `.ls -la .`, on tombe sur un fichier **.creds** qu'on peut afficher avec `.cat .creds`, qui contient un combo *user:hash*.

Il suffit ensuite de `john` le MD5 avec **rockyou** pour obtenir le mot de passe, qui est notre premier flag.

## Hidden Bot

*Catégorie* : **Network**

*Bon, le développeur de notre bot a eu bonne conscience (et une claque du RP), donc au lieu de protéger sa machine, il a pris la décision de l'isoler dans le réseau.\
Obtenez son adresse IP, trouvez comment l'atteindre et enfin que faire de ces identifiants.*

**HINT** : `T'as déjà entendu parler de VLAN Tagging ?`

Premièrement, on doit obtenir l'IP où est hébergée le bot grâce à `.net` qu'on a vu plus tôt dans l'aide.

Avec ceci, on doit comprendre (entre le titre du challenge, la catégorie et la description) qu'il est dans un VLAN différent du nôtre. D'ailleurs, si on ne l'a pas encore compris, on le comprendra quand on essaie de ping la machine.

On doit donc **tagguer** son interface réseau dans le VLAN concerné (cela mets en avant un problème de configuration des flux qui autorisent tout d'un VLAN à l'autre, ce qui détruit l'utilité d'un VLAN).

- [Windows](https://woshub-com.translate.goog/configure-multiple-vlan-on-windows/?_x_tr_sl=auto&_x_tr_tl=fr&_x_tr_hl=fr)
- [MacOS](https://support.apple.com/fr-fr/guide/mac-help/mh15134/mac)
- **Linux** : Facile à trouver en documentation, par distribution

On peut tester que le **tagging** a fonctionné en réussissant à ping l'IP du bot.

Un fois cela fait, on voit grâce à `nmap` plusieurs ports ouverts : **445** (*SMB*), **2222** (*SSH*).

En tentant de se connecter grâce à `smbclient` au SMB avec les credentials obtenus dans le premier challenge, on trouve notre flag dans **.passwd**.

## Je s'appelle Broot

*Catégorie* : **Privilege Escalation**

*C'est bien beau tous ces fichiers sur la machine du bot, mais notre turbo-dev n'a pas l'air d'avoir laissé grand chose de plsu critique encore... Si ?*

Il nous faut un **shell**, la description est claire. On avait vu le port 2222 plus tôt, passons par là avec le même utilisateur que le SMB.

On se rend vite compte que l'authentification par mot de passe est désactivée.

### Easy Way Connection

En listant les fichiers, on ne voit qu'un PCAP qui pourrait être utile, mais en commençant la commande pour lister et en tabulant, on voit qu'on nous propose un autre dossier : `.deleted`, qui contient un **id_rsa** ! C'est une clé privée !

Il ne nous reste plus qu'à le download et l'intégrer avec `-i` à la commande de connection SSH pour être sur la machine.

### Hard Way Connection

Dans les fichiers on voyait un PCAP. En le téléchargeant et l'analysant, on se rend compte qu'un échange SMB a eu lieu, contenant une clé privée !

L'échange SMB n'étant pas chiffré, on reconstruit la clé (recherches à faire) afin de pouvoir l'utiliser avec `-i` dans la commande de connection SSH.

### Privilege Escalation

Après avoir réussi à se connecter au port 2222 avec l'utilisateur **debug-user**, on doit connaître nos droits avec `sudo -l`.

**NO PASSWD ALL** !!

On peut donc `sudo -i` pour passer root.

Le flag est dans `/root`.