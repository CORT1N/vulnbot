import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis un fichier .env
load_dotenv()

# Récupère le token depuis les variables d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

# Vérifie si le token est chargé
if not TOKEN:
    raise ValueError("Le token Discord n'a pas été trouvé dans les variables d'environnement !")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Nécessaire pour lire les messages

bot = commands.Bot(command_prefix='.', intents=intents, description="Utilisez .vuln_help pour voir les commandes disponibles !")

# public_channel_id = 1344793049145938091  # Remplace par l'ID du channel public
public_channel_id = 1346606488461906063  # Remplace par l'ID du channel public
# hidden_channel_id = 1344794668969361421  # Remplace par l'ID du channel caché
hidden_channel_id = 1346607100335358003  # Remplace par l'ID du channel caché

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Utilisez .vuln_help"))

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return
    
    # Ignorer les messages provenant de DMs
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send("Je ne peux pas répondre aux messages privés. Utilisez le serveur pour interagir avec moi.")
        return

    # Traitement normal des commandes si le message n'est pas un DM
    await bot.process_commands(message)

@bot.command(name="vuln_help")
async def vuln_help(ctx):
    """Commande qui informe sur comment obtenir l'accès au channel caché."""
    if ctx.channel.id == public_channel_id:
        await ctx.author.send("[DEBUG] : Ce bot est actuellement en mode debug, certaines permissions sont trop permissives. Vous pouvez utiliser `.unlock` dans le channel de commandes pour obtenir l'accès aux channels cachés.")
    elif ctx.channel.id == hidden_channel_id:
        await ctx.author.send("""
        [DEBUG] : Vous êtes dans le channel de débug ! Voici les nouvelles commandes disponibles :
        
        - `.ls [option(s)]` : Liste les fichiers dans le répertoire actuel courant. Prend des paramètres (-la).
        - `.cat <fichier>` : Affiche le contenu du fichier spécifié.
	- `.net : Affiche l'IP du serveur.
        """)
    else:
        await ctx.author.send("Vous ne pouvez utiliser cette commande que dans le channel bot-command !")
    
    # Suppression du message de commande après envoi du DM
    await ctx.message.delete()

@bot.command()
async def unlock(ctx):
    """Commande qui donne accès au channel caché."""
    if ctx.channel.id == public_channel_id:
        hidden_channel = bot.get_channel(hidden_channel_id)
        if hidden_channel:
            await ctx.author.send(f"[DEBUG] Accès accordé ! Vous pouvez maintenant voir : {hidden_channel.mention} et exécuter des commandes de débug. Attention, cette permission n'aurait pas dû être accordée...")
            await hidden_channel.set_permissions(ctx.author, read_messages=True)
        else:
            await ctx.author.send("Problème avec les channels cachés.")
    else:
        await ctx.author.send("Vous ne pouvez utiliser cette commande que dans le channel bot-command !")

    # Suppression du message de commande après envoi du DM
    await ctx.message.delete()

@bot.command()
async def ls(ctx, *args):
    """Commande disponible dans le channel caché pour lister les fichiers."""
    if ctx.channel.id == hidden_channel_id:
        if args:
            files = []
            for path in args:
                # Vérifie si l'argument est un répertoire ou fichier valide
                if os.path.exists(path):
                    if os.path.isdir(path):
                        files.extend(os.listdir(path))
                    else:
                        files.append(path)
                else:
                    files.append(f"[DEBUG] Le chemin spécifié n'existe pas : {path}")
            await ctx.author.send("\n".join(files) if files else "[DEBUG] Aucun fichier visible...")
        else:
            # Par défaut, liste les fichiers non cachés dans le répertoire courant
            files = [f for f in os.listdir('.') if not f.startswith('.')]
            await ctx.author.send("\n".join(files) if files else "[DEBUG] Aucun fichier visible...")
    else:
        await ctx.author.send("Vous n'avez pas accès à cette commande ici !")

    # Suppression du message de commande après envoi du DM
    await ctx.message.delete()

@bot.command()
async def cat(ctx, filename: str):
    """Commande pour afficher le contenu du fichier .creds uniquement si présent."""
    if ctx.channel.id == hidden_channel_id:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()

            # Vérifier la longueur du contenu et envoyer par morceaux si nécessaire
            max_length = 2000  # Discord limite les messages à 2000 caractères
            intro = f"[DEBUG] Lecture du fichier : {filename}\n"
            clean_content = content  # Contenu sans le formatage des backticks

            # Calculer la longueur maximale du contenu pour que le message entier tienne dans 2000 caractères
            max_content_length = max_length - len(intro) - 7  # 7 caractères pour les backticks et espaces

            # Découper le contenu en morceaux de taille appropriée
            for i in range(0, len(clean_content), max_content_length):
                chunk = clean_content[i:i + max_content_length]
                # Ajouter les backticks et l'introduction au message
                if i == 0:
                    # Ajouter les backticks seulement au début du premier message
                    await ctx.author.send(f"```{intro}{chunk}```")
                else:
                    # Pour les messages suivants, n'ajoute pas de backticks ni d'intro
                    await ctx.author.send(f"```{chunk}```")
        else:
            await ctx.author.send(f"[DEBUG] Le fichier {filename} n'existe pas ou n'est pas accessible.")
    else:
        await ctx.author.send("Vous n'avez pas accès à cette commande ici !")

    # Suppression du message de commande après envoi du DM
    await ctx.message.delete()

@bot.command()
async def net(ctx):
    """Commande qui envoie l'IP à l'utilisateur."""
    if ctx.channel.id == hidden_channel_id:
        await ctx.author.send("[DEBUG] Adresse IP du serveur : 10.11.0.3")
    else:
        await ctx.author.send("Vous n'avez pas accès à cette commande ici !")

    # Suppression du message de commande après envoi du DM
    await ctx.message.delete()

bot.run(TOKEN)
