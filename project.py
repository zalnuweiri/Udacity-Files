import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago', 'chi', 'new york city', 'ny', 'nyc', 'washington', 'dc', 'was']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


    while True:
        city_select = input('What city would you like to view \nChicago, \nNew York City, \nor Washington? ').lower()
        if city_select.lower() in cities:
            city_confirm = input("You have selected " + city_select + " is that correct? (y/n) ").lower()
            if city_confirm.lower() == 'y':
                print(city_select)
                break
            elif city_confirm.lower() == 'n':
                city_select
            else:
                print("Sorry, we didn't understand that. Please input again.")
        else:
            print("Sorry, we don't have information on that city. Please input again.")


    while True:
        month = input("What month would you like to analyze (January Through June, or 'all')? ").lower()
        if month.lower() in months:
            confirmation = input("You have selected " + month + " is that correct? (y/n) ").lower()
            if confirmation.lower() == 'y'and month.lower() == 'all' :
                print(months[0:6])
                break
            elif confirmation.lower() == 'y':
                print(month)
                break
            elif confirmation.lower( )== 'n':
                month
            else:
                print("Sorry, that's not an option. Please input again.")
        else:
            print("Sorry, that's not an option. Please input again.")


    while True:
        day = input("What day would you like to analyze? (type 'all' for all days) ").lower()
        if day.lower() in days:
            day_confirm = input("You have selected " + day + " is that correct? (y/n) ").lower()
            if day_confirm.lower() == 'y' and day == 'all':
                print(days[0:7])
                break
            elif day_confirm.lower() == 'y':
                print(day)
                break
            elif day_confirm.lower() == 'n':
                day
            else:
                print("Sorry, we didn't understand that. Please input again.")
        else:
            print("Sorry, that option isn't included. Please input again.")

    print('-'*40)
    return city_select, month, day


def load_data(city_select, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city_select])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['End Time'].dt.month
    df['day_of_week'] = df['End Time'].dt.weekday_name
    df['hour'] = df['End Time'].dt.hour

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    most_common_month = df['month'].value_counts().idxmax()
    print("The month with the most travel is ", most_common_month)


    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("The day with the most travel is ", most_common_day)


    most_common_hour = df['hour'].value_counts().idxmax()
    print("The hour that the most travel starts at is ", most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_used_start_station = df['Start Station'].mode()[0]
    print("The most used start station is ", most_used_start_station)



    most_used_end_station = df['End Station'].mode()[0]
    print("The most frequently used end station is ", most_used_end_station)


    most_used_combo = most_common_combo = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most frequently used combination: \n{}".format(most_used_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    total_travel = df['Trip Duration'].sum()
    print("Total time spent traveling: ", total_travel)



    mean_travel = df['Trip Duration'].mean()
    print("Average travel time: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_type_count = df['User Type'].value_counts()
    print('The count of user types is \n{}'.format(user_type_count))



    if 'Gender' in df.columns:
        user_gender_count = df['Gender'].value_counts()
        print('The gender count is \n{}'.format(user_gender_count))
    else:
        print("Sorry, gender data is not included in this city's data collection.")


    if 'Birth Year' in df.columns:
        bday = df['Birth Year']
        earliest_bday = df['Birth Year'].min()
        youngest_bday = df['Birth Year'].max()
        mc_bday = df['Birth Year'].value_counts().idxmax()
        print('The birthday of the oldest user is: ',earliest_bday)
        print('The birthday of the youngest user is: ',youngest_bday)
        print('The most common birthday is: ',mc_bday)
    else:
        print('Sorry, birthday information is not collected in this city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    option_select = input('We have compiled data on the following \n "Time Stats", "Station Stats", "Trip Duration Stats", "User Stats", and "all" \nWhat set of information would you like to view? ').lower()
    if option_select == 'Time Stats'.lower():
        time_stats(df)
    elif option_select == 'Station Stats'.lower():
        station_stats(df)
    elif option_select == 'Trip Duration Stats'.lower():
        trip_duration_stats(df)
    elif option_select == 'User Stats'.lower():
        user_stats(df)
    elif option_select == 'All'.lower():
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
    else:
        print("Sorry, that's not an option. Please input again.")
        display_data(df)


def examine_more(df):
    while True:
        more_data = input('Would you like to observe your options for the same city and filters you selected? (y/n) ').lower()
        if more_data.lower() == 'y':
            display_data(df)
        elif more_data.lower() == 'n':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        examine_more(df)

        restart = input('\nWould you like to restart? (y/n).\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
