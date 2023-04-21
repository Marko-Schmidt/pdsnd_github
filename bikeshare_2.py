import time
import pandas as pd
import numpy as np
CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input
    while True:
        city = input("Which of the tree Cities do you want to explore (Chicago, New York or Washington): ").lower()
        if city in ["chicago", "new york", "washington"]:
            break
        else:
            print("Sorry but you requested a city out of scope. Please try again.")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month do you want to explore (where are data available for January to June or type in all): ").lower()
        if month in ["all", "january", "february", "march", "april", "may", "june"]:
            break
        else:
            print("Sorry but you requested a month that doesn´t exist. Please try again.")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of the week are you up to (type in all or specific day): ").lower()
        if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            break
        else:
            print("Sorry but you requested a day that doesn´t exist. Please try again.")
    print('-' * 40)
    return city, month, day
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month:', popular_month)
    
    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', popular_day_of_week)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    print('Most popular Start Station is:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('Most popular End Station is:', popular_end)

    # display most frequent combination of start station and end station trip
    popular_combination = df['Start Station'] + df['End Station'].value_counts().idxmax()
    print('Most popular combination of start station and end station ist:\n', popular_combination)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_sec = df['Trip Duration'].sum()
    total_time_hour = round(total_time_sec / 60 / 60 ,0)
    
    print('Bike user traveled {} hours in total.'.format(total_time_hour))

    # display mean travel time
    travel_mean_sec = df['Trip Duration'].mean()
    travel_mean_min = round(travel_mean_sec / 60 ,0)
    
    print('Bike user traveled {} minutes in average.'.format(travel_mean_min))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCounts of user types:\n',user_types)
    
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender Count:\n',gender)
    except KeyError:
        print('\nSorry, but for Washington where are no Gender data available.')

    # Display earliest, most recent, and most common year of birth
    try:
        earlist_birth = int(df['Birth Year'].min())
        print('\nThe earlist birth year of users is:',earlist_birth)
    
        recent_birth = int(df['Birth Year'].max())
        print('\nThe recent birth year of users is:',recent_birth)
    
        common_birth = int(df['Birth Year'].value_counts().idxmax())
        print('\nThe most common birth year of users is:',common_birth)
    except KeyError:
        print('Unfortnatly we do not have birth dates as well.\n')
              
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    

def display_data(df):
    """Gets user access to raw data."""
    x = 0
    while True:
        display_raw_data = input('\nPlease type "yes" if you would you like to see 5 rows of data?\n')
        
        if display_raw_data.lower() != 'yes':
            break
            
        else:
            x = x + 5
            print(df.iloc[x:x+5])
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        #print(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
    main()