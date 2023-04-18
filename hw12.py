
#==========================================
# Purpose:
# Input Parameter(s):
# Return Value(s):
#==========================================




import tkinter as tk
import random
#FIRST: Implement and test your Pokemon class below
class Pokemon:
    def __init__(self,name,number,rate,speed):
        self.name = name
        self.number = number
        self.rate = rate
        self.speed = speed
    def __str__(self):
        return self.name
        


#NEXT: Complete the class definition provided below
class SafariSimulator(tk.Frame):
    
#==========================================
# Purpose:
# Input Parameter(s):
# Return Value(s):
#==========================================
    
    def __init__(self, master=None):
        
        self.balls = int(30)
        self.caught = []
        fp = open('pokedex.csv','r')
        lines = fp.readlines()
        allpoke = lines[1:]
        lspokename = []
        lspokenum = []
        lspokerate = []
        lspokespeed = []
        for i in range(len(allpoke)):
            current = allpoke[i]
            current1 = current.split(",")
            
            lspokename.append(current1[1])
            lspokenum.append(current1[0])
            lspokerate.append(current1[2])
            lspokespeed.append(current1[3])

        self.lspokename = lspokename
        self.lspokenum = lspokenum
        self.lspokerate = lspokerate
        self.lspokespeed = lspokespeed

        self.x = random.randint(0,150)

        #Use Pokemon Class here
        self.name = Pokemon(self.lspokename[self.x],self.lspokenum[self.x],self.lspokerate[self.x],self.lspokespeed[self.x])
        self.num = self.lspokenum[self.x]
        self.rate = self.lspokerate[self.x]
        self.speed = self.lspokespeed[self.x]
        
            
            
        
        
        
        #Read in the data file from pokedex.csv at some point here
        #It's up to you how you store and handle the data 
        #(e.g., list, dictionary, etc.),
        #but you must use your Pokemon class in some capacity

        #Initialize any instance variables you want to keep track of



        #DO NOT MODIFY: These lines set window parameters and create widgets
        tk.Frame.__init__(self, master)
        master.minsize(width=275, height=350)
        master.maxsize(width=275, height=350)
        master.title("Safari Zone Simulator")
        self.pack()
        self.createWidgets()
        fp.close()

        self.nextPokemon()
        #Call nextPokemon() method here to initialize your first random pokemon

    def createWidgets(self):
        
        #See the image in the instructions for the general layout required
        #"Run Away" button has been completed for you as an example:
        
        self.runButton = tk.Button(self)
        self.runButton["text"] = "Run Away"
        self.runButton["command"] = self.nextPokemon
        
        
        #You need to create an additional "throwButton"
        self.runButton2 = tk.Button(self)
        self.runButton2["text"] = "Throw Safari Ball " + '(' + str(self.balls) + ' left)'
        self.runButton2["command"] = self.throwBall
        self.runButton2.pack()
        self.runButton.pack()

        #A label for status messages has been completed for you as an example:
        self.messageLabel = tk.Label(bg="grey")
        self.messageLabel.pack(fill="x", padx=5, pady=5)
        self.messageLabel["text"] =  "You encounter a wild " + str(self.name)

        #You need to create two additional labels:

        #Complete and pack the pokemonImageLabel here.
        self.photo = tk.PhotoImage(file ='sprites/' + str(self.num)+'.gif')
        self.pokemonImageLabel = tk.Label(bg = "white" , text = "asdjfhbasdj")
        self.pokemonImageLabel['image'] = self.photo
        self.pokemonImageLabel.pack()
        

        #Complete and pack the catchProbLabel here.
        self.messageLabe2 = tk.Label(bg="grey")
        self.messageLabe2.pack(fill="x", padx=5, pady=5)
        catch_rate = min((int(self.rate)+1), 151) / 449.5
        catch_rate = catch_rate * 100

        catch_rate = catch_rate//1
        
        catch_rate = int(catch_rate)
        if catch_rate == 0:
            self.messageLabe2["text"] = "Your chance of catching is almost " + str(catch_rate) + "%"
        else:
            
            self.messageLabe2["text"] = "Your chance of catching is " + str(catch_rate) + "%"



    def nextPokemon(self):
        
    
        self.x = random.randint(0,150)
        
        


        self.name = Pokemon(self.lspokename[self.x],self.lspokenum[self.x],self.lspokerate[self.x],self.lspokespeed[self.x])
        self.num = self.lspokenum[self.x]
        self.rate = self.lspokerate[self.x]
        self.speed = self.lspokespeed[self.x]

        self.runButton2.pack_forget()
        self.runButton.pack_forget()
        self.messageLabel.pack_forget()
        self.messageLabe2.pack_forget()
        self.pokemonImageLabel.pack_forget()
        return self.createWidgets()
        
        
        

        #This method must:
            #Choose a random pokemon
            #Get the info for the appropriate pokemon
            #Ensure text in messageLabel and catchProbLabel matches the pokemon
            #Change the pokemonImageLabel to show the right pokemon

        #Hint: to see how to create an image, look at the documentation 
        #for the PhotoImage/Label classes in tkinter.
        
        #Once you generate a PhotoImage object, it can be displayed 
        #by setting self.pokemonImageLabel["image"] to it
        
        #Note: the PhotoImage object MUST be stored as an instance
        #variable for some object (you can just set it to self.photo).
        #Not doing this will, for weird memory reasons, cause the image 
        #to not be displayed.
        
    def throwBall(self):
        
        self.balls = self.balls - 1
        if self.balls > 0:
            self.runButton2["text"] = "Throw Safari Ball " + '(' + str(self.balls) + ' left)'
        if self.balls == 0:
            return self.endAdventure()

        number = random.random()
        catch_rate = min((int(self.rate)+1), 151) / 449.5

        print(f"This is the random number {number}")
        print(f"This is the catch rate {catch_rate}")
        
        
        if number < catch_rate:
            self.caught.append(self.name)
            self.nextPokemon()
            
            
           
          
        if number > catch_rate:
             self.messageLabel["text"] = "Aargh! It escaped!"
            

           
            

        
            
            
        
        
        
        #This method must:

            #Decrement the number of balls remaining
            #Try to catch the pokemon
            #Check to see if endAdventure() should be called

        #To determine whether or not a pokemon is caught, generate a random
        #number between 0 and 1, using random.random().  If this number is
        #less than min((catchRate+1), 151) / 449.5, then it is caught. 
        #catchRate is the integer in the Catch Rate column in pokedex.csv, 
        #for whatever pokemon is being targetted.
        
        #Don't forget to update the throwButton's text to reflect one 
        #less Safari Ball (even if the pokemon is not caught, it still 
        #wastes a ball).
        
        #If the pokemon is not caught, you must change the messageLabel
        #text to "Aargh! It escaped!"
        
        #Don't forget to call nextPokemon to generate a new pokemon 
        #if this one is caught.
        
    def endAdventure(self):
        self.runButton2.pack_forget()
        self.runButton.pack_forget()
        self.messageLabel.pack_forget()
        self.messageLabe2.pack_forget()
        self.pokemonImageLabel.pack_forget()

        self.messageLabe2 = tk.Label(bg="grey")

        self.messageLabe2.pack(fill="x", padx=10, pady=5)
            
        self.messageLabe2["text"] = "You're all out of balls, hope you had fun!"

        self.messageLabe1 = tk.Label(bg="grey")

        self.messageLabe1.pack(fill="x", padx=10)

        
        
        if len(self.caught) != 0:
            ls = []
            for i in self.caught:
                ls.append((str(i) + "\n"))
            ls = " ".join(ls)
            caught = [(str(self.caught[x])+ "\n") for x in range(len(self.caught))]
            
            self.messageLabe1["text"] = "You caught " + str(len(self.caught)) + " Pokemon:"
            self.messageLabel3 = tk.Label(bg="grey" ,text = ls)
            self.messageLabel3.pack(fill="x", padx=10)

        if len(self.caught) == 0:
            self.messageLabe1["text"] = "Oops you caught 0 Pokemon"
            
        
        
        #This method must: 

            #Display adventure completion message
            #List captured pokemon

        #Hint: to remove a widget from the layout, you can call the 
        #pack_forget() method.
        
        #For example, self.pokemonImageLabel.pack_forget() removes 
        #the pokemon image.




#DO NOT MODIFY: These lines start your app
app = SafariSimulator(tk.Tk())
app.mainloop()
