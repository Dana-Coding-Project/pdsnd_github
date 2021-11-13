"""The purpose of this program is to take user input and explore bikeshare data from three major US cities. 
   The user can input responses based on the city, the month, and the day and analyze the data sets using those
   arguments. The ouput is both textual and visual."""

#python dependencies for this program
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import calendar
plt.style.use('fivethirtyeight')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! Please review the readme file \nfor more details on how this program works and references. ')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter your search city (chicago, new york city, or washington):").lower()
    while city not in ["chicago","new york city", "washington"]:
        city = input("Try again. Please choose either chicago, new york city, or washinton: ").lower()


    # get user input for month (all, january, february, ... , june)
    month = input("Enter your search month (all,january,february,march,april,may, or june):").lower()
    while month not in ["all","january","february","march","april","may","june"]:
        month = input("Try again. Please choose either all,january,february,march,april,may, or june: ").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter your search day (all,monday,tuesday,wednesday,thursday,friday,saturday,or sunday):").lower()
    while day not in ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
        day = input("Try again. Please choose either all,monday,tuesday,wednesday,thursday,friday,saturday,or sunday: ").lower()
    print('-'*40)
    print(city,month,day)
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

    # load data file into a dataframe
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

   #show user the filtered data based on the inputs
    raw = df.head(5)
    print (raw)
    print("Would you like to see more raw data?")
    ans = input("yes or no:").lower()
    i=10
    
    while ans == "yes" and i< len(df.index):
        print(df.head(i))
        i+=5
        ans = input("Still want more? yes or no:").lower()
    

    labels = df['User Type'].unique()
    values = df['User Type'].value_counts()
    fig, ax = plt.subplots()
    fig1=ax.bar(labels, values)
    ax.set_title("User Description For Selected Filters")
    
    plt.show(block=False)
    return df



"""Displays statistics on the most frequent times of travel."""
def time_stats(df,month):
    

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['start_hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df["month"].mode()[0]
    popular_month_name = calendar.month_name[popular_month]
    print(popular_month_name)
    print('*'*40)

    # display the most common day of week
    print(df["day_of_week"].mode()[0])
    print('*'*40)
    # display the most common start hour
    print(df["start_hour"].mode()[0])
    print('*'*40)
     
    if month == "all":
        labels = df['month'].unique()
        values = df['month'].value_counts()
        fig, ax = plt.subplots()
        fig2=ax.bar(labels, values)
        ax.set_title("The Most Popular BikeShare Month")
        plt.show(block=False)
    else:
        print("Single month thus no graph.")
     

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print(start_station)
    print('*'*40)    
    # display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print(end_station)
    print('*'*40)
    # display most frequent combination of start station and end station trip
    print("The most frequent start and stop station combination is:\n"+ (df["Start Station"]+ " and "+ df["End Station"]).mode()[0])
    print('*'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(total_travel_time)
    print('#'*40)

    # display mean travel time
    average_travel_time = df["Trip Duration"].mean()
    print(average_travel_time)
    print('#'*40)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df["User Type"].value_counts())
    print('~'*40)

    # Display counts of gender
    if city == "chicago" or city == "washington":
        gender_total = df["Gender"].value_counts()
        print(gender_total)
    print('~'*40)

    # Display earliest, most recent, and most common year of birth
    if city == "chicago" or city == "washington":
        youngest = df["Birth Year"].max()
        oldest = df["Birth Year"].min()
        average_year = df["Birth Year"].mode()[0]
        print(f"The earliest birth year is {oldest}, the most recent is {youngest}\n and the most common is {average_year}.")
    print('~'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        time_stats(df,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()