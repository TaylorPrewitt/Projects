
library(tidyverse)
library(psych)
library(broom)
library(plyr)




# loading in data created from pubg_stats.py
pubg_stats = read.csv("pubg_player_stats.csv",
                      header=TRUE)

head(pubg_stats)

# Removing python index column and player names.
pubg_stats = pubg_stats %>% 
  dplyr::select(-X, -name)

# Looking at dimensions of dataframe and what columns are in it.
dim(pubg_stats)
names(pubg_stats)

# Inspecting dtypes for each column.
str(pubg_stats)

# Finding unique values and frequency for deathType and playerId
as.data.frame(table(pubg_stats$deathType))
length(unique(pubg_stats$playerId))



# Creating function to count any missing values in data
count_missing_vals = function(df) 
  
  #' params: df: DataFrame
  #'   Data to be parsed for any missing values. 
  #   
  #' return: missing_vals_df: DataFrame
  #'   Total number of missing values per column. 
  
  {missing_vals = c(0)
  dataset = df
  for (col in 1:ncol(dataset))
    {missing_vals = append(missing_vals, sum(is.na(dataset[,col])))}
    missing_vals = missing_vals[1:length(dataset)]
    missing_vals_df = data.frame(Variable = c(colnames(dataset)),
                                 NumMissing = missing_vals)
  return(missing_vals_df)}



# searching for missing values
count_missing_vals(pubg_stats)

# Inspecting preliminary descriptive statistics of metrics
pubg_stats %>%
  select_if(is.numeric) %>%
  describe()




# setting time unit
sec  = 60

# Creating a time invariant set with metrics for cheating identification.
# This has individual match data for each account.
pubg_eval = pubg_stats %>% 
  dplyr::select(boosts, heals, weaponsAcquired, 
                DBNOs, kills, headshotKills,
                timeSurvived, walkDistance, rideDistance,
                deathType, playerId) %>% 
  # boosts used per time unit survived
  mutate(boost_rate = boosts/(timeSurvived/sec)) %>% 
  # heal items used per time unit survived
  mutate(heals_rate = heals/(timeSurvived/sec)) %>% 
  # meters rode per time unit survived
  mutate(ride_rate = rideDistance/(timeSurvived/sec)) %>%
  # count of weapons picked up per time unit survived 
  mutate(weaponsAcquired_rate = weaponsAcquired/(timeSurvived/sec)) %>% 
  # proportion of kills that are headshots
  mutate(headshot_rate = (headshotKills)/kills) %>% 
  # proportion of kills per down
  mutate(kill_rate = (kills)/DBNOs) %>% 
  # downs per time unit survived 
  mutate(DBNO_rate = (DBNOs)/(timeSurvived/sec)) %>% 
  # meters walked per time unit survived
  mutate(walk_rate = walkDistance/(timeSurvived/sec)) %>% 
  dplyr::select(boost_rate, heals_rate, ride_rate,
                weaponsAcquired_rate, headshot_rate, kill_rate, DBNO_rate,
                walk_rate, deathType, playerId) 


# Zero division created some NaN values. A NaN in these instances=0
pubg_eval[is.na(pubg_eval)] = 0

# NaN check
count_missing_vals(pubg_eval)

# Some values from zero division are stored as 'Inf' not  NaN
pubg_eval[339478,1]

# Manually removing the instances and setting to zero. 
for (m in 1:nrow(pubg_eval)){
  for (n in 1:ncol(pubg_eval)){
    if (pubg_eval[m,n] == 'Inf') {
      pubg_eval[m,n] = 0
    }
  }
}

# Showing 'Inf' is changed
pubg_eval[339478,1]


# Aggregating over account so need to remove deathType.
pubg_account_group = pubg_eval %>% 
  dplyr::select(-deathType)

# Initializing list
player_grouping = list()

# For each column, get mean of metric rate for that particular account.
for (n in 1:(ncol(pubg_account_group)-1)){
  player_grouping[[n]] = aggregate(x = pubg_account_group[,n],               
                                   by = list(pubg_account_group$playerId),              
                                   FUN = mean)
}

# Convert to a df
player_grouping = data.frame(player_grouping)

# Removing duplicate acct columns
player_data = player_grouping[seq(2, length(player_grouping), 2)]
account_data = cbind(player_data, player_grouping$Group.1)

# Adding number of tournaments each account was observed
account_data = cbind(account_data, as.data.frame(table(pubg_eval$playerId))$Freq)

# Tidying column names for usability
colnames(account_data) = c(paste0("acct_", colnames(pubg_account_group)), "Freq")





# Metric stats
account_data %>% 
  dplyr::select(acct_headshot_rate, acct_kill_rate, acct_DBNO_rate) %>% 
  describe()


# Storing stats for filtering
DBNO = describe(account_data$acct_DBNO_rate)
kpd = describe(account_data$acct_kill_rate)
hs = describe(account_data$acct_headshot_rate)

# Setting p-value for threshold
p = 0.95

# Finding thresholds for each metric
dbno_limit = qnorm(p=p, mean = DBNO$median, sd = DBNO$mad)
kpd_limit = qnorm(p=, mean = kpd$mean, sd = kpd$sd)
hs_limit = qnorm(p=p, mean = hs$mean, sd = hs$sd)

vars = c("acct_DBNO_rate", "acct_kill_rate", "acct_headshot_rate")
cond = c(dbno_limit, kpd_limit, hs_limit)

# Filtering based on thresholds
suspect = account_data %>%
  filter(.data[[vars[[1]]]] > cond[[1]],
         .data[[vars[[2]]]] > cond[[2]],
         .data[[vars[[3]]]] > cond[[3]])


