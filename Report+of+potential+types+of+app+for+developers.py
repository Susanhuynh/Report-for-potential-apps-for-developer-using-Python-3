#!/usr/bin/env python
# coding: utf-8

# # Report of potential types of app for users
# 
# We are  company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better.
# 
# *Our goal* for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# In[66]:


from csv import reader

# Open file App Store Data set
opened_file = open("AppleStore.csv")
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]

# Open file Google Play data set
opened_file = open("googleplaystore.csv")
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]


# In[67]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print("\n") #add a new empty line after each row
    
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns', len(dataset[0]))

print(ios_header)
print("\n")
explore_data(ios, 0, 4, True)


# *There are some column names which are not informative enough. You can follow this [documentation](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home) for more information*

# In[68]:


print(android_header)
print("\n")
explore_data(android, 0,7, True)


# In[69]:


print(android[10472])
print("\n")
print(android_header)
print("\n")
print(android[0])


# In[70]:


del android[10472]


# In[71]:


explore_data(android, 0, 3, True)


# *Row 10472 is missing Category, so it was deleted*

# In[72]:


for app in android:
    name = app[0]
    if name == "Instagram":
        print(app)


# In[73]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print("Number of duplicate apps: ", len(duplicate_apps))
print("\n")
print("Number of unique apps: ", len(unique_apps))


# *There are duplicate rows, I will remove the duplicated ones randomly. They have different number of views, so the entry with highest views will be left, the other will be deleted.*

# In[74]:


print("Expected dataset length: ", len(android) - 1181)


# In[75]:


reviews_max = {}
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    if name not in reviews_max:
        reviews_max[name] = n_reviews

print("Expected length: ", len(reviews_max))


# In[76]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
print("After deleting row: ", len(android_clean))


# In[77]:


def is_english(string):
    count = 0
    for character in string:
        if ord(character) > 127:
            count += 1
        
    if count > 3:
        return False
    return True
is_english("Instagram")


# In[78]:


is_english('爱奇艺PPS -《欢乐颂2》电视剧热播')


# In[79]:


is_english('Docs To Go™ Free Office Suite')


# In[80]:


is_english('Instachat 😜')


# In[81]:


english_ios_apps = []
for app in ios:
    name = app[1]
    if is_english(name) == True:
        english_ios_apps.append(app)

print("English IOS apps: ", len(english_ios_apps))


# In[82]:


explore_data(ios, 0, 3, True)


# In[83]:


explore_data(english_ios_apps, 0, 3, True)


# In[84]:


english_android_apps = []
for app in android_clean:
    name = app[0]
    if is_english(name) == True:
        english_android_apps.append(app)

print(android_header)
print("\n")
explore_data(english_android_apps, 0, 3, True)


# In[85]:


english_free_android = []
for app in english_android_apps:
    price = app[7]
    if price == "0":
        english_free_android.append(app)

explore_data(english_free_android, 0, 3, True)


# In[86]:


print(ios_header)


# In[87]:


english_free_ios = []

for app in english_ios_apps:
    price = app[4]
    if price == "0.0":
        english_free_ios.append(app)

explore_data(english_free_ios, 0, 3, True)


# *As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.*
# 
# *To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:*
# 
# *Build a minimal Android version of the app, and add it to Google Play.*
# *If the app has a good response from users, we develop it further.
# If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.*
# *Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets. For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.*
# 
# *Let's begin the analysis by getting a sense of what are the most common genres for each market. For this, we'll need to build frequency tables for a few columns in our data sets.*

# In[88]:


print(ios_header)
print("\n")
print(android_header)


# In[89]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for app in dataset:
        total += 1
        name = app[index]
        if name in table:
            table[name] +=1
        else:
            table[name] = 1
    table_percentage = {}
    for key in table:
        percentage = (table[key]/total)*100
        table_percentage[key] = percentage

    return table_percentage

freq_table(english_free_ios, 11)


# In[90]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[91]:


display_table(english_free_ios, 11)


# *In Apple Store dataset:*
#     **Game** is the most common genre. **Entertainment** is the runner-up. 
#     Most of apps designed for entertainments are popular then apps designed for education. 
#     There are lot of apps in one particular genres, but it does not mean that those apps have a lot of users.

# In[92]:


display_table(english_free_android, 1)


# *In Android Store App*: The most common genres are **Family**, **Game**, **Tools** and **Business**. 
#     On Android system, apart from Games with the highest frequencies, most of following apps belongs to educations and lifestyle. 

# In[ ]:





# In[93]:


print(ios_header)


# In[94]:


print(android_header)


# In[95]:


explore_data(english_free_android, 0 , 3, True)


# In[96]:


explore_data(english_free_ios, 0, 3, True)


# In[97]:


freq_table(english_free_ios, -5)


# In[98]:


genre_table = freq_table(english_free_ios, -5)


# In[99]:


genre_table = freq_table(english_free_ios, -5)

for genre in genre_table:
    total = 0
    len_genre = 0
    for app in english_free_ios:
        genre_app = app[-5]
        if genre_app == genre:
            value = float(app[5])
            total += value
            len_genre += 1
    average = total / len_genre
    print(genre, ": ", average)


# In[100]:


for app in english_free_ios:
    if app[-5] == "Navigation":
        print(app[1], ": ", app[5])


# In[101]:


for app in english_free_ios:
    if app[-5] == "Social Networking":
        print(app[1], ": ", app[5])


# In[102]:


for app in english_free_ios:
    if app[-5] == "Reference":
        print(app[1], " ", app[5])


# In[103]:


for app in english_free_ios:
    if app[-5] == "Weather":
        print(app[1], ": ", app[5])


# In[104]:


for app in english_free_ios:
    if app[-5] == "Music":
        print(app[1], ": ", app[5])


# *On average, **navigation** apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together*.
# 
# *The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.*
# 
# *Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.*
# 
# *Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating*

# *However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.*
# 
# *This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.*
# 
# *Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us*
# 
# *Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.*
# 
# *Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.*
# 
# *Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.*

# In[105]:


print(android_header)


# In[106]:


explore_data(english_free_android, 0 , 2, True)


# In[107]:


type(english_free_android[5])


# In[108]:


type(english_free_android[5][5])


# In[109]:


table = freq_table(english_free_android, 1)


# In[110]:


print(table)


# In[111]:


for category in table:
    total = 0
    len_category = 0
    for app in english_free_android:
        category_app = app[1]
        if category_app == category:
            n_install = app[5]
            n_install = n_install.replace(",", "")
            n_install = n_install.replace("+", "")
            n_install = float(n_install)
            total += n_install
            len_category += 1
    average = total/len_category
    print(category, ": ", average)


# On average, **communication** apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[112]:


for app in english_free_android:
    if app[1] == "COMMUNICATION" and (app[5] == "1,000,000,000+" or app[5] == "500,000,000+" or app[5] == "100,000,000+"):
        print(app[0],": ", app[5])
        


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

# In[113]:


under_10 = []

for app in english_free_android:
    value = app[5]
    value = value.replace(",","")
    value = value.replace("+", "")
    value = float(value)
    if app[1] == "COMMUNICATION" and value < 100000000:
        under_10.append(value)
sum(under_10)/len(under_10) 


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[114]:


for app in english_free_android:
    print(app[0], ": ", app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[117]:


for app in english_free_android:
    if app[1] == "BOOKS_AND_REFERENCE" and (app[5] == "1,000,000,000+" or app[5] == "500,000,000+" or app[5] == "100,000,000+"):
        print(app[0],": ", app[5])
        


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[118]:


for app in english_free_android:
    if app[1] == "BOOKS_AND_REFERENCE" and (app[5] == "1,000,000+" or app[5] == "5,000,000+" or app[5] == "10,000,000+" or app[5] == "100,000,000+"):
        print(app[0], ": ", app[5])


# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.
# 
# We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.
# 
# However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

# In[ ]:




