from logging import FileHandler, root
from random import randint

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel


from fileReaders import *
from anime_recommender import *


#Builder.load_file("recommender.kv")

anime = ObjectProperty(None)
rating = ObjectProperty(None)
selected_anime_label = ObjectProperty(None)
anime_spinner = ObjectProperty(None)
all_animes = read_list_of_animes("animetitles.csv")

class MyLayout(TabbedPanel):
    
     

    changes_made = False


    def add_anime_button_pressed(self):
        anime_to_add= self.selected_anime_label.text
        rating =self.rating.value

        #If no anime selected
        if anime_to_add=="None Selected":
            self.anime.background_color = "#FAA0A0"
            error_popup("You have not added a valid anime title yet!")
            return
        else:
            #check if anime has already been added
            my_ratings = read_my_ratings("my_ratings.txt") 
            anime_to_add = anime_to_add[10:len(anime_to_add)-1]
            already_done = False
            for i in range(len(my_ratings)):
                if anime_to_add==my_ratings[i][0]:
                    already_done = True
                    self.anime.background_color = "#FAA0A0"
                    error_popup("You have already rated this anime!")
                    return
            

        #add to my animes text file.
        file=open("my_ratings.txt","a")
        file.write("\n"+anime_to_add+"^"+str(rating))
        file.close()
        added_anime_popup(anime_to_add,rating)

        #reset stuff ready for new anime
        self.changes_made = True
        self.anime.text = ""
        self.selected_anime_label.text = "None Selected"
        self.rating.value = 1


    #edit rating label
    def slider(self,*args):
        self.rating_label.text = str(args[1])



    #The following functions are used for providin suggestions when the user is choosing an anime
    #So that only animes that are in the database can be selected
    def anime_input(self,text):
        suggestions = []
        for anime in all_animes:
            if text.lower() in anime.lower():
                suggestions.append(anime)

        self.refresh_suggestions(suggestions)

    def fillout(self,instance):
        self.anime.text = ''
        self.selected_anime_label.text = "Selected: " + instance.text
        
        self.ids.suggestions.clear_widgets()

    def refresh_suggestions(self,animes):
        self.ids.suggestions.clear_widgets()

        if len(animes)>10:
            animes = animes[0:10]

        for anime in animes:
            new_button = Button(text=str(anime), background_color = "#b6f2c8", font_size = "12")
            new_button.bind(on_press = self.fillout)
            self.ids.suggestions.add_widget(new_button)


    def recommender_tab_pressed(self):
        print('here')
        self.ids.recommend_anime_button.disabled = False
        self.ids.recommend_anime_label.text = 'Press button for recommendations'
            
    

        
    def recommend_button_pressed(self):
        my_ratings = read_my_ratings("my_ratings.txt")
        if len(my_ratings)==0:
            error_popup("No recommendations if you don't have any rated anime. Please add an anime to get a rating :)")
            return
        if self.changes_made:
            self.ids.recommend_anime_button.disabled = True
            self.ids.recommend_anime_label.text = "\nChanges have been made to your library. \nNew recommendations are being generated.\nPlease be patient.This may take a couple of minutes"

            generate_recommendations()
            self.changes_made = False
            self.ids.recommend_anime_button.disabled = False
            self.ids.recommend_anime_label.text = ''
        
        my_recommendations = read_my_recommendations('recommendations.csv', my_ratings,50)
        self.ids.recommend_anime_label.text = str(my_recommendations[randint(0,len(my_recommendations)-1)])

    def my_animes_tab_pressed(self):
        self.ids.my_animes_gl.clear_widgets()
        self.ids.my_animes_gl.add_widget(Label(text="ANIME"))
        self.ids.my_animes_gl.add_widget(Label(text="RATING"))
        my_ratings = read_my_ratings("my_ratings.txt")
        for anime in my_ratings:
            self.ids.my_animes_gl.add_widget(Button(text = str(anime[0])))
            self.ids.my_animes_gl.add_widget(Button(text = str(anime[1])))



     

    

    
      
    
        
    








class Added(BoxLayout):
    pass

#Popups
def added_anime_popup(anime,rating):
    l = Added()
    
    l.added_anime_label.text = "Anime:" + str(anime) + "\nRating: " + str(rating)
    popup = Popup(title = "Anime Added!",
                    content = l,
                    size_hint=(0.6,0.2),
                    pos_hint={"x":0.2,"top":0.9})
    popup.open()
    return

def error_popup(text):
    l = Added()
    
    l.added_anime_label.text = text
    popup = Popup(title = "Error",
                    content = l,
                    size_hint=(0.6,0.2),
                    pos_hint={"x":0.2,"top":0.9})
    popup.open()
    return



        

#Main App Function
class recommenderApp(App):
    def build(self):
        return MyLayout()

if __name__ == "__main__":
    recommenderApp().run()
