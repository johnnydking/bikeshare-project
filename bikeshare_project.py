import numpy as np
import pandas as pd



CITY_DATA = {'Chicago': 'chicago.csv', 'New York City': 'new_york_city.csv', 'Washington': 'washington.csv'}
#define functions
def load_data(city, month, day):
    print('Preparing dataframe!...', flush=True)
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All':
        df = df[df['month'] == month.title()]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]
    #below conditional statement adds columns for gender and birth year if dataframe is segmented to view washington.csv; to avoid exception if function user_stats is called
    if city == 'Washington':
        df.insert(7, 'Gender', '0')
        df.insert(8, 'Birth Year', 0)
    return df

def load_global():
    print('Preparing dataframe!...', flush=True)
    df1 = pd.read_csv('chicago.csv')
    df2 = pd.read_csv('new_york_city.csv')
    df3 = pd.read_csv('washington.csv')
    frames = [df1, df2, df3]
    df = pd.concat(frames)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    return df

def time_stats(month, day, hour):
    return ('Most rides occurred in {}, and the most common weekday was {}. The most common start hour was {}.'.format(month.mode()[0], day.mode()[0], hour.mode()[0]))

def station_stats(start, end):
    df['trip'] = start + " to " + end
    top_trip = df['trip'].mode()[0]
    top_count = len(df[df['trip'] == top_trip])
    return ('The most common start station was {}. \nThe most common end station was {}. \nThe most common trip was {} with {} total trips'.format(start.mode()[0], end.mode()[0], top_trip, top_count))

def duration_stats(duration):
    total = duration.sum()
    mean = duration.mean()
    return ('The total ride time for rides in the dataframe is {} seconds, or about {} hours.\nThe average ride time for riders was {} seconds, or about {} minutes.'.format(total, int(total // 3600), mean, int(mean // 60)))

def user_stats(type, gender, year):
    sub_total = len(type[type == 'Subscriber'])
    cust_total = len(type[type == 'Customer'])
    male_total = len(gender[gender == 'Male'])
    female_total = len(gender[gender == 'Female'])
    male_perc = int(male_total / (male_total + female_total +.0001) * 100)
    female_perc = int(female_total / (male_total + female_total + .0001) * 100)
    early_year = int(year.min())
    late_year = int(year.max())
    common_year = int(year.mode()[0])
    #conditional statements to address no gender or birth year values for washington
    if male_total == 0:
        male_total = 'not available'
    if female_total == 0:
        female_total = 'not available'
    if early_year == 0:
        early_year = 'not available'
    if late_year == 0:
        late_year = 'not available'
    if common_year == 0:
        common_year = 'not available'
    if male_perc == 0:
        male_perc = 'not available'
    if female_perc == 0:
        female_perc = 'not available'
    return('The total number of subscribers was {}\nThe total number of customers was {}\nThe number of male users was {}\nThe percentage of users that were male was {}%\nThe number of female users was {}\nThe percentage of users that were female was {}%\nThe earliest birth year was {}\nThe most recent birth year was {}\nThe most common birth year was {}'.format(sub_total, cust_total, male_total, male_perc, female_total, female_perc, early_year, late_year, common_year))

print('\nGreetings - let\'s explore bikeshare data! The first 6 months of 2017 are observed for three cities: Chicago, New York City and Washington.')
#loops and conditions to request and validate input; choose dataframe type, specify segment(s), call function, option to call additional function(s), restart with new dataframe or exit program
while True:
    while True:
        df_option = input('\nType global to create a dataframe with all data, or type segment to create a dataframe with segmented data: ').title()
        if df_option == 'Global':
            df = load_global()
            break

        if df_option == 'Segment':
            while True:
                c_input = input("\nWould you like to view data for Chicago, New York City or Washington?: ").title()
                cities = ['Chicago', 'New York City', 'Washington']
                if c_input in cities:
                    break
                elif print('\nSorry, can you please enter either Chicago, New York City or Washington?'):
                    break
            while True:
                m_input = input('Which month? January, February, March, April, May or June? (or type all to skip this segmentation): ').title()
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
                if m_input in months:
                    break
                elif print('\nSorry, please enter any month between January and June, or type all if you don\'t want to segment by month\n'):
                    break
            while True:
                d_input = input('Which day of the week (or type all to skip this segmentation): ').title()
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
                if d_input in days:
                    break
                elif print('\nSorry, can you enter a day of the week - Monday through Sunday? Or type all if you don\'t want to segment by weekday\n'):
                    break
            df = load_data(c_input, m_input, d_input)
            break
        else:
            print('Sorry - can you type global or segment?')

    print('\nDone!\n')
    while True:
        print('\nChoose from the menu \n\n 1. A sample of the dataframe \n 2. Time Stats: most frequent times of travel \n 3. Station Stats: most popular stations and trips \n 4. Trip Duration Stats: total and average trip duration \n 5. User Stats: bikeshare users \n 6. Show me all stats!\n')
        while True:
            options = [1, 2, 3, 4, 5, 6]
            while True:
                try:
                    selection = int(input('Enter the number of the item you would like to view: '))
                    break
                except ValueError:
                    print('please enter an integer')

            if selection in options:
                break
            else:
                print('please enter an integer between 1 and 6')



        if selection == 1:
            print('\nHere\'s a sample of your data - the first 20 rows\n')
            print(df.head(20))


        if selection == 2:
            print('\n----------Time Stats----------\n')
            print(time_stats(df['month'], df['day_of_week'], df['hour']))

        if selection == 3:
            print('\n----------Station Stats----------\n')
            print(station_stats(df['Start Station'], df['End Station']))

        if selection == 4:
            print('\n----------Trip Duration Stats----------\n')
            print(duration_stats(df['Trip Duration']))

        if selection == 5:
            print('\n----------User Stats----------\n')
            print(user_stats(df['User Type'], df['Gender'], df['Birth Year']))

        if selection == 6:
            print('\n----------Time Stats----------\n')
            print(time_stats(df['month'], df['day_of_week'], df['hour']))
            print('\n----------Station Stats----------\n')
            print(station_stats(df['Start Station'], df['End Station']))
            print('\n----------Trip Duration Stats----------\n')
            print(duration_stats(df['Trip Duration']))
            print('\n----------User Stats----------\n')
            print(user_stats(df['User Type'], df['Gender'], df['Birth Year']))

        more = input('\nWould you like to see more from current dataframe?: ').title()
        while True:
            if more == 'No' or more == 'Yes':
                break
            if more != 'No' or more != 'Yes':
                print('Sorry, can you please type yes or no?')
                more = input('\nWould you like to see more from current dataframe?: ').title()
        if more == 'No':
            break
        if more == 'Yes':
            continue

    answer = input('\nType new to start over with a new dataframe, or type exit to quit the program\n').title()
    while True:
        if answer == 'New' or answer == 'Exit':
            break
        if answer != 'New' or answer != 'Exit':
            print('Sorry, can you please type new or exit?')
            answer = input(':').title()
    if answer == 'Exit':
        print('Thanks for stopping by!')
        break
    if answer == 'New':
        continue
