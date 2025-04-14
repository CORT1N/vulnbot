# VulnBot - A vulnerable Discord Bot

For the Hack In Time v2 that took place in my school (**ESGI**) organized by [Thom-Son](https://github.com/Thom-Son), I made this multi-step challenge based on the assumption that a developer left a Discord Bot in *debug mode*.

## Prerequisites

- a machine with Docker installed
- a Discord that you're owning or at least administrator
- a firewall or network solution allowing you to use VLAN capabilities

For the last one, that's because there is a network vlan tagging part in the challenge.

## Installation

You need to assign the Docker's VM an IP in another VLAN that the one where you're hosting your challenge/CTF.

For the time, just let all the traffic pass between these two VLANs.

```bash
git clone https://github.com/CORT1N/vulnbot.git
cd vulnbot
cp .env.example .env
```

After cloning the project, go to the [Discord Develop Portal](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications) and follow the path to create an application.

You can fill the **DISCORD_TOKEN** variable in the `.env` file that you created with the token that you get for the application.

You can now generate an invitation link for your bot, and invite it on your Discord Server. *Make sure when you do it to give it enough permissions*.

Create a **command_bot** or whatever channel and take it's ID in the second `.env` value.

Create an **hidden_bot** or whatever private channel, accessible by nobody by default, take it's ID in the third `.env` value.

You can set the **SERVER_IP** `.env` value to the IP that you assigned in another VLAN.

```bash
docker compose up -d --build
docker compose logs -f
```

You should be able to see `Connected as *****`.

Try to connect to the open ports for the challenge with telnet from another machine, in the CTF VLAN : **445**, **2222**. If you got any problem, make sure they are opened on your machine firewall and on your physical firewall.

For the last step, you need to provide DHCP for your CTF players's network in a VLAN, and allow routing to the VM's VLAN, but only if you're tagged (with also DHCP active in it).

## Resolution

Write-up in french [here](write-up/fr.md).
