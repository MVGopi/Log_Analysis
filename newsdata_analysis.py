#!/usr/bin/env python
import psycopg2

# connection to our database
def database_connection(db_name="news"):
    """Instance for connecting to postgresql database"""
    try:
        conn_obj=psycopg2.connect("dbname={}".format(db_name))
        return conn_obj
    except:
        print("Failed  to connect {} database".format(db_name))

#first top 3 articles execution
def M_P_Art():
    conn_obj=database_connection()
    #cursor object create
    cur_obj=conn_obj.cursor()
    q1= ''' SELECT title, views FROM l_a INNER JOIN articles ON
    articles.slug = l_a.slug ORDER BY views desc LIMIT 3; '''
    cur_obj.execute(q1)
    results=cur_obj.fetchall()
    print("1.top  popular three articles of all time ? \n")
    for r in results:
        print('  "{0}"===>{1} views'.format(r[0], r[1]))
        
#top 4 authors
def M_P_Aut():
    conn_obj=database_connection()
    cur_obj=conn_obj.cursor()
    q2= '''
    SELECT l_n.name AS author,
    sum(l_a.views) AS views FROM l_a INNER JOIN l_n
    ON l_n.slug=l_a.slug
    GROUP BY l_n.name ORDER BY views desc limit 4;
    '''
    cur_obj.execute(q2)
    results=cur_obj.fetchall()
    print("\n2.top 4 most popular article authors of all time ? \n")
    
    for r in results:
        print('  "{0}"====>{1} views'.format(r[0], r[1]))

#lead error
def L_Error_A():
    conn_obj=database_connection()
    cur_obj=conn_obj.cursor()
    q3= '''
    SELECT l_f.date ,(l_f.count*100.00 / l_t.count) AS
    percentage FROM l_f INNER JOIN l_t
    ON l_f.date = l_t.date
    AND (l_f.count*100.00 / l_t.count) >1
    ORDER BY (l_f.count*100.00 /l_t.count) desc;
    '''
    cur_obj.execute(q3)
    results=cur_obj.fetchall()
    print(" \n 3.Days on which more than 1% of requests lead to errors ? ")
    for r in results:
        print('\n  On ' + str(r[0]) +'   ===>   ' + '%.1f' % r[1] +'% errors\n')
M_P_Art()
M_P_Aut()
L_Error_A()


