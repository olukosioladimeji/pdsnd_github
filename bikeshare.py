import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# we define a function to let us explore bikeshare for the three cities
def get_filters():
    """
    Please specify the city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # we create an empty city
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # we create an empty city
    city = ''
    # we run a loop to ensure correct user input
    while city not in CITY_DATA.keys():
        print("\nWelcome.Please choose city:")
        print("\n1.Chicago 2. New York City 3. Washington")
        print("\nInput accepted:\nFull name of city; not case sensitive(e.g new york city or NEW YORK CITY).\nFull name in title case(e.g. Chicago).")
        # we take user input in lower case
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nCheck your input")
            print("\nRestart")
    print("\nYou have chosen{city.title()} as your city.")
    # TO DO: get user input for month (all, january, february, ... , june)
    # we begin with setting a dictionary month_data and an empty month
    month_data= {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'all':7}
    month = ''
    while month not in month_data.keys():
        print("\nEnter the month,between January to june  for which you are seeking data")
        print("\nInput accepted:n\Full month name;not case sensitive(e.g february or FEBRUARY).\nFull month name in title case(e.g January).")
        print("\nView data for all the months with 'all'")
        month = input().lower()

        if month not in month_data.keys():
            print("\nInvalid input.")
            print("\nRestart.")
    print(f"\nYou choose {month.title()} as your month.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
     # we create a list to store days
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in day_list:
        print("\nEnter the day you are seeking data from:")
        print("\Input accepted:\nDayname;not case sensitve")
        print("\nView data for all the month with 'all'")
        day = input().lower()

        if day not in day_list:
          print("\nInvalid input.")
          print("\nRestart")

    print(f"\nYou choose {day.title()} as your day.")
    print(f"You choose data for city:{city.upper()}, month/s:{month.upper()} and day/s:{day.upper()}.")
    print('-'*50)
    return city, month, day

# we define a function to load data
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
    #we Load data for city
    print("\nData Loading:Please wait")
    df = pd.read_csv(CITY_DATA[city])

    #We convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #We now extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #We use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #We filter by month to create the new dataframe
        df = df[df['month'] == month]

    #We filter by day of week if applicable
    if day != 'all':
        #We filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #We now returns the selected file as a dataframe (df) with relevant columns
    return df

# we now define a function to calculate the time related statistics using the data chosen
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most common Month (1 = January,...,6 = June): {common_month}")

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"\nMost common day: {common_day}")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    common_start_hour = df['hour'].mode()[0]
    print(f"\nThe most common start hour: {common_start_hour}")


    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*60)

# we define a function to see statistics of the most popular city
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combination = df['Start To End'].mode()[0]
    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*60)

# we define a function for trip duration
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60) # duration in min & secs
    hour,minute = divmod(minute, 60) # duration in hour and minute
    # TO DO: display mean travel time
    # We now calculate the average trip duration using mean() in mins and secs and use the if,else statement to print time in hrs,mins and sec
    average_duration = round(df['Trip Duration'].mean())
    mins,sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nAverage trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nAverage trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*60)
# we define a function for bikeshare users statistics
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    user_type = df ['User Type'].value_counts()
    print(f"Types of users by number below:\n\n{user_type}")
    # TO DO: Display counts of gender
    # we use the try clause to display user by gender it should however be noted that the try clause ensure only df with birth year columns are displayed.
    try:
        gender = df['Gender'].value_counts()
        print(f"\nTypes of users by gender are given below:\n\n{gender}")
    except:
        print("\nNo 'Gender' column in this file.")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest year of birth: {earliest}\n\nMost recent year of birth: {recent}\n\nMost common year of birth: {common_year}")
    except:
        print("No birth year details in this file.")


    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*60)

# Wedefine a function for us to display the data
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    r_list = ['yes', 'no']
    rdata = ''
    #counter variable is initialized.
    counter = 0
    while rdata not in r_list:
        print("\nDo you want to see raw data?")
        print("\nResponses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user want to see it
        if rdata == "yes":
            print(df.head())
        elif rdata not in r_list:
            print("\nCheck your input.")
            print("Input does not seem to match responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user wants it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*60)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
