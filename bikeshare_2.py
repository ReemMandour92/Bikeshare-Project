import time
import sys
import numpy as np
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

# ------------------------------------------------------------------------------


def exit_if_input(exit_choice):
    """
    Exits the application any time user enters exit during input.
    """
    if(exit_choice.lower().strip() == 'exit'):
        print('\nApplication exits....\n')
        sys.exit()

# ------------------------------------------------------------------------------


def show_raw_data(df):
    """
    Displays raw data of 5 rows upon request.
    Takes dataframe variable
    Returns:
    First 5 rows and upon request next 5 until user stops.
    """
    hop = 0
    display = input('Do you want to view raw data? Enter y/n. ')
    if display.lower().strip() == 'y':
        print(df.head())
        display = input("view more? Enter y/n. ")
        while display.lower().strip() == 'y':
            hop += 5
            print(df.iloc[hop:hop+5])
            display = input("view more? Enter y/n. ")
    exit_if_input(display)
    print('Let\'s get to statistics calculations...\n\n')
    return df

# ------------------------------------------------------------------------------


def city_interaction_input():
    """
    Asks user to enter any of three cities: Chicago, New York, Washington.
    If user enters wrong city, the program rejects the input by printing
    invalid city name and asking for correct city.
    Returns:
    city name user wants to view analysis for.
    """
    # get user input for city (chicago, new york city, washington).
    city = input("""Please enter Chicago, New York, Washington to view\n""")
    # If user enter exit
    exit_if_input(city.lower().strip())
    # Use a while loop to handle invalid inputs
    while city.lower().strip() not in CITY_DATA.keys():
        print('Invalid city name.\n')
        print('Please rewrite your preferred city\n')
        city = input("Enter Chicago, New York, Washington\n")
        exit_if_input(city.lower().strip())
    return city


# ------------------------------------------------------------------------------


def interaction_choice(choice):
    """
    Interacts with user to enter specific month and/or day.
    Called and executed inside month_day_both_input function.
    Returns:
    specific month or day ex jan for January or sun for Sunday
    """
    months = np.array(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'exit'])
    days = np.array(['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'exit'])
    print('Which {}?\n'.format(choice))
    print('Please enter the first 3 letters of {}'.format(choice))
    if choice.lower().strip() == 'month':
        choice = str(input('ex: jan for January:\n'))
        while choice.lower().strip() not in months:
            choice = str(input('Please enter a valid 3 letter month:\n'))
            exit_if_input(choice)
    elif choice.lower().strip() == 'day':
        choice = str(input('ex: sun for Sunday:\n'))
        while choice.lower().strip() not in days:
            choice = str(input('Please enter a valid 3 letter day:\n'))
            exit_if_input(choice)
    exit_if_input(choice)

    return choice


# ------------------------------------------------------------------------------


def month_day_both_input(user_choice, choice):
    """
    Assigns month and day variables based on user input.
    Calls 'interaction_choice' function to take input from
    user.
    Returns:
    month and day values assigned after user enters the input.
    """
    month = ''
    day = ''
    # user_choice = user_choice.lower().strip()
    try:

        if user_choice == choice[0]:  # month
            month = interaction_choice(choice[0])
            day = 'all'
        elif user_choice == choice[1]:  # day
            day = interaction_choice(choice[1])
            month = 'all'
        elif user_choice == choice[2]:  # both
            print('Please write month followed by day. \n')
            month = interaction_choice(choice[0])
            day = interaction_choice(choice[1])
        elif user_choice == choice[3]:  # none
            month = 'all'
            day = 'all'
        else:
            print('you entered an invalid choice')
            print('you repeat your input\n')
    except Exception as e:
        print('Error occurred in month_day_both_input func: {}.'.format(e))
    return month, day

# ------------------------------------------------------------------------------


def filter_input():
    """
    choice is numpy array with choices available for user to choose from.
    choice = np.array(['month', 'day', 'both', 'none', 'exit']).
    returns month and day user input choices.
    """
    choice = np.array(['month', 'day', 'both', 'none', 'exit'])
    try:
        filter = input('Filter by month, day, both, or none \n')
        while filter.lower().strip() not in choice:
            print('you entered an invalid choice')
            filter = input('Filter by month, day, both, or none \n')
        exit_if_input(filter)
        month, day = month_day_both_input(filter.lower().strip(), choice)

    except Exception as e:
        print('error occurred in filter_input function {}'.format(e))
    return month, day

# ------------------------------------------------------------------------------


def start_app():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or
              "all" to apply no month filter
        (str) day - name of the day of week to filter by, or
              "all" to apply no day filter
    """
    try:
        print('Hello! Let\'s explore some US bikeshare data!')
        print('Type \'exit\' any time during input insertion to close app')
        city = city_interaction_input()
        print('_'*40)
    except Exception as e:
        print('error occurred due to incorrect input {}'.format(e))
    return city

# ------------------------------------------------------------------------------


def load_data(city):
    """
    Loads data for the specified city.

    Args:
        (str) city - name of the city to analyze
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour
        # df.drop(df.columns[[0]], axis=1, inplace=True)
        df.rename(columns={'Unnamed: 0': 'ID'}, inplace=True)
        return df
    except OSError:
        print('\nWrong or missing file\n')
        print('Please ensure all data files are correctly added')
        print('to project directory, and restart the app.')
        exit_if_input('exit')

# ------------------------------------------------------------------------------


def filtered_data(df, month, day):
    """
    Drop first column containing index(0, 1, 2, 3, ....)
    Rename first unamed column
    df is the loaded data frame
    (str) month - name of the month to filter by, or
          "all" to apply no month filter
    (str) day - name of the day of week to filter by, or
          "all" to apply no day filter
    Returns:
    Filtered data frame or same loaded dataframe, if 'all' is passed to
    variables month and day.
    """
    if month != 'all':
        month = month.lower().strip()
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        del months
    if day != 'all':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']
        found = [weekday for weekday in days if day.title() in weekday]
        df = df[df['day_of_week'] == found[0]]
        del found, days
    return df

# ------------------------------------------------------------------------------


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Filter is month
    if(month.lower() != 'all' and day.lower() == 'all'):
        common_day = df['day_of_week'].mode()[0]
        common_hour = df['hour'].mode()[0]
        # display the most common day of week
        print('The most common day of week: {}.\n'.format(common_day))
        # display the most common start hour
        print('The most common hour of day: {}\n'.format(common_hour))
    # Filter is day
    elif(month.lower() == 'all' and day.lower() != 'all'):
        common_month = df['month'].mode()[0]
        common_hour = df['hour'].mode()[0]
        # display the most common month
        print('The most common month: {}\n'.format(months[common_month-1]))
        # display the most common start hour
        print('The most common hour of day: {}\n'.format(common_hour))
    # Filter is both
    elif(month.lower() != 'all' and day.lower() != 'all'):
        common_hour = df['hour'].mode()[0]
        # display the most common start hour
        print('The most common hour of day: {}\n'.format(common_hour))
    # Filter is none
    else:
        common_month = df['month'].mode()[0]
        common_day = df['day_of_week'].mode()[0]
        common_hour = df['hour'].mode()[0]
        # display the most common month
        print('The most common month: {}\n'.format(months[common_month-1]))
        # display the most common day of week
        print('The most common day of week: {}.\n'.format(common_day))
        # display the most common start hour
        print('The most common hour of day: {}\n'.format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('_'*40)

# ------------------------------------------------------------------------------


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    pop_st_end = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('-'*40)
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station: {}\n'.format(popular_start_station))
    # display most commonly used end station
    print('The most common end station: {}\n'.format(popular_end_station))
    # display most frequent combination of start station and end station trip
    print('The most common combined stations: {}\n'.format(pop_st_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)

# ------------------------------------------------------------------------------


def format_Seconds_to_time(time_in_seconds):
    """
    Function to calculate time from large time_in_seconds

    Returns:
    day, hour, minutes, seconds
    """
    d = int(time_in_seconds // (24 * 60 * 60))
    time_in_seconds %= (24 * 60 * 60)
    h = int(time_in_seconds // (60 * 60))
    time_in_seconds %= (60 * 60)
    m = int(time_in_seconds / 60)
    time_in_seconds %= 60
    s = int(time_in_seconds)
    return d, h, m, s

# ------------------------------------------------------------------------------


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    print('-'*40)
    start_time = time.time()
    travel_dur = df['Trip Duration'].sum()
    avg_dur = df['Trip Duration'].mean()
    # display total travel time
    print('The total of trips\' duration: {}\n'.format(travel_dur))
    d, h, m, s = format_Seconds_to_time(travel_dur)
    print('which formats to: {} ds, {} hrs,  {} mins, {} secs\n'
          .format(d, h, m, s))
    # display mean travel time
    print('The average of trips\' duration: {}\n'.format(avg_dur.item()))
    d, h, m, s = format_Seconds_to_time(avg_dur)
    print('which formats to: {} ds, {} hrs,  {} mins, {} secs\n'
          .format(d, h, m, s))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)

# ------------------------------------------------------------------------------


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types are:\n{}'.format(user_types.to_string()))
    if city.lower().strip() != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('\n\nGenders are:\n{}'.format(gender.to_string()))
        # Display earliest, most recent, and most common year of birth
        earl_birth_year = df['Birth Year'].min()
        rec_birth_year = df['Birth Year'].max()
        com_birth_year = df['Birth Year'].mode()[0]
        print('\n\nThe earliest birth year is:\n{}'.format(earl_birth_year))
        print('\n\nThe most recent birth year is:\n{}'.format(rec_birth_year))
        print('\n\nThe repeated birth year is:\n{}'.format(com_birth_year))
    else:
        print('\n\nGender and Birth Year are not applicable for washington.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)

# ------------------------------------------------------------------------------


def main():
    restart = 'y'
    while restart.lower().strip() == 'y':
        city = start_app()
        print('\n{} data loading.....'.format(city.title().strip()))
        df = load_data(city.lower().strip())
        print('\n{} data loaded.\n'.format(city.title().strip()))
        show_raw_data(df)
        mon_day_filter = 'y'
        while mon_day_filter.lower().strip() == 'y':
            month, day = filter_input()
            data_filtered = filtered_data(df, month, day)
            # df.to_csv('load {}.csv'.format(city))
            # data_filtered.to_csv('load filtered {}.csv'.format(city))
            time_stats(data_filtered, month, day)
            station_stats(data_filtered)
            trip_duration_stats(data_filtered)
            user_stats(data_filtered, city)
            print('\nWould you like to filter more on {}?'
                  .format(city.title().strip()))
            mon_day_filter = input('\nEnter y/n. ')
            if mon_day_filter.lower().strip() != 'y':
                break
        restart = input('\nWould you like to restart? Enter y/n.\n')
        if restart.lower().strip() != 'y':
            break
    sys.exit()


if __name__ == "__main__":
    main()
