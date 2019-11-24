#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:09:32 2019

@author: ingeborg
"""

# Import modules
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Create pandas dataframe from csv file 
df = pd.read_csv('unge_lovende.csv') 

# Get start time of first and last session in data set
firstVisitStartTime = datetime.fromtimestamp(df['visitStartTime'].min())
lastVisitStartTime = datetime.fromtimestamp(df['visitStartTime'].max())
print("\nThe first session started at: ", firstVisitStartTime)
print("The last session started at: ", lastVisitStartTime)

# Print first 5 rows of the starting dataframe
print("\nFirst 5 rows of the starting total dataset\n", df.head())

# Print description of the starting dataframe 
print("\nDescription of the starting total dataset\n", df.describe())

# Delete rows where timeWithinVisit = 0
df = df[df['timeWithinVisit'] != 0]

# Convert from unix timestamp to datetime
df['visitStartDatetime'] = pd.to_datetime(df['visitStartTime'],unit='s')
df['visitStartDate'] = df['visitStartDatetime'].dt.date
df['visitStartHour'] = df['visitStartDatetime'].dt.hour

# Add columns with duration in seconds and episodeEndTime
df['timeWithinVisitSeconds'] = df['timeWithinVisit']/1000
df['timeWithinVisitSeconds'] = df['timeWithinVisitSeconds'].round(0)

# Find unique programId's and create dataframe of subsets for each episode
unique_programIds = sorted(df['programId'].unique())
df_episode1 = df[df.programId == unique_programIds[0]].reset_index(drop=True)
df_episode2 = df[df.programId == unique_programIds[1]].reset_index(drop=True)
df_episode3 = df[df.programId == unique_programIds[2]].reset_index(drop=True)
df_episode4 = df[df.programId == unique_programIds[3]].reset_index(drop=True)
df_episode5 = df[df.programId == unique_programIds[4]].reset_index(drop=True)
df_episode6 = df[df.programId == unique_programIds[5]].reset_index(drop=True)
list_df_episodes = [df_episode1, df_episode2, df_episode3, 
                    df_episode4, df_episode4, df_episode6]

# Create lists of count of events per episode
count_total_events = [len(df_episode1.index), len(df_episode2.index), 
                        len(df_episode3.index), len(df_episode4.index), 
                        len(df_episode5.index), len(df_episode6.index)]
count_unique_userIds = df.groupby('programId')['userId'].nunique()
count_nonunique_userIds = count_total_events - count_unique_userIds

# Print count of events
print("\nTotal number of events in dataset: ", len(df.index))
print("Number of events with unique userIds: ", len(df['userId'].unique()))
print("Number of events per episode: ")
print(15*" ", "Total", 3*" ", "Unique userId", 2*" ", "Nonunique userId")
for i in range(len(unique_programIds)):
    print("    Episode %d: %6.d %13.d %18.d" % (i+1, count_total_events[i],
                                         list_df_episodes[i]['userId'].nunique(),
                                         count_nonunique_userIds[i]))

# Count of unique sessions and average number of events per session
count_unique_sessions = df['visitStartDatetime'].nunique()
print("Number of unique sessions: ", count_unique_sessions)
print("Averge number of events per session: %.1f" % 
      (len(df.index)/count_unique_sessions))

# Find number userIds with X registered events
print("\nCount of events per userId:")
events_per_userId = df.groupby('userId')['timeWithinVisit'].nunique()
print("Min:     %3d" % events_per_userId.min())
print("Mean:    %.1f" % events_per_userId.mean())
print("Median:  %3d " % events_per_userId.median())
print("Mode:", events_per_userId.mode())
print("Max:     %d" % events_per_userId.max())
print("Mode userId of user which have the most events:", df['userId'].mode())
count_events_per_userId = events_per_userId.value_counts().sort_index()
list_count_events_per_userId = [count_events_per_userId[1],
                                count_events_per_userId[2],
                                count_events_per_userId[3],
                                count_events_per_userId[4],
                                count_events_per_userId[5],
                                count_events_per_userId[6],
                                sum(count_events_per_userId[6:])]
print("Number of userIds with:")
for i in range(len(unique_programIds)):
    print("%5d registered event(s): %6d" % (i+1, list_count_events_per_userId[i]))
print("%5d+ registered event(s): %5d" % (i+1, list_count_events_per_userId[i+1]))

# Create sets of userIds for each episode
set_userId_episode1 = set(df_episode1['userId'])
set_userId_episode2 = set(df_episode2['userId'])
set_userId_episode3 = set(df_episode3['userId'])
set_userId_episode4 = set(df_episode4['userId'])
set_userId_episode5 = set(df_episode5['userId'])
set_userId_episode6 = set(df_episode6['userId'])

# Find intersection of userIds from all episodes
unique_userIds_all_episodes = set.intersection(set_userId_episode1, 
                                               set_userId_episode2, 
                                               set_userId_episode3, 
                                               set_userId_episode4, 
                                               set_userId_episode5, 
                                               set_userId_episode6)
print("\nNumber of users that have seen all 6 episodes:", 
      len(unique_userIds_all_episodes))

# Create dataframe of events where the user has seen all episodes
df_userId_all_episodes = df[df['userId'].isin(unique_userIds_all_episodes)]

# Print description of dataset with events where the users that have 
# seen all episodes
print("\nDescription of dataset with users that have seen all episodes")
print(df_userId_all_episodes.describe())

# Find number of episodes per session 
bingewatching_count = df_userId_all_episodes.groupby('visitStartDatetime')['programId'].nunique()
print("\nNumber if episodes per session when the users have seen all episodes")
print("Min:      %3d" % bingewatching_count.min())
print("Mean:     %.1f" % bingewatching_count.mean())
print("Median:   %3d" % bingewatching_count.median())
print("Mode: ", bingewatching_count.mode())
print("Max:      %3d" % bingewatching_count.max())
episodes_per_session = bingewatching_count.value_counts().sort_index()
print("Number of sessions with ")
for i in range(len(unique_programIds)):
    print("%5d episode(s) per session: %5d" % (i+1, episodes_per_session[i+1]))

#########
# Plots #
#########

# Comparison of total number of events with number of unique
# userIds per episode
fig, ax = plt.subplots()
bar_width = 0.25
episodes = ['Ep. 1', 'Ep. 2', 'Ep. 3', 'Ep. 4', 'Ep. 5', 'Ep. 6']
index = np.arange(len(unique_programIds))
rects1 = plt.bar(index, count_total_events, bar_width, 
                 color='b', label='Totalt')
rects2 = plt.bar(index + bar_width, count_unique_userIds, bar_width, 
                 color='g', label='Unike brukere')
plt.xlabel('Episode')
plt.ylabel('Antall eventer')
plt.title('Antall evener per episode')
plt.xticks(index + bar_width, episodes)
plt.legend()
plt.grid()
#ax.set_ylim(80000,120000)
plt.tight_layout()
plt.savefig('countOfEventsPerEpisode.png', dpi=300)
plt.show()

# Create plot of count of userIds that have more than one 
# session per episode
fig, ax = plt.subplots()
bar_width = 0.25
index = np.arange(len(unique_programIds))
rects1 = plt.bar(index, count_nonunique_userIds, bar_width, 
                 color='b', label='Brukere')
plt.xlabel('Episoder')
plt.ylabel('Antall brukere')
plt.title('Antall brukere som har sett episoden mer enn én gang')
plt.xticks(index, episodes)
plt.legend()
plt.grid()
plt.savefig('countOfNonUniqueUserIdsPerEpisode.png', dpi=300)
plt.show()

## Plot of number userId with X registered events
fig, ax = plt.subplots()
index = np.arange(1, 8)
bar_width = 0.25
plt.bar(index, list_count_events_per_userId)
plt.xlabel('Antall eventer per bruker')
plt.ylabel('Antall brukere')
plt.title('Antall brukere med gitt antall registrerte eventer')
plt.grid()
plt.xticks(rotation=0)
events = ["1", "2", "3", "4", "5", "6", "6+"]
plt.xticks(index, events)
plt.savefig('numUsersPerEventsPerUser.png', dpi=300)
plt.show()

# Plot of unique userId's per day
ax = df.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
plt.xticks(rotation=90)
plt.xlabel('Dato')
plt.ylabel('Antall unike brukere')
plt.title('Antall unike brukere per dato')
plt.tight_layout()
plt.savefig('uniqueUserIdsPerDay.png', dpi=300)
plt.show()

# Plot of unique userId's of each episode per day
ax = df_episode1.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
df_episode2.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
df_episode3.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
df_episode4.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
df_episode5.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
df_episode6.groupby('visitStartDate')['userId'].nunique().plot.line(grid=True)
ax.legend(["Episode 1", "Episode 2", "Episode 3", "Episode 4", "Episode 5", 
           "Episode 6"])
plt.xticks(rotation=90)
plt.xlabel('Dato')
plt.ylabel('Antall unike brukere')
plt.title('Antall unike brukere per episode per dato')
plt.tight_layout()
plt.savefig('uniqueUserIdsPerEpisodePerDay.png', dpi=300)
plt.show()

# Plot of unique userId's per hour
ax = df.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
plt.xlabel('Time')
plt.ylabel('Antall unike brukere')
plt.title('Antall unike brukere per time (UTC)')
plt.tight_layout()
plt.savefig('uniqueUserIdsPerHour.png', dpi=300)
plt.show()

# Plot of unique userId's of each episode per hour
ax = df_episode1.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
df_episode2.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
df_episode3.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
df_episode4.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
df_episode5.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
df_episode6.groupby('visitStartHour')['userId'].nunique().plot.line(grid=True)
ax.legend(["Episode 1", "Episode 2", "Episode 3", "Episode 4", "Episode 5", 
           "Episode 6"])
plt.xlabel('Time')
plt.ylabel('Antall unike brukere')
plt.title('Antall unike brukere per episode per time (UTC)')
plt.tight_layout()
plt.savefig('uniqueUserIdsPerEpisodePerHour.png', dpi=300)
plt.show()

# Plot of number of episodes per session where the user has seen all episodes
episodes_per_session.plot(kind='bar')
plt.xlabel('Antall episoder per sesjon')
plt.ylabel('Antall sesjoner')
plt.title('Antall episoder i hver sesjon blant brukerne som har sett alle episodene')
plt.grid()
plt.xticks(rotation=0)
plt.savefig('episodesPerSession.png', dpi=300)
plt.show()