# Introduction

![PUBG-Online-Tournament](https://user-images.githubusercontent.com/80305894/161854200-3f47bb34-65b5-4b3e-975e-8425e1c151ed.jpg)


PlayerUnknown's Battlegrounds (PUBG) is an online multiplayer battle royale game. Each match starts with players parachuting from a plane onto one of the four maps. Once they land, players can search buildings, ghost towns, and other sites to find weapons, vehicles, armor, and other equipment. 

  - Items are procedurally distributed throughout the map at the start of a match, with certain high-risk zones typically having better equipment. <br>
  - Killed players can be looted to acquire their gear as well.

Every few minutes, the playable area of the map begins to shrink down towards a random location, with any player caught outside the safe area taking damage incrementally, and eventually being eliminated if the safe zone is not entered in time.

Tournaments are a competitive option in PUBG which can have prizes such as in-game currency or real-world currency. For instance one tournament had a reward for the player with the most kills of $10,000. Due to the eSport presence and potential earnings, there is a strong motivation for players to get any competitive advantage possible, sadly, this can include cheating. 

([wiki](https://en.wikipedia.org/wiki/PUBG:_Battlegrounds))

<br>

# Goal

Using tournament summaries, the intent of this investigation is to statistically identify [cheating](https://www.gamesradar.com/pubg-cheats-explained/) in PUBG tournaments, specifically focusing on identifying accounts which employ *Aimbots*.

<br>

# Data Description

The dataset had a built in index which was removed since the dataframe the data was stored in has its own indexing.  Additionally, the data had both, screen names and account IDs for participants.  The a names column (PUBG IGN of the player associated with this participant) was dropped for further anonymity and redundancy of labeling. 


| **Column Names** | **Description** | 
| :-------: | :------- |
| DBNOs | Number of enemy players knocked. |
| assists | Number of enemy players this player damaged that were killed by teammates. |
| boosts | Number of boost items used. |
| damageDealt | Total damage dealt. *Note: Self inflicted damage is subtracted.* |
| deathType | The way by which this player died, or alive if they didn't. |
| headshotKills | Number of enemy players killed with headshots. | 
| heals | Number of healing items used. |
| killPlace | Ranking in match of number of enemy players killed. |
| killStreaks | Max number of enemy players killed in a short amount of time. |
| kills | Number of enemy players killed. |
| longestKill | Longest distance between player and player killed at time of death. *This may be misleading, as downing a player and driving away may lead to a large longestKill stat.* |
| playerId | Account ID of the player associated with this participant. |
| revives | Number of times this player revived teammates. |
| rideDistance | Total distance traveled in vehicles measured in meters. |
| roadKills | Number of kills while in a vehicle. |
| swimDistance | Total distance traveled by swimming measured in meters. |
| teamKills | Number of times this player killed a teammate. |
| timeSurvived |  Time survived in seconds. |
| vehicleDestroys | Number of vehicles destroyed. |
| walkDistance | Total distance traveled on foot measured in meters. |
| weaponsAcquired | Number of weapons picked up. |
| winPlace | This player's placement in the match. | 


For the above columns there are 375364 observations. These are player stats for all matches in 200 PUBG tournaments. Each row is a player's performance in a match. 

* This data covers 19316 different player accounts over the 200 tournaments.  <br>
    * This does not mean that there are 19316 unique players because individuals can own multiple accounts.  <br>
* The total number of players who use multiple accounts in tournament play is considered small compared to the total number of players so each account be considered independent of one another.<br>

The metrics are match totals for each player (with variable time in-play), making each performance metric recorded is an unknown function of time.  While the exact function of time is unknown, the relationship is assumed to be positive.  The longer a player is alive in a match, the more opportunities they will have to use/acquire items or fight opposing players. 

There are however edge cases which would cause identification issues while remaining a function of time. For example, since these are match totals, there is no differentiation between a player who had 5 knockdowns in 5 seconds versus a player who had 5 knockdowns in 5 minutes.    

To compensate for edge cases, metric rates are calculated and used to identify cheaters in place of raw totals.  For example, the metric DBNO changed from a quantity of players knocked down to the number of players knocked down per minute of play. 


<br>

# Cheating Identification 


### Aimbot
In order to find players using aimbots in-game, it is assumed that any player using this sort of cheat will perform better in a shorter amount of time.  This means that more of their kills will be recorded as headshots, they will have a higher knockdown rate, and they will be more proficient having a knockdown become a kill as well. 

In PUBG players are 'knocked down' before being killed.  When this happens, headshots are typically easier for all players due to the knocked down player becoming relatively stationary and defenseless.  This causes headshot kills alone to not be a sufficient metric for cheating detection.  

Since the first outcome of a firefight is being knocked down, anyone with an aimbot will have an advantage. Aimbots cause all shots to be headshots, and as a result players can take opposing players down faster.  Assuming players with this type of cheat want to be in skirmishes and triumph, they are unlikely to be passive players and avoid firefights.  This means while they are alive, cheating players are expected to take down more opposing players per second than non-cheating players. 

If a player performs outside the quantile bounds of these metrics, the account should be flagged and reviewed for cheating by a moderator to be potentially banned. 


### Data

Both kill rate and headshot rate are approximately normally distributed with minimal outlier influence.
This is seen by a skew and kurtosis values being close to 0.  However, DBNO rate had a postitive skew and a high kurtosis.  

With kill and headshot rates being normally distributed, the mean and standard deviation were used to define the probability distribution function. 
To compensate for the skew and outliers in DBNO rate, the median value was used in place of the mean, and the median absolute deviation in place of the standard deviation.


### Results

Over the 19316 player accounts, 86 were flagged as potential cheaters using the described methods.  These accounts have a 0.0125% probability or less of legitimately performing as recorded during tournament play when compared to the performance of the overall player base.  These accounts and their associated tournament matches should be investigated in further detail to determine a proper response by the game's administration.   

