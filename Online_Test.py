
#Importing required liraries
import csv
from datetime import datetime

#function find Which site_id has the largest number of unique users? And what's the number?
def largest_unique_user(country_id):
    unique_users = {}
    site_with_largest_users = []
    largest_users_sites = []
    with open("Adops & Data Scientist Sample Data - Q1 Analytics.csv", 'r') as file:
        site_logs = csv.DictReader(file)
        for access in site_logs:
            if country_id == access['country_id']:
                if access['site_id'] not in unique_users.keys():
                    unique_users[access['site_id']] = []

                unique_users[access['site_id']].append(access['user_id'])
                unique_users[access['site_id']] = list(set(unique_users[access['site_id']]))
                if not site_with_largest_users:
                    site_with_largest_users.append(access['site_id'])
                    largest_users_sites.append({
                        'site_id': access['site_id'],
                        'number_of_unique_users': len(unique_users[access['site_id']])
                    })
                else:
                    if len(unique_users[access['site_id']]) > len(unique_users[site_with_largest_users[0]]):
                        site_with_largest_users.clear()
                        largest_users_sites.clear()
                        site_with_largest_users.append(access['site_id'])
                        largest_users_sites.append({
                            'site_id': access['site_id'],
                            'number_of_unique_users': len(
                                unique_users[access['site_id']])
                        })
                    elif len(unique_users[access['site_id']]) == len(unique_users[site_with_largest_users[0]]):
                        if access['site_id'] not in site_with_largest_users:
                            site_with_largest_users.append(access['site_id'])
                            largest_users_sites.append({
                                'site_id': access['site_id'],
                                'number_of_unique_users': len(
                                    unique_users[access['site_id']])
                            })
                        else:
                            largest_users_sites[
                                site_with_largest_users.index(access['site_id'])].update({
                                'site_id': access['site_id'],
                                'number_of_unique_users': len(
                                    unique_users[access['site_id']])
                            })

    file.close()
    return largest_users_sites
    
# Function to Find these four users & which sites they (each) visited more than 10 times.    
def four_users(start_time, end_time, min_visits):
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    with open("Adops & Data Scientist Sample Data - Q1 Analytics.csv", 'r') as file:
        site_logs = csv.DictReader(file)

        sites_visited = {}
        visits = {}
        
        for access in site_logs:
            access_time = datetime.strptime(access['ts'], '%Y-%m-%d %H:%M:%S')
            if start_time <= access_time <= end_time:
                if access['user_id'] not in sites_visited.keys():
                    sites_visited[access['user_id']] = {}
                if access['site_id'] not in sites_visited[access['user_id']].keys():
                    sites_visited[access['user_id']][access['site_id']] = 0
                sites_visited[access['user_id']][access['site_id']] = sites_visited[access['user_id']][access['site_id']] + 1
                if sites_visited[access['user_id']][
                    access['site_id']] >= min_visits:
                    visits[access['user_id']] = (access['user_id'], access['site_id'], sites_visited[access['user_id']][access['site_id']])
    file.close()
    return [visits[user_id] for user_id in visits]

#Funtion to find what are top three sites?
def last_visited():
    datetime_format = '%Y-%m-%d %H:%M:%S'
    access_times_by_user = {}
    visited_by_user_datetime = {}
    num_of_users_by_site = {}

    with open("Adops & Data Scientist Sample Data - Q1 Analytics.csv", 'r') as file:
        site_logs = csv.DictReader(file)

        for access in site_logs:
            access_times_by_user.setdefault(access['user_id'], []).append(datetime.strptime(access['ts'], datetime_format))
            visited_by_user_datetime.setdefault('{}_{}'.format(access['user_id'], access['ts']), access['site_id'])
            num_of_users_by_site.setdefault(access['site_id'], 0)

        for user_id in access_times_by_user:
            last_datetime_str = sorted(access_times_by_user[user_id],reverse=True)[0].strftime(datetime_format)
            if '{}_{}'.format(user_id, last_datetime_str) in visited_by_user_datetime.keys():
                site_id = visited_by_user_datetime['{}_{}'.format(user_id, last_datetime_str)]
                num_of_users_by_site[site_id] = num_of_users_by_site[site_id] + 1

    top_visited_sites = sorted(num_of_users_by_site.items(),
                               key=lambda kv: (kv[1], kv[0]),
                               reverse=True)
    file.close()
    return top_visited_sites[:3]

#Function to Compute the number of users whose first/last visits are to the same website. What is the number?
def same_visits():
    datetime_format = '%Y-%m-%d %H:%M:%S'
    access_times_by_user = {}
    visited_by_user_datetime = {}
    num_of_users_same_visits = 0

    with open("Adops & Data Scientist Sample Data - Q1 Analytics.csv", 'r') as file:
        site_logs = csv.DictReader(file)

        for access in site_logs:
            access_times_by_user.setdefault(access['user_id'], []).append(datetime.strptime(access['ts'], datetime_format))
            visited_by_user_datetime.setdefault('{}_{}'.format(access['user_id'], access['ts']), access['site_id'])

        for user_id in access_times_by_user:
            first_datetime_str = sorted(access_times_by_user[user_id])[0].strftime(datetime_format)
            last_datetime_str = sorted(access_times_by_user[user_id],
                                       reverse=True)[0].strftime(datetime_format)
            if '{}_{}'.format(user_id, first_datetime_str) in visited_by_user_datetime.keys() and '{}_{}'.format(user_id, last_datetime_str) in visited_by_user_datetime.keys():
                first_site_id = visited_by_user_datetime['{}_{}'.format(user_id, first_datetime_str)]
                last_site_id = visited_by_user_datetime['{}_{}'.format(user_id, last_datetime_str)]
                if first_site_id == last_site_id:
                    num_of_users_same_visits = num_of_users_same_visits + 1
    file.close()
    return num_of_users_same_visits


    
#Main Function for calling above defined functions
if __name__ == '__main__':
    
    #Question1
    '''
    
    '''
    print('\nQuestion1\n')
    print('Site_with_largest_number_of_unique_user with country_id = BDV:')
    print(largest_unique_user(country_id='BDV'))                           
    
    
    #Question2
    print('\nQuestion2\n')
    print('Four users & sites they visited more than 10 times are:')
    print(four_users(start_time='2019-02-03 00:00:00', end_time='2019-02-04 23:59:59', min_visits=10)) 
    
    
    #Question3
    print('\nQuestion3\n')
    print('What are top three sites where the unique number of users whose last visit?:')
    print(last_visited())
    
    
    #Question4
    print('\nQuestion4\n')
    print('Compute the number of users whose first/last visits are to the same website. \n What is the number?:')
    print(same_visits())
