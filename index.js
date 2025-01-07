const dotenv = require("dotenv");
dotenv.config();

const {
  Client,
  GatewayIntentBits,
  SlashCommandBuilder,
} = require("discord.js");

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers],
});

const rolesToRemove = [
  "⠀Айс - Отработка⠀",
  "⠀Дарина - Отработка⠀",
  "⠀Хан Максим - Отработка⠀",
  "⠀Нуржигит - Отработка⠀",
  "⠀Томирис - Отработка⠀",
  "⠀Карлыгаш - Отработка⠀",
  "⠀Айнура - Отработка⠀",
  "⠀Акбота - Отработка⠀",
  "⠀Ганибет - Отработка⠀",
  "⠀Жания - Отработка⠀",
  "⠀Айдар - Отработка⠀",
  "⠀Ермухаммет - Отработка⠀",
  "⠀Жолан - Отработка⠀",
  "⠀Алишер - Отработка⠀",
  "⠀Жибек - Отработка⠀",
  "⠀Тимофей - Отработка⠀",
  "⠀Асема - Отработка⠀",
  "⠀Елдос - Отработка⠀",
  "⠀Аружан - Отработка⠀",
  "⠀Бахтияр - Отработка⠀",
  "⠀Замирайлов Максим - Отработка⠀",
  "⠀Тахир - Отработка⠀",
  "⠀Диас - Отработка⠀",
]; // Roles to remove

client.on("ready", async () => {
  console.log(`Logged in as ${client.user.tag}!`);

  const guildId = "1325871677611184212"; // Replace with your guild ID
  const guild = client.guilds.cache.get(guildId);
  if (!guild) return console.log("Guild not found");

  const commands = [
    new SlashCommandBuilder()
      .setName("removeroles")
      .setDescription("Remove specific roles from all members"),
  ];

  try {
    await guild.commands.set(commands);
    console.log("Commands registered!");
  } catch (error) {
    console.error("Error registering commands:", error);
  }
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  if (interaction.commandName === "removeroles") {
    const guild = interaction.guild;
    const members = await guild.members.fetch();

    for (const member of members.values()) {
      for (const roleName of rolesToRemove) {
        const role = guild.roles.cache.find(
          (r) => r.name.toLowerCase() === roleName.toLowerCase()
        );
        if (role && member.roles.cache.has(role.id)) {
          try {
            await member.roles.remove(role);
          } catch (error) {
            console.error(
              `Error removing role from ${member.user.username}:`,
              error
            );
          }
        }
      }
    }

    interaction.reply(`Roles removed from members.`);
  }
});

client.login(process.env.TOKEN);
