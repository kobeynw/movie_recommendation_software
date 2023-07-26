import pandas as pd
import glob
import random
from hash_map_class import HashMap


#  CREATE DATA FILE FROM CSV
files = glob.glob("imdb_top_1000.csv")
df_list = []

for filename in files:
  data = pd.read_csv(filename)
  df_list.append(data)
imdb_data = pd.concat(df_list)


#  HELPER FUNCTIONS
titles_column = imdb_data.Series_Title
genres_column = imdb_data.Genre.str.split(", ")

def get_hash_map(column):
  imdb_hash_map = HashMap(1000)
  for title, genres in zip(titles_column, column):
    imdb_hash_map.assign(title, genres)
  return imdb_hash_map


def intro():
  print("####    FLICK PICK    ####\n")
  print("Select a genre from the list and we'll give you some "
        "recommended movies from the 'IMDB top 1000 movies' list!\n")


def ending():
  print("\nThank you for using Flick Pick! We hope you found a movie you can enjoy!")


rel_year_range = None
runtime_range = None
genres_list = ['Drama', 'Crime', 'Action', 'Adventure', 'Sci-Fi', 'Thriller', 'Horror',
               'Film-Noir', 'Fantasy', 'Romance', 'Mystery', 'Family', 'Animation', 'Music', 'Musical',
               'Comedy', 'Western', 'Sport', 'Biography', 'History', 'War']
director_list = []

def get_input(col):
  print(f"Genre options: {', '.join(genres_list)}")
  selection = input("What would you like your recommendation based on? >> ")
  if selection in genres_list:
    return selection
  return get_input(col)


def follow_up(recs, hm, col, selection):
  fav = input("\nWhich of these suggestions did you like best? (if none, type 'none') >> ")
  if fav == 'none':
    another = input("Sorry to hear that! Would you like another recommendation?"
                    " ('y' for yes, 'n' for no) >> ")
    if another == 'y':
      get_recommendation(hm, col)
    else:
      ending()

  elif fav not in recs:
    follow_up(recs, hm, col, selection)

  else:
    new_rec_list = []
    if len(hm.retrieve(fav)) > 1:
      if hm.retrieve(fav)[0] != selection:
        new_selection = hm.retrieve(fav)[0]
      else:
        new_selection = hm.retrieve(fav)[1]
      print("\nYou might also like...")
      for title in imdb_data.Series_Title:
        if fav in title and fav != title:
          print(title)
        elif new_selection in hm.retrieve(title):
          new_rec_list.append(title)
      for new_rec in random.sample(new_rec_list, 3):
        print(new_rec)
      ending()

    else:
      print("\nYou might also like...")
      for title in imdb_data.Series_Title:
        if fav in title and fav != title:
          print(title)
        elif selection in hm.retrieve(title):
          new_rec_list.append(title)
      for new_rec in random.sample(new_rec_list, 3):
        print(new_rec)
      ending()


def get_recommendation(hm, col):
  selection = get_input(col)
  rec_list = []
  for title in imdb_data.Series_Title:
    if selection in hm.retrieve(title):
      rec_list.append(title)
  max_n = len(rec_list)
  if max_n > 20:
    max_n = 20
  n = input(f"How many recommended movies would you like? (maximum is {max_n}) >> ")
  if not n.isnumeric() or int(n) >= max_n:
    n = max_n
  else:
    n = int(n)
  recs = random.sample(rec_list, n)
  print("\nHere are some recommended movies based on your preference!")
  for rec in recs:
    print(rec)
  follow_up(recs, hm, col, selection)


#  MAIN CODE BODY
def recommend_software():
  intro()
  imdb_hash_map = get_hash_map(genres_column)
  get_recommendation(imdb_hash_map, genres_column)



#  TEST CODE
recommend_software()