import tkinter as tk
import pygame
import time
import json
import random
from tkinter import messagebox


# "SELF" Ito ay isang special parameter na nagsisilbing reference sa instance ng class. Sa bawat method ng class,
# kinakailangan itong maging unang parameter upang ma-access ang mga attributes at iba pang methods ng class.

class InteractiveQuiz:
    def __init__(self, root): # unang bahagi ng code na tinatawag kapag ginagawa ang isang instance ng class.
        self.root = root
        self.root.title("INTERACTIVE QUIZ GAME")
        self.root.geometry(f"1500x800") # "f" or f-string pag may variable ka na gusto gawing string / size of the window
        self.root.configure(bg="#2A225A") # violet
        # Load sound file (replace with your actual file path)
        pygame.mixer.init()
        self.wrong_sound = pygame.mixer.Sound(r"wrong3.mp3")
        self.correct_sound = pygame.mixer.Sound(r"correct1.mp3")
        self.gameover_music = pygame.mixer.Sound(r"gameovermusic.mp3")
        self.button_music = pygame.mixer.Sound(r"button2music.mp3")
        self.congrats_music = pygame.mixer.Sound(r"congrats.mp3")
        background_music_file = r"quizbg.mp3"
        pygame.mixer.music.load(background_music_file)
        # Start playing the background music (loop indefinitely)
        pygame.mixer.music.play(-1)
        self.difficulty_var = tk.StringVar()
        self.subject_var = tk.StringVar()
        self.topics = None
        self.currentFrame = None
        self.score_label = None
        self.submit_button = None
        self.question_label = None
        self.back_button = None
        self.save_button = None
        
        self.currentQuestionIndex = 0
        self.score = 0
        self.lives = 0
        self.que_var = 0
        self.wrong_var = 0
        self.total_iq = 0
        self.calculated_iq = 0
        self.player_answer = tk.StringVar()
        self.player_answers = {}

        self.menu_frame1()

    def menu_frame1(self):
        
        # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)

        bg_frame1 = tk.Frame(self.root, bg="#2A225A")  # background color for the frame 1
        bg_frame1.pack()

        self.currentFrame = bg_frame1

        frame1_label1 = tk.Label(bg_frame1, text="INTERACTIVE QUIZ",
                                 bg="#2A225A",
                                 fg="white",
                                 font=("Comic sans MS", 75, "bold"))
        frame1_label1.pack(pady=60)

        frame1_label2 = tk.Label(bg_frame1, text="Version 3.2",
                                 bg="#2A225A",
                                 fg="white",
                                 font=("Comic sans MS", 30, "bold"))
        frame1_label2.pack(pady=10)

        frame1_button1 = tk.Button(bg_frame1, text="  Start  ",
                                   command=self.start_button_sound,
                                   padx=35,
                                   border=8,
                                   cursor='hand2',
                                   background="#C3C123",
                                   foreground="#097FA2",
                                   activebackground="yellow",
                                   activeforeground="#097FA2",
                                   font=("Comic sans MS", 30, "bold"))
        frame1_button1.pack(pady=20)
        
        menu_button2 = tk.Button(bg_frame1, text="  Quit  ",
                                 command=self.quit_button_sound,
                                 padx=45,
                                 border=8,
                                 cursor='hand2',
                                 background="#A44D53",
                                 foreground="yellow",
                                 activebackground="red",
                                 activeforeground="yellow",
                                 font=("Comic sans MS", 30, "bold"))
        menu_button2.pack(pady=25)
        
        # button sounds in opening frame
    def start_button_sound(self):
        self.button_music.play()
        self.show_frame2()
        
    def quit_button_sound(self):
        self.button_music.play()
        self.quit_game()
        

    def show_frame2(self):
        
        pygame.mixer.music.play()
        
        # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)
         
        bg_frame2 = tk.Frame(self.root, bg="#2A225A")  # Set the background color for the frame 2
        bg_frame2.pack()
        
        # kasalukuyang frame na ginagamit
        self.currentFrame = bg_frame2
        
        
        frame2_label = tk.Label(bg_frame2, text="M E N U",
                                bg="#2A225A",
                                fg="white",
                                font=("Comic sans MS", 75, "bold"))
        frame2_label.pack(pady=60)
         
        # select difficulty 
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Difficulty")
           
        option_menu_font = ('Comic sans MS bold', 40)
        option_menu_bg = "#D80A1F"
        option_menu_abg = "red"
        option_menu_fg = "yellow"
        option_menu_cur = "hand2"

        difficulty_dropdown = tk.OptionMenu(bg_frame2, self.difficulty_var,
                                            "      Easy    ",
                                            "    Normal    ",
                                            "     Hard    ",
                                            "    Average   ",
                                            "    Genius    ")
        difficulty_dropdown.config(font=option_menu_font, bg=option_menu_bg,fg=option_menu_fg, activebackground=option_menu_abg,cursor=option_menu_cur)
        difficulty_dropdown.pack(padx=10)
        
        #select topic / subject 
        self.subject_var = tk.StringVar()
        self.subject_var.set("Select Topic!")

        option2_menu_font = ('Comic sans MS bold', 40)
        option2_menu_bg = "gold"
        option2_menu_abg ="yellow"
        option2_menu_fg = "blue"
        option2_menu_cur = "hand2"                              # dito mag lagay ng topic name
        subject_dropdown = tk.OptionMenu(bg_frame2, self.subject_var, "Universe","Tricky","Brain Teaser","Mythology","Music","History","Biology","TEST HERE")
        subject_dropdown.config(font=option2_menu_font, bg=option2_menu_bg, fg=option2_menu_fg, activebackground=option2_menu_abg,cursor=option2_menu_cur)
        subject_dropdown.pack(pady=40)

         #load progress
        loadbutton_progress = tk.Button(bg_frame2,
                                 text="     Load     ",
                                 command=self.load_button_sound,
                                 padx=32, pady=10,
                                 border=4,
                                 cursor='hand2',
                                 background="#066B10",
                                 foreground="white",
                                 activebackground="#23F136",
                                 activeforeground="WHITE",
                                 font=("Comic sans MS", 20, "bold"))
        loadbutton_progress.pack(side=tk.LEFT, padx=25)

        
        # new game button
        start_button = tk.Button(bg_frame2,
                                 text="  New Game  ",
                                 command=self.newgame_button_sound,
                                 padx=32, pady=10,
                                 border=4,
                                 cursor='hand2',
                                 background="#07688D",
                                 foreground="white",
                                 activebackground="#65E7FF",
                                 activeforeground="WHITE",
                                 font=("Comic sans MS", 20, "bold"))
        start_button.pack(side=tk.LEFT, padx=40)
        
        # back button
        back_button = tk.Button(bg_frame2,
                                 text="    Back    ",
                                 command=self.back_button_sound,
                                 padx=55, pady=10,
                                 border=4,
                                 cursor='hand2',
                                 background="#A44D53",
                                 foreground="white",
                                 activebackground="red",
                                 activeforeground="white",
                                 font=("Comic sans MS", 20, "bold"))
        back_button.pack(side=tk.LEFT, padx=10)
        
        # button sounds in menu frame
    def load_button_sound(self):
        self.button_music.play()
        self.start_2quiz()
        
    def newgame_button_sound(self):
        self.button_music.play()
        self.start_quiz()
        
    def back_button_sound(self):
        self.button_music.play()
        self.menu_frame1()     
        
        #start quiz
    def start_quiz(self):
        selected_difficulty = self.difficulty_var.get()
        selected_subject = self.subject_var.get()

        if selected_difficulty == "Difficulty" or selected_subject == "Select Topic!":
            tk.messagebox.showerror("E R R O R", "PLEASE SELECT BOTH DIFFICULTY AND TOPIC !")                                                             
            return
        # lives base on difficulty
        if selected_difficulty == "      Easy    ":
           self.lives = 999
        elif selected_difficulty == "    Normal    ":
             self.lives = 17
        elif selected_difficulty == "     Hard    ":
             self.lives = 11
        elif selected_difficulty == "    Average   ":
             self.lives = 8
        elif selected_difficulty == "    Genius    ":
             self.lives = 4
             
        # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)
            
        self.reset_score()
        self.reset_lives()
        self.reset_topics()
        self.generate_quiz_frame()
        
    def load_progress_button(self):
        try:
            with open("progress.json", "r") as file:
                progress_data = json.load(file)
                self.currentQuestionIndex = progress_data["question_index"]
                self.score = progress_data["score"]
                self.player_answers = progress_data.get("player_answers", {})
                self.lives = progress_data.get("lives", 1)
                self.topic = progress_data["topic"]
                self.subject_var.set(progress_data["topic"]) # getting the progress data to store sa subject_var.
                self.que_var = progress_data["que"]
                
                self.generate_quiz_frame2()
        except FileNotFoundError:
        
            
            tk.messagebox.showinfo("Info", "No saved progress found.")
            self.show_frame2()

        
    def start_2quiz(self):
        
     if self.currentFrame:
         self.currentFrame.pack_forget()
     self.root.after(100)
     
     self.load_progress_button()
     
        
    def reset_score(self):
        self.score = 0

    def reset_lives(self):
        selected_difficulty = self.difficulty_var.get()

    def reset_topics(self):
        self.currentQuestionIndex = 0
    

    def saved_progress(self):
        messagebox.showinfo("S A V E D",f"Your Progress Has Saved!")
        progress_data = {
            "que": self.que_var,
            "topic": self.subject_var.get(),
            "question_index": self.currentQuestionIndex,
            "score": self.score,
            "player_answers": self.player_answers,
            "lives": self.lives  # Fixed the key name here
        }

        with open("progress.json", "w") as file:
            json.dump(progress_data, file)
            
            
        # GENERATING QUIZ FRAME FOR NEW PROGRESS
    def generate_quiz_frame(self):
       
        if self.subject_var.get() == "Universe":
            self.topics = [
                {"question": "Approximately, what is the age of the universe?", "options": ["365 Days", "366 Days", "23.9 Billion Years", "13.8 Billion Years"],
                 "answer": "13.8 Billion Years"},
                {"question": "What is the famous theory of creation of the universe?", "options": ["Information Theory", "Game Theory", "Big Bang Theory", "Quantum Theory"],
                 "answer": "Big Bang Theory"},
                {"question": "What is this mysterious component of the universe\ncalled?", "options": ["Dark Energy", "Dark Star", "Dark Matter", "Black Hole"],
                 "answer": "Dark Energy"},
                {"question": "A space wherein the gravity’s so strong not even light can\nescape.", "options": ["Butt Hole", "Black Hole", "Black Jack", "Black Butt"],
                 "answer": "Black Hole"},
                {"question": "What is the estimated count of galaxies in the observable universe?", "options": ["100 to 200 Galaxies", "10 to 20 Galaxies", "100 to 200 Billion Galaxies", "Eight Galaxies"],
                 "answer": "100 to 200 Billion Galaxies"},
                {"question": "What is the prevailing cosmological model that explains the\norigin and evolution of the observable universe?", "options": ["Big Bang Theory", "Information Theory", "Quantum Theory", "God's Creation Theory"],
                 "answer": "Big Bang Theory"},
                {"question": "What is the form of matter that is invisible and undetectable\nthrough electromagnetic radiation?", "options": ["Dark Energy", "Dark Star", "Dark Matter", "Black Hole"],
                 "answer": "Dark Matter"},
                {"question": "This concept proposes a rapid and exponential expansion of the\nearly universe during the first moments after the Big Bang.", "options": ["Cosmic Inflation", "Continental Drift Theory", "Game Theory", "Information Theory"],
                 "answer": "Cosmic Inflation"},
                {"question": "Formed through the gravitational collapse of massive objects,\ntypically the remnants of massive stars.", "options": ["Meteorite", "Meteor", "Black Hole", "Star"],
                 "answer": "Black Hole"},
                {"question": "This is a formation of rock debris flying freely in the universe?", "options": ["Meteorite", "Meteor", "Asteroid", "Asteroid Belt"],
                 "answer": "Asteroid"},
                {"question": "What’s the three possible shape of the universe?", "options": ["Oblique,Sphere,Trapezoid", "Flat,Open,Close", "Rectangle,Triangle,Sphere,", "Flat,Sphere,Oblique"],
                 "answer": "Flat,Open,Close"},
                {"question": "What do you call the processes of star formation, stellar death\nand feedback, influencing their appearance and characteristics?", "options": ["Galactic Evolution", "Galactic Rebirth", "Galactic Revolution", "Galaxy Overhaul"],
                 "answer": "Galactic Evolution"},
                {"question": "This matter is incredibly dense and compact stellar remnants\nthat form when massive stars undergo a supernova explosion.", "options": ["Neuron Stars", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Fascinating objects that push the limits of our\nunderstanding of matter and gravity.", "options": ["Neuron Stars", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Possess extremely strong magnetic fields, often trillions\nof times stronger than Earth's magnetic field.", "options": ["Neuron Star", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Hypothetical tunnel-like structure that connects\ntwo separate points in space-time.", "options": ["Wormhole", "Funnel", "Asshole", "Black Hole"],
                 "answer": "Wormhole"},
                {"question": "It consists of two ends, often referred to as mouths or throats.\nEach mouth is a separate entrance or exit point in space time.", "options": ["Wormhole", "Funnel", "Asshole", "Black Hole"],
                 "answer": "Wormhole"},
                {"question": "The simplest type of wormhole, known as a _, is a hypothetical\nsolution to the equations of general relativity.", "options": ["Wormhole", "White Hole", "Black Hole", "Einstein-Rosen Bridge"],
                 "answer": "Einstein-Rosen Bridge"},
                {"question": "Responsible for the formation of celestial bodies, such as\nstars, planets, galaxies, and galaxy clusters.", "options": ["Gravity", "Stars", "Meteor", "Meteorites"],
                 "answer": "Gravity"},
                {"question": "Gravity governs the ___ of celestial bodies in the universe.", "options": ["Orbital Motion", "Revolution", "Gravitational Pull", "Meteorites"],
                 "answer": "Orbital Motion"},
                {"question": "It is the primary force shaping the dynamics of galaxies.", "options": ["Gravity", "Force", "UV rays", "Meteorite"],
                 "answer": "Gravity"},
                {"question": ". __ is a fundamental force that governs the behavior of matter,\nfrom the smallest particles to largest structures.", "options": ["Gravity", "Force", "UV rays", "Meteorite"],
                 "answer": "Gravity"},
                {"question": "These planets are not located within the Sun's family of planets\nbut instead orbit stars that may be light-years away from Earth.", "options": ["Wormhole", "Exoplanets", "Neuroplanets", "Dwarf Planets"],
                 "answer": "Exoplanets"},
                {"question": "Also known as Goldilocks Zone", "options": ["Restricted Zone", "Habitable Zone", "Danger Zone", "Deadly Zone"],
                 "answer": "Habitable Zone"},
                {"question": "What is the three detection method?", "options": ["Transit, Direct Imaging, Radar", "Transit, Radial Velocity,\nDirect imaging", "Tracking, Recording, Surveillance", "Transmit, Monitor, Radar"],
                 "answer": "Transit, Radial Velocity,\nDirect imaging"},
                {"question": "This equation is a probabilistic formula that was developed\nby the American astrophysicist Dr. Frank Drake in 1961.", "options": ["Probability & Statistics", "Mathematical Equation", "Drake Equation", "Pythagorean Theorem"],
                 "answer": "Drake Equation"},
                {"question": "__is a large-scale structure of the universe, composed of\ninterconnected filaments of dark matter and gas.", "options": ["Star", "Cosmic Web", "Black Hole", "Worm Hole"],
                 "answer": "Cosmic Web"},
                {"question": "What is the three elements of cosmic web?", "options": ["Filaments, Nodes, Voids", "Gas, Dark Energy, Dark Matter", "Filaments, Voids, Dark Energy", "Nodes, Dark Energy, Dark Matter"],
                 "answer": "Filaments, Nodes, Voids"},
                {"question": "The __ of the cosmic web is primarily composed of\ndark matter,a mysterious form of matter that does not interact with light.", "options": ["Backbone", "Heart", "Brain", "Center"],
                 "answer": "Backbone"},
                {"question": "__ thought to trace the underlying distribution of dark matter.", "options": ["Backbone", "Cosmic Web", "Dark Energy", "Ordinary Matter"],
                 "answer": "Ordinary Matter"},
                {"question": ". __ is a scientific concept that addresses the universe's\nphysical constants and conditions allow for the existence of \nlife.", "options": ["Genetics", "Properties of Matter", "Big Bang Theory", "Anthropic Principle"],
                 "answer": "Anthropic Principle"},
                {"question": "What is the two (2) types of anthropic Principle?", "options": ["SAP & WAP", "SAP & PWD", "WAP & DSWD", "AAP & SAP"],
                 "answer": "SAP & WAP"},
                {"question": "__ is a highly magnetized, rotating neutron star that emits\nbeams of electromagnetic radiation along its magnetic poles.", "options": ["Void", "Pulsar", "Pulse", "Electron"],
                 "answer": "Pulsar"},
                {"question": "Composed primarily of neutrons, with incredibly high densities.", "options": ["Void", "Pulsar", "Pulse", "Electron"],
                 "answer": "Pulsar"},
                {"question": "Have extremely strong magnetic fields, typically trillions\nof times stronger than Earth's magnetic field.", "options": ["Neutron Star", "Pulsar", "Moon", "Sun"],
                 "answer": "Pulsar"},
                {"question": "Three types of radiation Pulsar produce.", "options": ["Gamma ray, X-ray, Radio Waves", "Gamma ray,Pulse,UV ray", "X-ray,Pulse,Radio waves", "Sun Ray,UV ray,Micro Waves"],
                 "answer": "Gamma ray, X-ray, Radio Waves"},
                {"question": "Hypothetical one-dimensional topological defects in the\nfabric of space time.", "options": ["Common String", "Cosmic Strings", "Coil Spring", "Pulse String"],
                 "answer": "Cosmic Strings"},
                {"question": "Topological defects because their existence is not dependent on\nspecific physical properties or the material they are made of.", "options": ["Common String", "Cosmic Strings", "Coil Spring", "Pulse String"],
                 "answer": "Cosmic Strings"},
                {"question": ". __ expected to generate gravitational effects.", "options": ["Gravity", "Cosmic Strings", "Sun", "Pulsar"],
                 "answer": "Cosmic Strings"},
                {"question": "Considered as a possible mechanism for seeding the formation of\nlarge-scale structures such as galaxies and galaxy clusters.", "options": ["Duplicating", "Cosmic Strings", "Replicating", "Reproduction"],
                 "answer": "Cosmic Strings"},
                {"question": "What are the two types of supernova?", "options": ["Type C&Prototype", "Type C&B", "Type 1&2", "Type II & la"],
                 "answer": "Type II & la"},
                {"question": "Responsible for synthesizing and dispersing heavy elements,\nsuch as iron and gold, into space.", "options": ["Planet Collision", "Star Explosion", "Meteor Collision", "Supernova"],
                 "answer": "Supernova"},
                {"question": "Consists of particles with the same mass as\nordinary matter particles but with opposite charge.", "options": ["Core", "Anti-Matter", "Dark Matter", "Sun"],
                 "answer": "Anti-Matter"},
                {"question": "Hypothetical substance that combines dark matter and\ndark energy into a unified framework.", "options": ["Dark Energy", "Dark Matter", "Dark Fluid", "Dark Liquid"],
                 "answer": "Dark Fluid"},
                {"question": "Late-stage star that has exhausted its core hydrogen,\nexpanded, and cooled.", "options": ["Dwarf Planet", "Dead Star", "Dark Fluid", "Red-Giant"],
                 "answer": "Red-Giant"},
                {"question": "Region of the solar system beyond Neptune that\ncontains many small, icy bodies.", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "It is similar to the asteroid belt, which is located\nbetween Mars and Jupiter, but much larger and \nfarther from the Sun.", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "Named after Dutch-American astronomer Gerard Kuiper, who\nfirst proposed the existence of such a region in the\n1950s?", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "Hypothetical region in the outermost reaches of the\nsolar system, believed to contain icy bodies and comets.", "options": ["Oort Cloud", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Oort Cloud"},
                {"question": "Named after the Dutch astronomer Jan Oort, who\nproposed its existence in 1950?", "options": ["Oort Cloud", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Oort Cloud"},
                {"question": "The remnant core of a star that has exhausted\nits nuclear fuel.", "options": ["Oort Cloud", "Asteroid Belt", "White Dwarf", "Red-Giant"],
                 "answer": "White Dwarf"},
                {"question": "Characterized by their small size, high density, and relatively low\nluminosity compared to their earlier stages as main-sequence\nstars.", "options": ["Oort Cloud", "Asteroid Belt", "White Dwarf", "Red-Giant"],
                 "answer": "White Dwarf"},
                {"question": "Extremely luminous and energetic active galactic nucleus,\npowered by a supermassive black hole.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Can exhibit rapid and extreme variability in their brightness\nover short timescales, ranging from days to months.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Appear as point sources, they are\nassociated with host galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "This astronomical object helps\nscientists study the early universe.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Study of active galactic nuclei and the understanding of\nthe energetic processes occurring in the centers of galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Among the most luminous objects in the universe,\noutshining entire galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "First identified as unusual point sources of\nradio waves in the 1960s.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Measure of the rate at\nwhich the universe is expanding.", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "Named after the American astronomer Edwin Hubble, understanding\nof the expansion of the universe.", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "Expressed in units of kilometers per second\nper megaparsec (km/s/Mpc).", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "States that the velocity at which a galaxy\nis moving away from an observer is directly\nproportional to its distance.", "options": ["Boyle's Law", "Hubble's Law", "Charles's Law", "Law of Attraction"],
                 "answer": "Hubble's Law"},
                {"question": "Denoted by the symbol (H₀).", "options": ["Velocity", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "According to quantum mechanics, it's a phenomenon\nknown as vacuum fluctuations.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Inversely proportional to the mass of the\nblack hole. Smaller black holes emit more intense\nradiation than larger ones.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Not been directly observed because the effect is\nextremely weak for astrophysical black holes.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Occurs when the Moon passes between the Earth\nand the Sun, blocking part or all of\nthe Sun's light.", "options": ["Supernova", "Meteor Shower", "Lunar Eclipse", "Solar Eclipse"],
                 "answer": "Solar Eclipse"},
                {"question": "Can happen only when the Sun, Moon, and\nEarth are aligned in a straight line, with\nthe Moon casting a shadow on Earth.", "options": ["Supernova", "Meteor Shower", "Lunar Eclipse", "Solar Eclipse"],
                 "answer": "Solar Eclipse"},
                {"question": "The Moon completely covers the Sun from the\nviewpoint of observers on Earth.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Total Solar Eclipse"},
                {"question": "Only a portion of the Sun is covered\nby the Moon, and the Sun appears as\na crescent.", "options": ["Partial Solar Eclipse", "Annual Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Partial Solar Eclipse"},
                {"question": "Occurs when the Moon is too far from\nEarth to completely cover the Sun.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Annular Solar Eclipse"},
                {"question": "The Sun's outer atmosphere, called the solar\ncorona, becomes visible during totality.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Total Solar Eclipse"},
                {"question": "The extent of coverage depends on the\nobserver's location within the eclipse's path.", "options": ["Partial Solar Eclipse", "Annual Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Partial Solar Eclipse"},
                {"question": "These bursts are the most energetic events in\nthe universe, emitting more energy in a few\nseconds.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Gamma Ray Burst"},
                {"question": "Stellar explosion that is more energetic and powerful\nthan a supernova. It represents the extreme life cycle\nof massive stars.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Hypernova"},
                {"question": "Stellar explosion that results from the merger\nof two stars in a binary system.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Luminous Red Nova"},
                {"question": "Temporary increase in the brightness of a star,\ntypically by a factor of several thousand.", "options": ["Nova", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Nova"},
                {"question": "It is a minor type of stellar explosion.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Solar Flares"],
                 "answer": "Solar Flares"},
                {"question": "What is the unit used to indicate the\ndistance of the galaxy in the universe?", "options": ["Light Year", "Parsec", "Miles", "Kilometers"],
                 "answer": "Parsec"},
                {"question": "Used to describe a hypothetical space that exists\nbeyond the three spatial dimensions we are familiar\nwith.", "options": ["Light Year", "Parsec", "Hyperspace", "Kilometers"],
                 "answer": "Hyperspace"},
                {"question": "Speculative concept that arises in various scientific and\nphilosophical discussions,and it suggests the existence of multiple, possibly\ninfinite, universes or realities.", "options": ["Universe", "Multiverse", "Parallel Universe", "Alternate Reality"],
                 "answer": "Multiverse"},
                {"question": "Theoretical framework in physics that attempts to describe\nthe building blocks of the universe as one-\ndimensional, suggests the possibility of multiple compactified dimensions.", "options": ["Universe", "Multiverse", "String Theory", "Alternate Reality"],
                 "answer": "String Theory"},
                {"question": "Typically refers to a hypothetical or fictional version\nof reality that differs from the one we\nexperience in our everyday lives.", "options": ["Universe", "Multiverse", "String Theory", "Alternate Reality"],
                 "answer": "Alternate Reality"},
                {"question": "Also known as an alternate universe or a\nparallel dimension.", "options": ["Universe", "Multiverse", "String Theory", "Parallel Universe"],
                 "answer": "Parallel Universe"},
                {"question": "This wave ripples in the fabric of spacetime\ncaused by the acceleration of massive objects.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "__ waves are a form of radiation, similar\nto electromagnetic waves, but with distinct properties.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "__ waves are produced by accelerating masses,\nespecially those involved in violent astrophysical events.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "Travel at the speed of light and can\npass through matter without being significantly affected.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "This one main formulation takes a more metaphysical stance\nand suggests that the universe must have properties\nthat allow for the existence of observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Strong Anthropic Principle"},
                {"question": "This main formulation is the more modest form\nand states that the properties of the universe\nmust be consistent with the existence of observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Weak Anthropic Principle"},
                {"question": "The __ is often used to explain why\ncertain physical constants and conditions appear finely tuned\nfor the existence of life.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Weak Anthropic Principle"},
                {"question": "Some proponents of the __ go further, suggesting\nthat the universe is, in some sense, compelled\nto bring forth conscious observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Strong Anthropic Principle"},
                {"question": "He is a Soviet cosmonaut, was the first\nhuman to journey into outer space.", "options": ["Yuri Gagarin", "Albert Einstein", "Charles Darwin", "Robert Boyle"],
                 "answer": "Yuri Gagarin"},
                {"question": "His mission lasted approximately 108 minutes, during which\nhe experienced weightlessness and observed Earth from orbit.", "options": ["Yuri Gagarin", "Albert Einstein", "Charles Darwin", "Robert Boyle"],
                 "answer": "Yuri Gagarin"},
                {"question": "__ is a massive, gravitationally bound system consisting\nof stars, stellar remnants, interstellar gas, dust, and\ndark matter.", "options": ["Star", "Sun", "Universe", "Galaxy"],
                 "answer": "Galaxy"},
                {"question": "Come in various shapes and sizes and can\ncontain millions to trillions of stars.", "options": ["Star", "Sun", "Universe", "Galaxy"],
                 "answer": "Galaxy"},
                {"question": "This galaxy shape have a more spheroidal or\nellipsoidal shape and lack well-defined spiral arms.", "options": ["Sphere Galaxy", "Flat Galaxy", "Lunar Galaxy", "Elliptical Galaxy"],
                 "answer": "Elliptical Galaxy"},
                {"question": "Who is the first person to\nset foot on the Moon?", "options": ["Neil Armstrong", "Isaac Newton", "Charles Darwin", "Albert Einstein"],
                 "answer": "Neil Armstrong"}
            ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Tricky":
            self.topics = [
                {"question": " What is the capital of Canada?", "options": ["Ottawa", "Toronto", "Vancouver", "Montreal"],
                 "answer": "Montreal"},
                
                {"question": "Who is the author of 'To Kill a Mockingbird'?", "options": ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "F. Scott Fitzgerald"],
                 "answer": "Harper Lee"},
                
                {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"],
                 "answer": "6"},
                
                {"question": "Which planet is known as the 'Red Planet'?", "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                 "answer": "Mars"},
                
                {"question": "What is the square root of 144?", "options": ["12", "10", "14", "16"],
                 "answer": "12"},
                
                {"question": "In what year did World War I begin?", "options": ["1914", "1916", "1918", "1920"],
                 "answer": "1914"},
                
                {"question": "Who painted the Mona Lisa?", "options": ["Michelangelo", "Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"],
                 "answer": "Leonardo da Vinci"},
                
                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},
                
                {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Endoplasmic reticulum", "Golgi apparatus"],
                 "answer": "Mitochondria"},
                
                {"question": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"],
                 "answer": "6"},
                
                {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                 "answer": "William Shakespeare"},
                
                {"question": "What is the chemical symbol for gold?", "options": ["Gd", "Au", "Ag", "Pt"],
                 "answer": "Au"},
                
                {"question": "Which planet is known as the 'Morning Star'?", "options": ["Mars", "Venus", "Mercury", "Jupiter"],
                 "answer": "Venus"},
                
                {"question": "In what year did the Titanic sink?", "options": ["1910", "1912", "1915", "1918"],
                 "answer": "1912"},
                
                {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue whale", "Giraffe", "Hippopotamus"],
                 "answer": "Blue whale"},
                
                {"question": "Who discovered penicillin?", "options": ["Marie Curie", "Alexander Fleming", "Louis Pasteur", "Jonas Salk"],
                 "answer": "Alexander Fleming"},
                
                {"question": "Which country is known as the Land of the Rising Sun?", "options": ["China", "Japan", "South Korea", "Vietnam"],
                 "answer": "Japan"},
                
                {"question": "What is the speed of light?", "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "200,000 km/s"],
                 "answer": "300,000 km/s"},
                
                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Who is the lead singer of the band Queen?", "options": ["Freddie Mercury", "John Lennon", "Mick Jagger", "David Bowie"],
                 "answer": "Freddie Mercury"},

                {"question": "What is the currency of Japan?", "options": ["Yuan", "Yen", "Won", "Baht"],
                 "answer": "Yen"},

                {"question": "Which element has the chemical symbol 'He'?", "options": ["Helium", "Hydrogen", "Hafnium", "Hassium"],
                 "answer": "Helium"},

                {"question": "What is the square of 9?", "options": ["81", "64", "49", "81"],
                 "answer": "81"},
                
                {"question": "In which year did Christopher Columbus first reach the Americas?", "options": ["1492", "1500", "1510", "1498"],
                 "answer": "1492"},
                
                {"question": "What is the main ingredient in guacamole?", "options": ["Tomatoes", "Avocado", "Onions", "Peppers"],
                 "answer": "Avocado"},
                
                {"question": "Who painted 'Starry Night'?", "options": ["Claude Monet", "Pablo Picasso", "Vincent van Gogh", "Salvador Dali"],
                 "answer": "Vincent van Gogh"},

                {"question": "What is the largest desert in the world?", "options": ["Sahara Desert", "Gobi Desert", "Antarctic Desert", "Arabian Desert"],
                 "answer": "Antarctic Desert"},

                {"question": "Which element has the chemical symbol 'K'?", "options": ["Potassium", "Calcium", "Cobalt", "Krypton"],
                 "answer": "Potassium"},

                {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Endoplasmic reticulum", "Golgi apparatus"],
                 "answer": "Mitochondria"},
                
                {"question": "How many chromosomes do humans typically have?", "options": ["42", "46", "50", "52"],
                 "answer": "46"},

                {"question": "What is the largest organ in the human body?", "options": ["Liver", "Skin", "Heart", "Brain"],
                 "answer": "Skin"},

                {"question": "Who wrote '1984'?", "options": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "J.K. Rowling"],
                 "answer": "George Orwell"},

                {"question": "What is the capital of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
                 "answer": "Canberra"},
                
                {"question": "How many colors are there in a rainbow?", "options": ["5", "7", "9", "12"],
                 "answer": "7"},

                {"question": "What is the largest planet in our solar system?", "options": ["Mars", "Earth", "Jupiter", "Saturn"],
                 "answer": "Jupiter"},

                {"question": "Which of the following is a noble gas?", "options": ["Oxygen", "Helium", "Nitrogen", "Carbon dioxide"],
                 "answer": "Helium"},

                {"question": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "N2"],
                 "answer": "H2O"},

                {"question": "How many sides does a dodecagon have?", "options": ["10", "11", "12", "13"],
                 "answer":"12"},

                {"question": "Who wrote 'The Great Gatsby'?", "options": ["F. Scott Fitzgerald", "Ernest Hemingway", "J.D. Salinger", "Jane Austen"],
                 "answer": "F. Scott Fitzgerald"},

                {"question": "What is the largest bird in the world?", "options": ["Eagle", "Ostrich", "Penguin", "Albatross"],
                 "answer": "Ostrich"},
                
                {"question": "Which of the following is a prime number?", "options": ["1", "2", "4", "6"],
                 "answer": "2"},

                {"question": "What is the chemical symbol for iron?", "options": ["I", "Fe", "Au", "Ag"],
                 "answer": "Fe"},

                {"question": "In what year did the first manned moon landing occur?", "options": ["1967", "1969", "1971", "1973"],
                 "answer": "1969"},
                {"question": "What is the largest mountain range on Earth?", "options": ["Rocky Mountains", "Himalayas", "Andes", "Alps"], "answer": "Himalayas"},

                {"question": "Who wrote 'The Catcher in the Rye'?", "options": ["J.K. Rowling", "J.D. Salinger", "Ernest Hemingway", "F. Scott Fitzgerald"],
                 "answer": "J.D. Salinger"},

                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Which planet is known as the 'Red Planet'?", "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                 "answer": "Mars"},

                {"question": "What is the capital of Brazil?", "options": ["Rio de Janeiro", "Brasília", "Sao Paulo", "Salvador"],
                 "answer": "Brasília"},

                {"question": "What is the chemical symbol for gold?", "options": ["Gd", "Au", "Ag", "Pt"],
                 "answer": "Au"},

                {"question": "How many bones are there in the adult human body?", "options": ["206", "180", "220", "250"],
                 "answer": "206"},

                {"question": "Who painted the Sistine Chapel ceiling?", "options": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
                 "answer": "Michelangelo"},

                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},
                {"question": "What is the capital of China?", "options": ["Beijing", "Shanghai", "Hong Kong", "Taipei"],
                 "answer": "Beijing"},

                {"question": "How many planets in our solar system have rings?", "options": ["1", "2", "4", "6"],
                 "answer": "6"},

                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Who is the author of 'The Odyssey'?", "options": ["Homer", "Virgil", "Dante", "Sophocles"],
                 "answer": "Homer"},

                {"question": "What is the chemical symbol for oxygen?", "options": ["O2", "O", "Ox", "Om"],
                 "answer": "O"},

                {"question": "In what year did the Berlin Wall fall?", "options": ["1987", "1989", "1991", "1993"],
                 "answer": "1989"},

                {"question": "What is the capital of South Korea?", "options": ["Seoul", "Busan", "Incheon", "Daegu"],
                 "answer": "Seoul"},

                {"question": "Who developed the theory of relativity?", "options": ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"],
                 "answer": "Albert Einstein"},

                {"question": "What is the chemical symbol for silver?", "options": ["Si", "S", "Ag", "Sr"],
                 "answer": "Ag"},
                
                
                {"question": "What is the speed of sound in air?", "options": ["343 meters per second", "500 meters per second", "700 meters per second", "1000 meters per second"],
                 "answer": "343 meters per second"},

                {"question": "Which gas is responsible for the greenhouse effect?", "options": ["Nitrogen", "Carbon dioxide", "Oxygen", "Methane"],
                 "answer": "Carbon dioxide"},

                {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Jane Austen", "Emily Brontë", "Charlotte Brontë", "F. Scott Fitzgerald"],
                 "answer": "Jane Austen"},

                {"question": "What is the largest mammal on land?", "options": ["Elephant", "Giraffe", "Blue whale", "African Elephant"],
                 "answer": "African Elephant"},

                {"question": "What is the chemical symbol for lead?", "options": ["Ld", "Pb", "Le", "Pt"],
                 "answer": "Pb"},

                {"question": "In what year did the United States declare independence?", "options": ["1765", "1776", "1789", "1799"],
                 "answer": "1776"},

                {"question": "Which of the following is a prime number?", "options": ["15", "23", "30", "42"],
                 "answer": "23"},

                {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"],
                 "answer": "Paris"},

                {"question": "Who is known as the 'Father of Computers'?", "options": ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"],
                 "answer": "Charles Babbage"},
                
                {"question": "What is the chemical symbol for sodium?", "options": ["So", "Sd", "Na", "No"],
                 "answer": "Na"},

                {"question": "How many chambers are there in the human heart?", "options": ["2", "3", "4", "5"],
                 "answer": "3"},

                {"question": "Who wrote 'The Canterbury Tales'?", "options": ["William Shakespeare", "Geoffrey Chaucer", "John Milton", "Dante Alighieri"],
                 "answer": "Geoffrey Chaucer"},
                
                {"question": "What is the boiling point of water in Fahrenheit?", "options": ["100°F", "212°F", "150°F", "32°F"],
                 "answer": "212°F"},
                
                {"question": "What is the chemical symbol for helium?", "options": ["H", "He", "Ha", "Hu"],
                 "answer": "He"},
                
                {"question": "In what year did the Renaissance begin?", "options": ["1200", "1300", "1400", "1500"],
                 "answer": "1400"},

                {"question": "What is the capital of Russia?", "options": ["St. Petersburg", "Moscow", "Kiev", "Warsaw"],
                 "answer": "Moscow"},

                {"question": "Who discovered the law of gravity?", "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Johannes Kepler"],
                 "answer": "Isaac Newton"},


                {"question": "What is the chemical symbol for carbon?", "options": ["Ca", "C", "Co", "Cr"],
                 "answer": "C"},

                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},

                {"question": "Who painted 'The Last Supper'?", "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
                 "answer": "Leonardo da Vinci"},

                {"question": "What is the capital of Argentina?", "options": ["Rio de Janeiro", "Buenos Aires", "Santiago", "Lima"],
                 "answer": "Buenos Aires"},

                {"question": "What is the chemical symbol for nitrogen?", "options": ["N2", "Ni", "No", "Na"],
                 "answer": "N2"},

                {"question": "How many players are there on a standard soccer team?", "options": ["9", "11", "13", "15"],
                 "answer": "11"},
                
                {"question": "Who wrote 'War and Peace'?", "options": ["Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Vladimir Nabokov"],
                 "answer": "Leo Tolstoy"},
                
                {"question": "What is the capital of South Africa?", "options": ["Cape Town", "Johannesburg", "Pretoria", "Bloemfontein"],
                 "answer": "Cape Town"},
                
                {"question": "What is the chemical symbol for potassium?", "options": ["P", "K", "Pt", "Ka"],
                 "answer": "K"},
                
                {"question": "In what year was the Declaration of Independence signed?", "options": ["1776", "1789", "1800", "1812"],
                 "answer": "1776"},
                
                {"question": "What is the largest moon in our solar system?", "options": ["Titan", "Ganymede", "Io", "Europa"],
                 "answer": "Ganymede"},
                
                
                {"question": "Who is the author of 'The Grapes of Wrath'?", "options": ["Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "Harper Lee"],
                 "answer": "John Steinbeck"},
                
                {"question": "What is the chemical symbol for tin?", "options": ["Ti", "Tn", "Sn", "Si"],
                 "answer": "Sn"},
                
                {"question": "In what year did the French Revolution begin?", "options": ["1776", "1789", "1804", "1815"],
                 "answer": "1789"},
                
                {"question": "What is the capital of Turkey?", "options": ["Ankara", "Istanbul", "Athens", "Budapest"],
                 "answer": "Ankara"},
                
                {"question": "Who painted 'The Persistence of Memory'?", "options": ["Salvador Dali", "Pablo Picasso", "Claude Monet", "Vincent van Gogh"],
                 "answer": "Salvador Dali"},
                
                {"question": "What is the chemical symbol for uranium?", "options": ["Ur", "Un", "U", "Ut"],
                 "answer": "U"},
                
                {"question": "In what year did the Great Fire of London occur?", "options": ["1600", "1666", "1700", "1755"],
                 "answer": "1666"},
                
                {"question": "What is the largest desert in Africa?", "options": ["Sahara Desert", "Kalahari Desert", "Namib Desert", "Libyan Desert"],
                 "answer": "Sahara Desert"},
                
                {"question": "Who wrote 'The Scarlet Letter'?", "options": ["Nathaniel Hawthorne", "Emily Brontë", "Herman Melville", "F. Scott Fitzgerald"],
                 "answer": "Nathaniel Hawthorne"},
                
                {"question": "What is the chemical symbol for magnesium?", "options": ["Mg", "Mn", "Mo", "Me"],
                 "answer": "Mg"},
                
                {"question": "In what year did World War II end?", "options": ["1943", "1945", "1947", "1950"],
                 "answer": "1945"},
            ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Brain Teaser":
            self.topics = [
                {"question": " What has keys but can't open locks?", "options": ["Piano", "Guitar", "Typewriter", "Drum"],
                 "answer": "Drum"},
                
                {"question": "What has keys but can't open locks?","options": ["Piano", "Computer", "Book", "Clock"],
                 "answer": "Clock"},
                
                {"question": "What has a heart that doesn't beat?","options": ["Apple", "Artichoke", "Tomato", "Lettuce"],
                 "answer": "Lettuce"},
                
                {"question": "I speak without a mouth and hear without ears.\n What am I?","options": ["Echo", "Wind", "Radio", "Thunder"],
                 "answer": "Echo"},
                
                {"question": "The more you take, the more you leave behind.\n What am I?","options": ["Footsteps", "Memories", "Choices", "Mistakes"],
                 "answer": "Footsteps"},
                
                {"question": "What comes once in a minute, twice in a moment,\n but never in a thousand years?","options": ["M", "E", "A", "O"],
                 "answer": "M"},
                
                {"question": "What has a head, a tail, is brown,\n and has no legs?","options": ["Penny", "Snake", "Earthworm", "Stick"],
                 "answer": "Penny"},
                
                {"question": "Forward I am heavy, but backward I am not. What am I?","options": ["Ton", "Weight", "Light", "Mass"],
                 "answer": "Ton"},
                
                {"question": "What has a neck but no head?","options": ["Bottle", "Giraffe", "Shirt", "Snake"],
                 "answer": "Bottle"},
                
                {"question": "I have keys but open no locks. What am I?","options": ["Keyboard", "Guitar", "Locksmith", "Calculator"],
                 "answer": "Locksmith"},
                
                {"question": "What has an endless supply of letters but starts empty?","options": ["Library", "Inbox", "Dictionary", "Envelope"],
                 "answer": "Library"},
                
                {"question": "What has a face and two hands but no body?","options": ["Clock", "Watch", "Mirror", "Doll"],
                 "answer": "Clock"},
                
                {"question": "I have cities but no houses, forests but no trees,\n and rivers but no water. What am I?","options": ["Map", "Dictionary", "Globe", "Puzzle"],
                 "answer": "Map"},
                
                {"question": "I can fly without wings. I can cry without eyes.\n Wherever I go, darkness follows me. What am I?","options": ["Cloud", "Wind", "Night", "Bat"],
                 "answer": "Cloud"},
                
                {"question": "What is as big as you are and yet does not weigh anything?","options": ["A Shadow", "A Thought", "A Dream", "A Reflection"],
                 "answer": "A Shadow"},
                
                {"question": "In a year, there are 12 months,\n seven months have 31 days.\n How many months have 28 days?","options": ["One", "Six", "Twelve", "All Twelve"],
                 "answer": "All Twelve"},
                
                {"question": "I’m tall when I’m young, and I’m short when I’m old,\n what am I?","options": ["A Tree", "A Person", "A Candle", "A Giraffe"],
                 "answer": "A Candle"},
                
                {"question": "What is so fragile that saying its name breaks it?","options": ["Silence", "Glass", "Egg", "Whisper"],
                 "answer": "Silence"},

                {"question": "What word is spelled wrong in the dictionary?","options": ["Incorrect", "Misspelled", "Dictionary", "Wrong"],
                 "answer": "Wrong"},

                {"question": "What can travel around the world while staying in a corner?","options": ["Stamp", "Postcard", "Airplane", "Stamp"],
                 "answer": "Stamp"},
                
                {"question": "What can run but not walk,\n has a mouth but never talks,\n has a head but never weeps, has a bed but never sleeps?","options": ["River", "Clock", "Car", "Wind"],
                 "answer": "River"},
                
                {"question": "Do you know what you can hold without ever touching it?","options": ["Breath", "Thought", "Emotion", "Memory"],
                 "answer": "Breath"},
                
                {"question": "Flat as a leaf, round as a ring;\n Has two eyes,\n can't see a thing. What is it?","options": ["Coin", "Button", "Camera", "Mirror"],
                 "answer": "Button"},
                
                {"question": "Where can you find roads without cars,forests without trees, \n and cities without houses  (without people)?","options": ["Map", "Imagination", "Dream", "Desert"],
                 "answer": "Map"},
                
                {"question": "What loses its head in the morning and gets it back at night?","options": ["Pillow", "Sunflower", "Clock", "Coin"],
                 "answer": "Pillow"},
                
                {"question": "A man pushes his car to a hotel and tells its owner that he is bankrupt. Why?","options": ["He lost a bet", "He's playing a game", "The car is a toy", "He's playing charades"],
                 "answer": "He's playing charades"},
                
                {"question": "When young, I am sweet in the sun.\n When middle-aged,I make you gay.\n When old, I am valued more than ever.","options": ["Wine", "Honey", "Friendship", "Gold"],
                 "answer": "Wine"},
                
                {"question": "How can you throw a ball as hard as you can and have it come back to you, \n even if it doesn't bounce off anything? There is nothing attached to it, \n and no one else catches or throws it back to you.","options": ["Throw it up", "Throw it underwater", "Throw it at a wall", "Throw it with a boomerang"],
                 "answer": "Throw it up"},
                
                {"question": "Imagine you’re in a room that is filling with water. \nThere are no windows or doors. How do you get out?","options": ["Stop imagining", "Swim through the water", "Evaporate the water", "Wait for it to drain"],
                 "answer": "Stop imagining"},
                
                {"question": "Feed me and I live, yet give me a drink and I die.","options": ["Fire", "Plant", "Air", "Time"],
                 "answer": "Fire"},
                
                {"question": "You are a cyclist in a cross-country race. \nJust before the crossing finish line you overtake the person in second place!\n What place did you finish in?","options": ["First", "Second", "Third", "Impossible to determine"],
                 "answer": "Second"},
                
                {"question": "With pointed fangs I sit and wait;\n With piercing force I crunch out fate; Grabbing victims, proclaiming might; \n Physically joining with a single bite. What am I?","options": ["Snake", "Spider", "Mosquito", "Vampire"],
                 "answer": "Mosquito"},
                
                {"question": "A farmer has 17 sheep and all but 9 die. How many are left?","options": ["8", "9", "17", "None"],
                 "answer": "9"},
                
                {"question": "A man was driving a black truck.\n His lights were not on. The moon was not out.,\n A lady was crossing the street. How did the man see her?","options": ["It was daytime", "He had night vision", "Street lights were on", "The lady had a flashlight"],
                 "answer": "It was daytime"},
                
                {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?","options": ["The Letter M", "An Idea", "A Memory", "A Dream"],
                 "answer": "The Letter M"},
                
                {"question": "What has six faces, but does not wear makeup, \n has twenty-one eyes, but cannot see? What is it?","options": ["Dice", "Spider", "Book", "Potato"],
                 "answer": "Dice"},
                
                {"question": "You live in a one-story house made entirely of redwood. What color would the stairs be?","options": ["Red", "There are no stairs", "Brown", "White"],
                 "answer": "There are no stairs"},
                
                {"question": "You are in a room with 3 monkeys. One monkey has a banana, one has a stick, and one has nothing.\n Who is the smartest primate?","options": ["Banana monkey", "Stick monkey", "Monkey with nothing", "All equally smart"],
                 "answer": "All equally smart"},
                
                {"question": "This old one runs forever, but never moves at all. He has not lungs nor throat,\n but still a mighty roaring call. What is it?","options": ["A River", "A Mountain", "A Waterfall", "Time"],
                 "answer": "Time"},
                
                {"question": "What five-letter word becomes shorter when you add two letters to it?","options": ["Short", "Brief", "Small", "Quick"],
                 "answer": "Short"},
                
                {"question": "If you drop a white hat into the red sea what does it become?","options": ["Wet", "Pink", "Lost", "Nothing"],
                 "answer": "Wet"},
                
                {"question": "One company owner asks another:\n 'Tell me, Bill, how come your employees are always on time in the mornings?'","options": ["Good Discipline", "Strict Rules", "Early Shifts", "They work from home"],
                 "answer": "They work from home"},
                
                {"question": "When it is alive we sing, when it is dead we clap our hands. What is it?","options": ["Birthday Cake", "Candle", "Fireworks", "Concert"],
                 "answer": "Candle"},
                
                {"question": "What is special about these words: job, polish, herb?","options": ["Pronounced differently","Same number of letters","Palindromes","Start with the same letter"],
                 "answer": "Start with the same letter"},
                
                {"question": "I am taken from a mine, \n and shut up in a wooden case, \n from which I am never released, \n and yet I am used by almost everybody. What am I?","options": ["Gold", "Diamond", "Silver", "Pencil"],
                 "answer": "Pencil"},
                
                {"question": "A man stands on one side of a river,\n his dog on the other. The man calls his dog, \n who immediately crosses the river without getting wet and without using a bridge or a boat.\n How did the dog do it?","options": [ "The river is frozen","The man throws a stick","There is a bridge","The man and the dog are not real"],
                 "answer": "The man and the dog are not real"},
                
                {"question": "I can't be bought, \n but I can be stolen with a glance. \n I'm worthless to one, \n but priceless to two. What am I?","options": ["Love", "Diamond", "Time", "Happiness"],
                 "answer": "Love"},

                {"question": "Turn me on my side and I am everything. Cut me in half and I am nothing. What am I?","options": ["8", "Infinity", "Zero", "O"],
                 "answer": "Infinity"},
                
                {"question": "No matter how little or how much you use me, you change me every month. What am I?","options": ["Water", "Soap", "Money", "Calendar"],
                 "answer": "Calendar"},
                
                {"question": "How can 8 + 8 = 4?","options": ["Roman numerals", "Magic", "Math error", "Cryptic code"],
                 "answer": "Math error"},
                
                {"question": "What has cities, but no houses; forests, but no trees; and water, but no fish?","options": ["Map", "Globe", "Library", "Internet"],
                 "answer": "Map"},
                
                {"question": "A red house is made from red bricks. \n A blue house is made from blue bricks. \n A yellow house is made from yellow bricks. \n What is a greenhouse made from?","options": ["Green bricks", "Plastic", "Glass", "Wood"],
                 "answer": "Glass"},
                
                {"question": "There is a word in the English language in which the first two letters signify a male, \n the first three letters signify a female, \nthe first four signify a great man, and the whole word, \n a great woman. What is the word?","options": ["History", "Future", "Present", "Past"],
                 "answer": "Present"},
                
                {"question": "In my hand I have two coins that are newly minted. \n Together,they total 30 cents. One isn’t a nickel. \n What are the coins?","options": ["Quarter and Nickel", "Dime and Nickel", "Dime and Penny", "Quarter and Dime"],
                 "answer": "Dime and Penny"},
                
                {"question": "What is harder to catch the faster you run?","options": ["Breath", "Cold", "Illness", "Time"],
                 "answer": "Time"},

                {"question": "What kind of running means walking?","options": ["Running water", "Running out", "Running shoes", "Running nose"],
                 "answer": "Running nose"},
                
                {"question": "What can be swallowed, but can also swallow you?","options": ["Pride", "Fear", "Anger", "Water"],
                 "answer": "Water"},
                
                {"question": "They fill me up and you empty me, \n almost every day; if you raise my arm, \n I work the opposite way. What am I?","options": ["Bank", "Pocket", "Gas tank", "Cup"],
                 "answer": "Gas tank"},
                
                {"question": "Which three letters can frighten a thief away? ICU","options": ["BOO", "ICE", "SOS", "911"],
                 "answer": "ICE"},
                
                {"question": "First I am dried, then I am wet. The longer I swim, the more taste you get. What am I?","options": ["Fish", "Tea", "Soup", "Sponge"],
                 "answer": "Tea"},
                
                {"question": "Lovely and round, I shine with pale light, grown in the darkness, A lady's delight. What am I?","options": ["Diamond", "Pearl", "Moon", "Sun"],
                 "answer": "Pearl"},
                
                {"question": "My voice is tender, my waist is slender \n and I'm often invited to play. Yet wherever I go I must take my bow \n or else I have nothing to say. What am I?","options": ["Flute", "Guitar", "Violin", "Trumpet"],
                 "answer": "Violin"},
                
                {"question": "I am a box that holds keys without locks, yet they can unlock your soul. What am I?","options": ["Safe", "Chest", "Piano", "Book"],
                 "answer": "Piano"},

                {"question": "I have a big mouth and I am also quite loud! \n I am NOT a gossip but I do get involved with everyone's dirty business. \n What am I?","options": ["Gossip", "Speaker", "Mouthwash", "Vacuum cleaner"],
                 "answer": "Mouthwash"},
                
                {"question": "I have four wings, but cannot fly,\n I never laugh and never cry; \n On the same spot I'm always found, \n toiling away with little sound. What am I?","options": ["Dragonfly", "Windmill", "Airplane", "Butterfly"],
                 "answer": "Windmill"},
                
                {"question": "What can be stolen, mistaken, or altered, yet never leaves you your entire life?","options": ["Memory", "Identity", "Heart", "Time"],
                 "answer": "Identity"},
                
                {"question": "Until I am measured, I am not known. Yet you miss me when I have flown. What am I?","options": ["Distance", "Time", "Air", "Love"],
                 "answer": "Time"},
                
                {"question": "Some try to hide, some try to cheat,\n  but time will show, we always will meet.\n Try as you might, to guess my name, \n I promise you'll know, when you do claim. Who am I?","options": ["Fate", "Destiny", "Death", "Life"],
                 "answer": "Death"},
                
                {"question": "Four cars come to a four-way stop,\n all coming from a different direction.\n They can't decide who got there first, \n so they all go forward at the same time. \n They do not crash into each other, but all four cars go. How is this possible?","options": ["Nighttime", "Traffic signal", "Roundabout", "They all made right-hand turns"],
                 "answer": "They all made right-hand turns"},
                
                {"question": "Take one out and scratch my head, I am now black but once was red. What am I?","options": ["Apple", "Tomato", "Match", "Cherry"],
                 "answer": "Match"},
                
                {"question": "I weaken all men for hours each day. I show you strange visions while you are away.\n I take you by night, by day take you back. None suffer to have me, but do from my lack. What am I?","options": ["Dream", "Imagination", "Sleep", "Nightmare"],
                 "answer": "Sleep"},

                {"question": "He has married many women, but has never been married. Who is he?","options": ["A polygamist", "A pastor", "A groom", "A preacher"],
                 "answer": "A preacher"},
                
                {"question": "My life is often a volume of grief,\n your help is needed to turn a new leaf.\n Stiff is my spine and my body is pale, \n but I'm always ready to tell a tale. What am I?","options": ["A book", "A candle", "A diary", "A letter"],
                 "answer": "A book"},
                
                {"question": "What has no hands but might knock on your door, and if it does you better open up?","options": ["Opportunity", "A storm", "A ghost", "A friend"],
                 "answer": "Opportunity"},
                
                {"question": "What do you throw out when you want to use it but take in when you don't want to use it?","options": ["Trash", "A lifeline", "An anchor", "A net"],
                 "answer": "An anchor"},
                
                {"question": "I can be short and sometimes hot. When displayed, I rarely impress. What am I?","options": ["Coffee", "Temperature", "Temper", "Fire"],
                 "answer": "Temper"},
                
                {"question": "What can be driven although it doesn't have wheels, sliced but stays whole?","options": ["A pie", "A golf ball", "A pizza", "A loaf of bread"],
                 "answer": "A golf ball"},
                
                {"question": "The cost of making only the maker knows, Valueless if bought,\n but sometimes traded. A poor man may give one as easily as a king. \nWhen one is broken, pain and deceit are assured. What is it?","options": ["A promise", "A diamond", "A secret", "A friendship"],
                 "answer": "A promise"},
                
                {"question": "What rocks but does not roll?","options": ["A mountain", "A boulder", "A chair", "A rocking chair"],
                 "answer": "A rocking chair"},
                
                {"question": "Shoot at me a thousand times and I may still survive.\n But, one scratch from me \n and you will find your prospects take a dive.\n What am I?","options": ["A bulletproof vest", "An eight-ball", "A shield", "A mirror"],
                 "answer": "An eight-ball"},
                
                {"question": "Why is the letter F like death?","options": ["It's the end", "It signifies failure", "Because without it life is a lie, or it makes life a lie.", "It's forbidden"],
                 "answer": "Because without it life is a lie, or it makes life a lie."},
                
                {"question": "You do not want to have it, But when you do have it, You do not want to lose it. What is it?","options": ["A headache", "A job", "A lawsuit", "A friend"],
                 "answer": "A lawsuit"},
                
                {"question": "Guess the next three letters in the series GTNTL.","options": ["I, T, S", "L, E, T", "F, O, R", "O, N, E"],
                 "answer": "I, T, S"},
                
                {"question": "Arnold Schwarzenegger has a long one. Michael J. Fox has a short one.\n Madonna does not use hers. Bill Clinton always uses his.\n The Pope never uses his. What is it?","options": ["A middle name", "A last name", "A stage name", "A nickname"],
                 "answer": "A last name"},
                
                {"question": "The number 8,549,176,320 is a unique number. What is so special about it?","options": ["It's a prime number", "It's the largest number", "It's a palindrome", "This is the only number that includes all the digits arranged in alphabetical order."],
                 "answer": "This is the only number that includes all the digits arranged in alphabetical order."},
                
                {"question": "Find a number less than 100 that is increased by \n one-fifth of its value when its digits are reversed.","options": ["27", "45", "63", "81"],
                 "answer": "45"},
                
                {"question": "What letter comes next in the following sequence? D R M F S L T _","options": ["X", "A", "E", "I"],
                 "answer": "E"},
    
                {"question": "You are in a place called Wally’s World and there is only one law. \n There is a mirror, but no reflection. There is pizza with cheese, but not sausage.\n There is pepper, but no salt. There is a door, yet no entrance or exit. What is the law?","options": ["No mirrors allowed", "No sausage on pizza", "No salt with pepper", "No entrance or exit allowed"],
                 "answer": "No salt with pepper"},
                
                {"question": "I come in different shapes and sizes. Parts of me are curved, \n other parts are straight. You can put me anywhere you like, \n but there is only one right place for me. What am I?","options": ["A tool", "A puzzle piece", "A toy", "A building block"],
                 "answer": "A puzzle piece"},
                
                {"question": "I have no eyes, no legs, or ears, and I help move the earth. What am I?","options": ["A tractor", "An earthworm", "A shovel", "A bulldozer"],
                 "answer": "An earthworm"},
                
                {"question": "A sundial has the fewest moving parts of any timepiece. Which has the most?","options": ["An hourglass, with thousands of grains of sand", "A digital clock", "A pendulum clock", "A wall clock"],
                 "answer": "An hourglass, with thousands of grains of sand"},
                
                {"question": "Put a coin into an empty bottle and insert a cork into the neck.\n How can you remove the coin \n without removing the cork or breaking the bottle?","options": ["Use a straw to push the coin out", "Turn the bottle upside down and shake the coin out", "Break the bottle to get the coin", "Use a vacuum cleaner"],
                 "answer": "Turn the bottle upside down and shake the coin out"},
                
                {"question": "In 1990, a person was 15 years old. In 1995,\n that same person was 10 years old. How can this be?","options": ["Time travel", "The person ages backward", "It's a mistake", "The person has a twin"],
                 "answer": "The person ages backward"},

                {"question": "Two boxers are in a match scheduled for 12 rounds. \n One of the boxers gets knocked out after only six rounds, yet no man throws a punch. \n How is this possible?","options": ["They are practicing shadow boxing", "Both the boxers were female", "The match was canceled", "The knocked-out boxer was injured"],
                 "answer": "Both the boxers were female"},
                
                {"question": "What does this mean? I RIGHT I","options": ["I have the right", "Turn right", "Right between the eyes", "I am right"],
                 "answer": "Right between the eyes"},
                
                {"question": "I have a large money box, 10 inches wide and 5 inches tall.\n Roughly how many coins can I place until \n my money box is no longer empty?","options": ["One", "Five", "As many as you want", "Just one, after which it will no longer be empty."],
                 "answer": "Just one, after which it will no longer be empty."},
                
                {"question": "Brothers and sisters I have none but this man's father is my father's son. Who is the man?","options": ["My son", "My nephew", "My brother", "My cousin"],
                 "answer": "My brother"},
                
                {"question": "Who makes it, has no need of it. Who buys it, has no use for it.\n Who uses it can neither see nor feel it. What is it?","options": ["A coffin", "A hat", "A shoe", "A wedding ring"],
                 "answer": "A coffin"},
                
                {"question": "What can you keep after giving to someone?","options": ["A promise", "A secret", "A smile", "A loan"],
                 "answer": "A promise"}
                ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Mythology":
            self.topics = [
                {"question": " In Greek mythology, who was the\ngod of the sky?", "options": ["Zeus", "Poseidon", "Hades", "Apollo"],
                 "answer": "Apollo"},
                {"question": "In Norse mythology, what is the\nname of the hammer wielded by Thor?", "options": ["Gungnir", "Mjolnir", "Excalibur", "Caladbolg"],
                 "answer": "Mjolnir"},
                {"question": " In Hindu mythology, who is the\ngod of destruction?", "options": ["Vishnu", "Shiva", "Brahma", "Indra"],
                 "answer": "Shiva"},
                {"question": " In Egyptian mythology, who is\nthe god of the afterlife?", "options": [" Anubis", "Osiris", "Horus", "Ra"],
                 "answer": "Osiris"},
                {"question": "In Greek mythology, who is the god of wine?", "options": ["Dionysus", "Hermes", "Apollo", "Ares"],
                 "answer": "Dionysus"},
                {"question": " In Norse mythology, what is the name of the\nserpent that encircles the world?", "options": ["Jormungand", "Nidhogg", "Fenrir", "Hel"],
                 "answer": "Jormungand"},
                {"question": "In Greek mythology, who is the god of the sea?", "options": ["Poseidon", "Zeus", "Hades", "Apollo"],
                 "answer": "Poseidon"},
                {"question": "In Hindu mythology, who is the god of love?", "options": ["Vishnu", "Shiva", "Brahma", "Kama"],
                 "answer": "Kama"},
                {"question": "In Egyptian mythology, who is\nthe goddess of magic?", "options": ["Isis", "Hathor", "Bastet", "Sekhmet"],
                 "answer": "Isis"},
                {"question": " In Greek mythology, who is the god of war?", "options": ["Ares", "Hermes", "Apollo", "Dionysus"],
                 "answer": "Ares"},
                {"question": "Who is the king of the gods?", "options": ["Ares", "Zeus", "Apollo", "Dionysus"],
                 "answer": "Zeus"},
                {"question": " Who is the goddess of beauty and love?", "options": ["Ares", "Zeus", "Apollo", "Aphrodite"],
                 "answer": "Aphrodite"},
                {"question": " Who is the queen of the gods?", "options": ["Hera", "Hermes", "Apollo", "Dionysus"],
                 "answer": "Hera"},
                {"question": "Who was the leader of the Argonauts?", "options": ["Ares", "Hermes", "Jason", "Dionysus"],
                 "answer": "Jason"},
                {"question": " Who was the nymph Apollo chased?", "options": ["Ares", "Daphne", "Jason", "Dionysus"],
                 "answer": "Daphne"},
                {"question": " What did Prometheus gift to humanity?", "options": ["Earth", "Fire", "Water", "Wind"],
                 "answer": "Fire"},
                {"question": "Who flew too close to the sun?", "options": ["Ares", "Icarus", "Jason", "Dionysus"],
                 "answer": "Icarus"},
                {"question": " Who was the goddess of the rainbow?", "options": ["Hera", "Hermes", "Iris", "Dionysus"],
                 "answer": "Iris"},
                {"question": " How many Greek gods lived on Mount Olympus?", "options": ["8", "16", "10", "12"],
                 "answer": "12"},
                {"question": "Who was the Greek goddess of Earth?", "options": ["Gaia", "Hermes", "Iris", "Dionysus"],
                 "answer": "Gaia"},
                {"question": "Who was the first human woman\ncreated by the Greek gods?", "options": ["Ares", "Daphne", "Pandora", "Dionysus"],
                 "answer": "Pandora"},
                {"question": "Which Greek goddess had snakes for hair?", "options": ["Gaia", "Hermes", "Medusa", "Dionysus"],
                 "answer": "Medusa"},
                {"question": "How long did it take Odysseus to\nget home from the Trojan War?", "options": ["8 years", "16 years", "10 years", "12 years"],
                 "answer": "10 years"},
                {"question": "What monster did Theseus slay?", "options": ["Minotaur", "Nidhogg", "Fenrir", "Hel"],
                 "answer": "Minotaur"},
                {"question": "Who were the parents of all Titans?", "options": ["Apollo and Daphne", "Zeus and Hera", "Gaea and Uranus", "Hades abd Aprodite"],
                 "answer": "Gaea and Uranus"},
                {"question": "Who designed the labyrinth for King Minos?", "options": ["Gaia", "Hermes", "Iris", "Daedalus"],
                 "answer": "Daedalus"},
                {"question": "Which Greek god formed dreams?", "options": ["Morpheus", "Hermes", "Iris", "Daedalus"],
                 "answer": "Morpheus"},
                {"question": "What’s the staff carried by Hermes called?", "options": ["Xiphos", "Gastraphetes", "Caduceus", "Sarissa"],
                 "answer": "Caduceus"},
                {"question": "Who was the Greek goddess of memory?", "options": ["Morpheus", "Hermes", "Iris", "Mnemosyne"],
                 "answer": "Mnemosyne"},
                {"question": "Who was the Greek goddess of victory?", "options": ["Nike", "Hermes", "Medusa", "Dionysus"],
                 "answer": "Nike"},
                {"question": "Which goddess is Apollo’s twin sister?", "options": ["Morpheus", "Artemis", "Iris", "Mnemosyne"],
                 "answer": "Artemis"},
                {"question": "What was the name of the horse Bellerophon rode?", "options": ["Jormungand", "Nidhogg", "Fenrir", "Pegasus"],
                 "answer": "Pegasus"},
                {"question": "Who was the Greek god of the underworld?", "options": ["Zeus", "Hades", "Poseidon", "Apollo"],
                 "answer": "Hades"},
                {"question": "Who was the Greek goddess of wisdom and war?", "options": ["Athena", "Hades", "Poseidon", "Apollo"],
                 "answer": "Athena"},
                {"question": "How many times did Hercules defeat Ares?", "options": ["Once", "twice", "Trice", "All of Above"],
                 "answer": "Twice"},
                {"question": " Who was the god of blacksmiths and fire?", "options": ["Zeus", "Hades", "Poseidon", "Hephaestus"],
                 "answer": "Hephaestus"},
                {"question": " Whose sacred animal is the quail?", "options": ["Jormungand", "Nidhogg", "Asteria", "Pegasus"],
                 "answer": "Asteria"},
                {"question": "Who was the goddess of music and dance?", "options": ["Athena", "Mousai", "Poseidon", "Apollo"],
                 "answer": "Mousai"},
                {"question": "Which Greek god rode a panther?", "options": ["Zeus", "Dionysus", "Poseidon", "Hephaestus"],
                 "answer": "Dionysus"},
                {"question": "Who held up the sky?", "options": ["Atlas", "Artemis", "Iris", "Mnemosyne"],
                 "answer": "Atlas"},
                {"question": "Who was the Greek god of sleep?", "options": ["Zeus", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Hypnos"},
                {"question": "Who was the Greek counterpart of Cupid?", "options": ["Atlas", "Artemis", "Iris", "Eros"],
                 "answer": "Eros"},
                {"question": "How many heads did the ant-eating\nserpent Amphisbaena have?", "options": ["3", "6", "1", "2"],
                 "answer": "2"},
                {"question": "Who was placed among the stars as\nthe constellation Aquarius?", "options": ["Ganymedes", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Ganymedes"},
                {"question": " What was a female monster with the lion’s body,\neagle’s wings, and woman’s head and breasts?", "options": ["Jormungand", "Nidhogg", "The Sphinx", "Pegasus"],
                 "answer": "The Sphinx"},
                {"question": "Who was the goddess of the dawn?", "options": ["Eos", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Eos"},
                {"question": "Who was the first wife of Zeus?", "options": ["Hera", "Athena", "Daphne", "Meis"],
                 "answer": "Metis"},
                {"question": "Who was the king of Pherae in the region\nof Thessaly and son of Pheres?", "options": ["Percy", "Kratos", "Hector", "Admetus"],
                 "answer": "Admetus"},
                {"question": "Which Trojan prince was considered\nthe greatest warrior of Troy?", "options": ["Percy", "Kratos", "Hector", "Admetus"],
                 "answer": "Hector"},
                {"question": "Which of Poseidon’s sons became the\ndemigod of the sea?", "options": ["Triton", "Kratos", "Hector", "Admetus"],
                 "answer": "Triton"},
                {"question": "Which Greek monster had 12 tentacles\nand six heads?", "options": ["Fenrir", "Hel", "Nidhogg", "Scylla"],
                 "answer": "Scylla"},
                {"question": "Who did Zeus put in an eternal sleep?", "options": ["Eos", "Dionysus", "Endymion", "Hephaestus"],
                 "answer": "Endymion"},
                {"question": "Who helped Theseus escape the Labyrinth?", "options": ["Ariadne", "Dionysus", "Endymion", "Hephaestus"],
                 "answer": "Ariadne"},
                {"question": " Who was the god of questioning\nand the inquisitive mind?", "options": ["Hera", "Coeus", "Daphne", "Meis"],
                 "answer": "Coeus"},
                {"question": " Who cut out Philomela’s tongue?", "options": ["Eos", "Dionysus", "Endymion", "Tereus"],
                 "answer": "Tereus"},
                {"question": "Who understood the language of animals?", "options": ["Triton", "Kratos", "Melampus", "Admetus"],
                 "answer": "Melampus"},
                {"question": " Who did the Isthmian Games honor?", "options": ["Athena", "Hades", "Poseidon", "Apollo"],
                 "answer": "Poseidon"},
                {"question": " Who built the Trojan Horse?", "options": ["Athena", "Epeius", "Poseidon", "Apollo"],
                 "answer": "Epeius"},
                {"question": "Who was the goddess of magic and ghosts?", "options": ["Hecate", "Epeius", "Poseidon", "Apollo"],
                 "answer": "Hecate"},
                {"question": " Who wished that everything he\ntouched would turn into gold?", "options": ["Hecate", "Epeius", "Poseidon", "King Midas"],
                 "answer": "King Midas"},
                {"question": " Who gave Athens its name?", "options": ["Triton", "Kratos", "Cecrops", "Admetus"],
                 "answer": "Cecrops"},
                {"question": "Who did Hades abduct?", "options": ["Athena", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Persephone"},
                {"question": " How man goddesses were in the Kharites?", "options": ["4", "6", "1", "3"],
                 "answer": "3"},
                {"question": " Who was the Titan goddess of\ndivine law and order?", "options": ["Themis", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Themis"},
                {"question": "Who was the Greek god of wine-making\nand drunkenness?", "options": ["Themis", "Persephone", "Silenus", "Apollo"],
                 "answer": "Silenus"},
                {"question": " Who fell in love with a statue he carved?", "options": ["Pygmalion", "Kratos", "Melampus", "Admetus"],
                 "answer": "Pygmalion"},
                {"question": " Who was the Greek god of medicine?", "options": ["Athena", "Asclepius", "Poseidon", "Apollo"],
                 "answer": "Asclepius"},
                {"question": "Which Greek goddess helped Troy\nin the Trojan War?", "options": ["Penthesilea", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Penthesilea"},
                {"question": " Lord Rama belonged to which of\nthe following era or yuga?", "options": ["Dwapara", "Tret Yuga", "None of the above", "Kali"],
                 "answer": "Tret Yuga"},
                {"question": " According to Hindu mythology,\nKing Kansa was the uncle of ______.", "options": ["Rama", "Arjuna", "Krishna", "Duryodhana"],
                 "answer": "Krishna"},
                {"question": "Who among the following is the\ncharioteer of Lord Surya?", "options": ["Arjun", "Jallandhar", "Arun", "Karna"],
                 "answer": "Arjun"},
                {"question": " In Hindu mythology, who is also called ‘Mihira’?", "options": ["Indra", "Balrama", "Surya", "Bheema"],
                 "answer": "Surya"},
                {"question": " In Hindu mythology, who was the first man to die?", "options": ["Ganesha", "Narada", "Yama", "Indra"],
                 "answer": "Yama"},
                {"question": "Who is the god of death in Hindu mythology?", "options": ["Yama", "Indra", "Varuna", "Agni"],
                 "answer": "Yama"},
                {"question": " Who is the goddess of wealth and\nprosperity in Hindu mythology?", "options": ["Saraswati", "Lakshmi", "Durga", "Kali"],
                 "answer": "Lakshmi"},
                {"question": " In Mahabharat, Devavrata was the other name of:", "options": ["Arjun", "Bhishma", "Krishna", "Balaram"],
                 "answer": "Bhishma"},
                {"question": " How many incarnations of Vishnu appeared in\nSatya or Krita Yuga from his Dashavatar?", "options": ["3", "2", "5", "4"],
                 "answer": "4"},
                {"question": " Which one is the first avatar of\nLord Vishnu from his Dashavatar?", "options": ["Matsya", "Kurma", "Varah", "Narasimbha"],
                 "answer": "Matsya"},
                {"question": " In the Narasimbha avatar, Lord Vishnu killed:", "options": ["Hiranyakashipu", "Bali", "Ravan", "Mayasura"],
                 "answer": "Hiranyakashipu"},
                {"question": " In which Yuga, Shree Rama was born in Ayodhya?", "options": ["Satya Yuga", "Treta Yuga", "Dwapara Yuga", "Kali Yuga"],
                 "answer": "Treta Yuga"},
                {"question": " Sati (wife of Lord Shiva) was the daughter of:", "options": ["Kubera", "Daksha Prajapati", "Himavan", "None of the above"],
                 "answer": "Daksha Prajapati"},
                {"question": " Who wrote down the epic Mahabharata\nwhile Vyasa was dictating?", "options": ["Narada", "Vishwakarma", "Ganesha", "Shiva"],
                 "answer": "Ganesha"},
                {"question": " Who brought the River goddess Ganga to\nEarth from the heavens?", "options": ["Shree Rama", "Krishna", "Bhagiratha", "Raja Harishchandra"],
                 "answer": "Bhagiratha"},
                {"question": " In which Yuga, Krishna was born?", "options": ["Satya Yuga", "Treta Yuga", "Dwapara Yuga", "Kal Yuga"],
                 "answer": "Kal Yuga"},
                {"question": " What is the final incarnation of\nLord Vishnu in his Dashavatara?", "options": ["Kurma", "Krishna", "Parashuram", "Kalki"],
                 "answer": "Kalki"},
                {"question": " Who was the son of Fergus mac Roigh,\nwho was mortally wounded by Conall Cernach?", "options": ["Ith", "Iollan", "Iuchar", "Lucharba"],
                 "answer": "Lucharba"},
                {"question": " How many distinct chronological\ncycles are there in Irish mythology?", "options": ["3", "2", "5", "4"],
                 "answer": "4"},
                {"question": " Which one is the first cycle in Irish mythology?", "options": ["Mythological Cycle", "Ulster Cycle", "Fenian Cycle", "Historical Cycle"],
                 "answer": "Mythological Cycle"},
                {"question": " What is the name of the Brazilian goddess of the moon?", "options": ["Iansã", "Oxum", "Nanã", "Jaci"],
                 "answer": "Jaci"},
                {"question": " Who was the Great Queen, the archetypal form of the\nGoddess in Ireland, and often associated with war?", "options": ["Morrigan", "Morfessa", "Moriath", "Murine"],
                 "answer": "Morrigan"},
                {"question": " Which one is the Land of Youth and immortality where\ngods and men lived together in a world of beauty?", "options": ["Tir Na n’Og", "Tir Na mBeo", "Tir Na mBan", "Tir Tairngire"],
                 "answer": "Tir Na n’Og"},
                {"question": " Who was the wife of Mongan and was\nborn the same night as he?", "options": ["Dubhlaing", "Dubh Lacha", "Donn", "Diuran"],
                 "answer": "Dubh Lacha"},
                {"question": " Who was the hag who helped Mongan retrieve his wife?", "options": ["Coinchend", "Cuirithir", "Cuimhne", "Creidne"],
                 "answer": "Coinchend"},
                {"question": " Who was the leader of the first\ninvasion of Ireland and the chief of every craft?", "options": ["Patrick", "Paddy", "Pooka", "Partholon"],
                 "answer": "Partholon"},
                {"question": " Who was the master of wisdom who gave in to Lugh’s\nkeeping of the spear, which gave victory in battle?", "options": ["Esras", "Eremon", "Etain", "Esriu"],
                 "answer": "Esras"},
                {"question": " Who is the god of the underworld in Japanese mythology?", "options": ["Izanami", "Amaterasu", "Susanoo", "Emma-ö"],
                 "answer": "Emma-ö"},
                {"question": " Who is the god of wisdom and\nintelligence in Japanese mythology?", "options": ["Hachiman", "Inari", "Omoikane", "Susanoo"],
                 "answer": "Omoikane"},
                {"question": " Who is the god of the wind in Japanese mythology?", "options": ["Fujin", "Raijin", "Tsukuyomi", "Ryujin"],
                 "answer": "Fujin"},
                {"question": " Who is the god of agriculture in Japanese mythology?", "options": ["Inari", "Hachiman", "Susanoo", "Amaterasu"],
                 "answer": "Inari"},
                {"question": " Who is the god of war in Japanese mythology?", "options": ["Hachiman", "Inari", "Kagutsuchi", "Tsukuyomi"],
                 "answer": "Hachiman"},
            ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Music":
            self.topics = [
                {"question": " What singer is known as The Vocal Bible?", "options": ["Brandy", "Michael Jackson", "Prince", "Madonna"],
                 "answer": "Brandy"},
                {"question": " Who is known as the King of Pop?", "options": ["Elvis Presley", "Michael Jackson", "Madonna  D. Prince"],
                 "answer": "Michael Jackson"},
                {"question": "Which instrument does Yo-Yo Ma play?", "options": ["Violin","Cello", "Piano", "Flute "],
                 "answer": "Violin"},
                {"question": "What is the main ingredient in\ntraditional Irish folk music?", "options": ["Bagpipes", "Banjo", "Fiddle", "Accordion"],
                 "answer": "Fiddle"},
                {"question": "Who wrote the famous musical Les Misérables?", "options": ["Andrew Lloyd Webber", "Stephen Sondheim", "Claude-Michel Schönberg", "Rodgers and Hammerstein"],
                 "answer": "Claude-Michel Schönberg"},
                {"question": "Which rock band released the album\nThe Dark Side of the Moon?", "options": ["The Rolling Stones", "The Beatles", "Pink Floyd", "Led Zeppelin"],
                 "answer": "Pink Floyd"},
                {"question": "What genre is associated with Bob Marley?", "options": ["Reggae", "Hip-hop", "Country", "Blues"],
                 "answer": "Reggae"},
                {"question": "Who is known as the Queen of Soul?", "options": ["Whitney Houston", "Aretha Franklin", "Diana Ross", "Etta James"],
                 "answer": "Aretha Franklin"},
                {"question": "In classical music, which period does Beethoven belong to?", "options": ["Baroque", "Romantic", "Classical", "Renaissance"],
                 "answer": "Classical"},
                {"question": "What is the most common time signature in Western music?", "options": ["4/4", "3/4", "6/8", "2/2"],
                 "answer": "4/4"},
                {"question": "Who was the lead singer of the band Queen?", "options": ["Freddie Mercury", "David Bowie", "Roger Taylor", "Brian May"],
                 "answer": "Freddie Mercury"},
                {"question": "Which instrument is central to a mariachi band?", "options": ["Trumpet", "Guitar", "Violin", "Accordion"],
                 "answer": "Violin"},
                {"question": "What is the name of the classical composer known for his famous\nRide of the Valkyries?", "options": ["Ludwig van Beethoven", "Richard Strauss", "Wolfgang Amadeus Mozart", "Richard Wagner"],
                 "answer": "Richard Wagner"},
                {"question": "Which genre is often associated with artists like\nMuddy Waters and B.B. King?", "options": ["Jazz", "Blues", "Rock and Roll", "Country"],
                 "answer": "Blues"},
                {"question": "What is the primary woodwind\ninstrument in an orchestra?", "options": ["Clarinet", "Flute", "Oboe", "Bassoon"],
                 "answer": "Flute"},
                {"question": "Who sang the theme song for the\nJames Bond film Skyfall?", "options": ["Adele", "Beyoncé", "Rihanna", "Katy Perry"],
                 "answer": "Adele"},
                {"question": "Which Beatles album features the song Hey Jude?", "options": ["Reggae", "Hip-hop", "Country", "Blues"],
                 "answer": "Reggae"},
                {"question": "What genre is associated with Bob Marley?", "options": ["Abbey Road", "The White Album", "Sgt. Pepper's Lonely Hearts Club Band", "Let It Be"],
                 "answer": "The White Album"},
                {"question": "What is the highest male singing voice?", "options": ["Tenor", "Baritone", "Bass", "Countertenor"],
                 "answer": "Tenor"},
                {"question": "In which country did the flamenco\nmusic and dance originate?", "options": ["Spain", "Italy", "France", "Portugal"],
                 "answer": "Spain"},
                {"question": "Who composed The Four Seasons?", "options": ["Antonio Vivaldi", "Johann Sebastian Bach", "George Frideric Handel", "Wolfgang Amadeus Mozart"],
                 "answer": "Antonio Vivaldi"},
                {"question": "Who sang the hit song Careless Whisper?", "options": ["George Michael", "Michael Jackson", "Prince", "Madonna"],
                 "answer": "George Michael"},
                {"question": "Which band had a hit with\nthe song Sweet Child O’ Mine?", "options": ["Guns N’ Roses", "Bon Jovi", "Aerosmith", "Van Halen"],
                 "answer": "Guns N’ Roses"},
                {"question": "Who sang the song Billie Jean?", "options": ["Michael Jackson", "Prince", "Madonna", "Whitney Houston"],
                 "answer": "Michael Jackson"},
                {"question": "Which band had a hit with\nthe song Livin’ on a Prayer?", "options": ["Bon Jovi", "Guns N’ Roses", "Aerosmith", "Van Halen"],
                 "answer": "Bon Jovi"},
                {"question": "Who sang the song Like a Virgin?", "options": ["Madonna", "Whitney Houston", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Madonna"},
                {"question": "Which band had a hit with the song Jump?", "options": ["Van Halen", "Bon Jovi", "Guns N’ Roses", "Aerosmith"],
                 "answer": "Van Halen"},
                 {"question": "Who sang the song I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Whitney Houston"},
                 {"question": "Which band had a hit with\nthe song Every Breath You Take?", "options": ["The Police", "U2", "Duran Duran", "The Cure"],
                 "answer": "The Police"},
                 {"question": "Who sang the song Girls Just Want to Have Fun?", "options": ["Cyndi Lauper", "Madonna", "Whitney Houston", "Tina Turner"],
                 "answer": "Cyndi Lauper"},
                 {"question": "Which band had a hit with the song Take on Me?", "options": ["A-ha", "Duran Duran", "The Cure", "U2"],
                 "answer": "A-ha"},
                 {"question": "Who sang the hit song Stairway to Heaven?", "options": ["Led Zeppelin", "Pink Floyd", "The Rolling Stones", "The Beatles"],
                 "answer": "Led Zeppelin"},
                 {"question": "Which band had a hit with\nthe song Bohemian Rhapsody?", "options": ["Queen", "The Who", "The Doors", "The Kinks"],
                 "answer": "Queen"},
                 {"question": "Who sang the song Stayin’ Alive?", "options": ["Bee Gees", "ABBA", "The Jackson 5", "The Temptations"],
                 "answer": "Bee Gees"},
                 {"question": "Which band had a hit with\nthe song Hotel California?", "options": ["Eagles", "Fleetwood Mac", "Journey", "Boston"],
                 "answer": "Eagles"},
                 {"question": "Who sang the song I Will Survive?", "options": ["Gloria Gaynor", "Donna Summer", "Diana Ross", "Cher"],
                 "answer": "Gloria Gaynor"},
                 {"question": "Which band had a hit with the song Dream On?", "options": ["Aerosmith", "Van Halen", "Guns N’ Roses", "Bon Jov"],
                 "answer": "Aerosmith"},
                 {"question": "Who sang the song Imagine?", "options": ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
                 "answer": "John Lennon"},
                 {"question": "Which band had a hit with the song We Will Rock You?", "options": ["Queen", "AC/DC", "Black Sabbath", "Deep Purple"],
                 "answer": "Queen"},
                 {"question": "Who sang the song American Pie?", "options": ["Don McLean", "Bob Dylan", "Neil Young", "Jim Croce"],
                 "answer": "Don McLean"},
                 {"question": "Which band had a hit with the song Stayin’ Alive?", "options": ["Bee Gees", "ABBA", "The Jackson 5", "The Temptations"],
                 "answer": "Bee Gees"},
                 {"question": "Who sang the hit song What a Wonderful World?", "options": ["Louis Armstrong", "Frank Sinatra", "Elvis Presley", "The Beatles"],
                 "answer": "Louis Armstrong"},
                 {"question": "Which rock-and-roll star\nwas famously nicknamed The King?", "options": ["Elvis Presley", "Chuck Berry", "Little Richard", "Jerry Lee Lewis"],
                 "answer": "Elvis Presley"},
                 {"question": "Who sang Brown Eyed Girl?", "options": ["Van Morrison", "Bob Dylan", "Neil Young", "Jim Croce"],
                 "answer": "Van Morrison"},
                 {"question": "Which band recorded the album\nSgt. Pepper’s Lonely Hearts Club Band?", "options": ["The Beatles", "The Rolling Stones", "The Who", "Pink Floyd"],
                 "answer": "The Beatles"},
                 {"question": "Who sang the song\nI Heard It Through the Grapevine?", "options": ["Marvin Gaye", "Stevie Wonder", "Otis Redding", "James Brown"],
                 "answer": "Marvin Gaye"},
                 {"question": "Who sang the song My Girl?", "options": ["The Temptations", "The Four Tops", "The Supremes", "The Miracles"],
                 "answer": "The Temptations"},
                 {"question": "Who sang the song Respect?", "options": ["Aretha Franklin", "Diana Ross", "Gladys Knight", "Tina Turner"],
                 "answer": "Aretha Franklin"},
                 {"question": "Which band had a hit with the song Light My Fire?", "options": ["The Doors", "The Who", "The Kinks", "The Rolling Stones"],
                 "answer": "The Doors"},
                 {"question": "Who sang the song Ain’t No Mountain High Enough?", "options": ["Marvin Gaye and Tammi Terrell", "Diana Ross", "Stevie Wonder", "The Temptations "],
                 "answer": "Marvin Gaye and Tammi Terrell"},
                 {"question": "Who sang the song Blowin’ in the Wind?", "options": ["Bob Dylan", "Neil Young", "Jim Croce", "Simon & Garfunkel"],
                 "answer": "Bob Dylan"},
                 {"question": "Which of the following is\nnot a member of the Beatles?", "options": ["John Lennon", "Paul McCartney", "George Harrison", "Marvin Gaye"],
                 "answer": "Marvin Gaye"},
                 {"question": "Who is the lead singer of the band Coldplay?", "options": ["Chris Martin", "Jonny Buckland", "Guy Berryman", "Will Champion"],
                 "answer": "Chris Martin"},
                 {"question": "Which of the following is\nnot a song by Michael Jackson?", "options": ["Beat It", "Billie Jean", "Thriller", "Like a Virgin"],
                 "answer": "Like a Virgin"},
                 {"question": "Who is the lead singer of the band Queen?", "options": ["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"],
                 "answer": "Freddie Mercury"},
                 {"question": "Which of the following is not a song by Elvis Presley?", "options": ["Jailhouse Rock", "Hound Dog", "Blue Suede Shoes", "Imagine"],
                 "answer": "Whitney Houston"},
                 {"question": "Who sang the song “I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Imagine"},
                 {"question": "Who is the lead singer of the band U2?", "options": ["Bono", "The Edge", "Adam Clayton", "Larry Mullen Jr."],
                 "answer": "Bono"},
                 {"question": "Which of the following\nis not a song by The Rolling Stones?", "options": ["Satisfaction", "Paint It Black", "Brown Sugar", "Stairway to Heaven"],
                 "answer": "Stairway to Heaven"},
                 {"question": "Who is the lead singer of the band Led Zeppelin?", "options": ["Robert Plant", "Jimmy Page", "John Paul Jones", "John Bonham"],
                 "answer": "Robert Plant"},
                 {"question": "Who sang the song “I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Whitney Houston"},
                 {"question": "Who is the lead singer of the band Led Zeppelin?", "options": ["Robert Plant", "Jimmy Page", "John Paul Jones", "John Bonham"],
                 "answer": "Robert Plant"},
                 {"question": "Which of the following is not a song by The Beatles?", "options": ["Hey Jude", "Let It Be", "Imagine", "Yesterday"],
                 "answer": "Hey Jude"},
                 {"question": "Who is the lead singer of the band Pink Floyd?", "options": ["David Gilmour", "Roger Waters", "Syd Barrett", "Nick Mason"],
                 "answer": "Syd Barrett"},
                 {"question": "Who is the lead singer of the band Aerosmith?", "options": ["Steven Tyler", "Joe Perry", "Brad Whitford", "Tom Hamilton"],
                 "answer": "Steven Tyler"},
                 {"question": " Which of the following is not a song by The Doors?", "options": ["Riders on the Storm", "Light My Fire", "Break on Through", "Love Me Tender"],
                 "answer": "Love Me Tender"},
                 {"question": "Who is the lead singer of the band Guns N’ Roses?", "options": ["Axl Rose", "Slash", "Duff McKagan", "Izzy Stradlin "],
                 "answer": "Axl Rose"},
                 {"question": "Which of the following is not a song by Nirvana?", "options": ["Smells Like Teen Spirit", "Marvine Gaye", "Lithium", "Heart-Shaped Box", "John Bonham"],
                 "answer": "Marvine Gaye"},
                 {"question": "Who is the lead singer of the band Red Hot Chili Peppers?", "options": ["Anthony Kiedis", "Flea", "Chad Smith", "John Frusciante"],
                 "answer": "Anthony Kiedis"},
                 {"question": "Which of the following is not a song by The Who?", "options": ["Baba O’Riley", "Pinball Wizard", "Won’t Get Fooled Again", "Jumpin’ Jack Flash"],
                 "answer": "Jumpin’ Jack Flash"},
                 {"question": "Who is the lead singer of the band Van Halen?", "options": ["David Lee Roth", "Eddie Van Halen", "Alex Van Halen", "Michael Anthony"],
                 "answer": "David Lee Roth"},
                 {"question": "Which of the following is not a song by AC/DC?", "options": ["Back in Black", "Thunderstruck", "Highway to Hell", "Sweet Child O’ Mine"],
                 "answer": "Sweet Child O’ Mine"},
                 {"question": "Who is the lead singer of the band Pearl Jam?", "options": ["Eddie Vedder", "Stone Gossard", "Jeff Ament", "Mike McCready"],
                 "answer": "Eddie Vedder"},
                 {"question": "Which of the following is not a song by Pink Floyd?", "options": ["Another Brick in the Wall", "Comfortably Numb", "Time", "Money"],
                 "answer": "Time"},
                 {"question": " What singer has had a Billboard No. 1 hit in each of\nthe last four decades?", "options": ["The Rolling Stones", "Mariah Carey", "Pink Floyd", "Led Zeppelin"],
                 "answer": "Mariah Carey"},
                 {"question": "Who was the very first American Idol winner?", "options": ["Eddie Vedder", "Stone Gossard", "Jeff Ament", "Kelly Clarkson"],
                 "answer": "Kelly Clarkson"},
                 {"question": "Before Bleachers and fun., Jack Antonoff fronted what band?", "options": ["Steel Train", "Thunderstruck", "Highway to Hell", "Sweet Child O’ Mine"],
                 "answer": "Steel Train"},
                 {"question": "Before Miley Cyrus recorded Wrecking Ball\nit was offered to which singer?", "options": ["Axl Rose", "Slash", "Beyoncé", "Izzy Stradlin"],
                 "answer": "Beyoncé"},
                 {"question": "Which artist's entire 1985 Live Aid\nset consisted of just a single cover song?", "options": ["Elvis Costello", "Brian Adams", "Roger Taylor", "John Deacon"],
                 "answer": "Brian Adams"},
                 {"question": "What rock icon was the founder of The Society\nfor the Prevention of Cruelty to Long-haired Men?", "options": ["Anthony Kiedis", "David Bowie", "Chad Smith", "John Frusciante"],
                 "answer": "David Bowie"},
                 {"question": "Keith Moon and John Entwistle of The Who are said to\nhave inspired the name of which other classic rock band?", "options": ["Anthony Kiedis", "David Bowie", "Led Zeppelin", "John Frusciante"],
                 "answer": "Led Zeppelin"},
                 {"question": "Before Phil Collins, who was the lead singer of Genesis?", "options": ["Don McLean", "Bob Dylan", "Neil Young", "Peter Gabriel"],
                 "answer": "Peter Gabriel"},
                 {"question": "Who was Marvin Gaye's duet partner?", "options": ["Tammi Terrell", "Paul McCartney", "George Harrison", "Ringo Starr"],
                 "answer": "Tammi Terrell"},
                 {"question": "Who was the first woman ever inducted into the\nRock and Roll Hall of Fame?", "options": ["Don McLean", "Aretha Franklin", "Neil Young", "Peter Gabriel"],
                 "answer": "Aretha Franklin"},
                 {"question": "Who replaced Ozzy Osbourne as Black Sabbath’s lead singer?", "options": ["Ronnie James Dio", "Judas Priest", "Dokken", "Whitesnake"],
                 "answer": "Ronnie James Dio"},
                 {"question": "To consider a band as a Big Band, what is\nthe minimum number of musicians needed?", "options": [" 11", "21", "12", "10"],
                 "answer": "10"},
                 {"question": "Bjork was the lead singer of what\nIcelandic band before pursuing a solo career?", "options": ["Kukl", "The Sugarcubes", "Cocteau Twins", "The Elgar sisters"],
                 "answer": "The Sugarcubes"},
                 {"question": " In an Orchestra, which is the largest brass section instrument?", "options": ["Trumpet", "Tenor", "French horns", "Tuba"],
                 "answer": "Tuba"},
                 {"question": "Who released the album Alf?", "options": ["Alison Moyet", "Aretha Louise Franklin", "Michael Joseph Jackson", "Christopher Maurice"],
                 "answer": "Alison Moyet"},
                 {"question": "Who released the album Here, My Dear?", "options": ["Frankie Gaye", "Bruno Mars", "Elton John", "Marvin Gaye"],
                 "answer": "Marvin Gaye"},
                 {"question": "Which classical composer was deaf?", "options": ["Frankie Gaye", "Ludwig van Beethoven", "Elton John", "Marvin Gaye"],
                 "answer": "Ludwig van Beethoven"},
                 {"question": "A tribute to David Bowie’s ex-wife was given\nwith a song by The Rolling Stones, name the song?", "options": ["Wild Horses", "Gimme Shelter", "Angie", "Satisfaction"],
                 "answer": "Angie"},
                 {"question": "Who was the blues great born Ellas Otha Bates?", "options": ["Little Richard", "Muddy Waters", "Bo Diddley", "Chuck Berry"],
                 "answer": "Bo Diddley"},
                 {"question": "Which band has its name after a\nscientist from the movie Barbarella?", "options": ["Duran Duran", "A Ha", "Nile Rodgers", "Tears for fears"],
                 "answer": "Duran Duran"},
                 {"question": "Name the orchestral instrument that can play high notes?", "options": ["Viola", "Piccolo", "Violin", "Cellos"],
                 "answer": "Piccolo"},
                 {"question": "What is the all-time bestselling movie soundtrack?", "options": ["I have nothing", "My love is your love", "Waiting to exhale", "The Bodyguard: Original Soundtrack Album"],
                 "answer": "The Bodyguard: Original Soundtrack Album"},
                {"question": "What is the most played song on American\nradio during the 20th century?", "options": ["You’ve Lost That Loving Feeling", "Just Once in My Life", "Danger Zone", "Soul and Inspiration"],
                 "answer": "You’ve Lost That Loving Feeling"},
                {"question": "Who was the musical director of the\nNew York Philharmonic from 1958 to 1970?", "options": ["Jaap Van Zweden", "Alan Gilbert", "Leonard Bernstein", "Kurt Masur"],
                 "answer": "Leonard Bernstein"},
                {"question": "The Clawhammer is a playing style\nassociated with which instrument?", "options": ["Ukulele", "Banjo", "Mandolin", "Fiddle"],
                 "answer": "Banjo"},
                {"question": "Who won the 2001 Grammy Award for Best New Artist?", "options": ["Sam Smith", "Amy Winehouse", "Meghan Trainor", "Alicia Keys"],
                 "answer": "Alicia Keys"},
                {"question": "Who recorded Groove is in the Heart?", "options": ["Q-Tip", "Deee-Lite", "Technotronic", "The B-52’s"],
                 "answer": "Deee-Lite"},
                {"question": "Who is the lead singer of Evanescence?", "options": ["Jen Majura", "Lzzy Hale", "Ben Moody", "Amy Lee"],
                 "answer": "Amy Lee"},
                {"question": "Which musical group had the 1967 Top 10 single,\nI Think We’re Alone Now?", "options": ["The Beatles", "The Monkees", "The Turtles", "Tommy James and the Shondells"],
                 "answer": "Tommy James and the Shondells"},
                {"question": "Who wrote the musical composition Rhapsody in Blue?", "options": ["Leonard Bernstein", "Cole Porter", "Claude Debussy", "George Gershwin"],
                 "answer": "Tommy James and the Shondells"},
            ]
            random.shuffle(self.topics)
        
        elif self.subject_var.get() == "History":
            self.topics = [
                {"question": "  In which year did the French Revolution begin?", "options": ["1776", "1789", " 1804", "1820"],
                 "answer": " 1789"},
                {"question": " Who was the first President of the United States?", "options": ["Thomas Jefferson", " John Adams", "George Washington", " James Madison"],
                 "answer": "George Washington"},
                {"question": "The Magna Carta, signed in 1215, limited\nthe power of which monarch?", "options": ["Henry VIII", " Richard the Lionheart", " John I", "Edward I"],
                 "answer": "John I"},
                {"question": "Which ancient civilization built the city of Machu Picchu?", "options": ["Mayans", "Aztecs", " Incas", " Egyptians"],
                 "answer": " Incas"},
                {"question": "The Battle of Waterloo took place in which year?", "options": ["1805", "1815", " 1820", " 1835"],
                 "answer": "1815"},
                {"question": "Who wrote The Communist Manifesto \nalongside Karl Marx?", "options": ["Friedrich Engels", " Vladimir Lenin", "  Attack on Pearl Harbo", "  D-Day"],
                 "answer": "Friedrich Engels"},
                {"question": "What event marked the beginning of\nWorld War II in Europe?", "options": ["Invasion of Poland", " Battle of Britain", " John I", "Edward I"],
                 "answer": "Invasion of Poland"},
                {"question": "The Renaissance originated in which Italian city?", "options": [" Florence", "  Rome", "  Venice", "Milan"],
                 "answer": " Florence"},
                {"question": "Who was the first woman to win a Nobel Prize and\nremains the only person to win Nobel Prizes\nin two different scientific fields?", "options": ["Marie Curie", " Rosalind Franklin", " Jane Goodall", "Dorothy Crowfoot Hodgkin"],
                 "answer": "Marie Curie"},
                {"question": "The Boston Tea Party occurred in protest\nof which British taxation policy?", "options": [" Stamp Act", " Sugar Act", " Townshend Acts", "Tea Act"],
                 "answer": "Tea Act"},
                {"question": " In which year did Christopher Columbus\nfirst reach the Americas?", "options": ["1492", "  1500", " 1510", "1525"],
                 "answer": "1492"},
                {"question": "Who was the leader of the Soviet Union\nduring the Cuban Missile Crisis?", "options": ["Joseph Stalin", "  Nikita Khrushchev", " Leon Trotsky", " Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Opium Wars involved conflicts between\nChina and which European power?", "options": [" France", "   Britain", "Spain", "Portugal"],
                 "answer": "Britain"},
                {"question": " The Treaty of Versailles officially\nended which major conflict?", "options": [" World War I", " World War II", " Korean War", " Vietnam War"],
                 "answer": "World War I"},
                {"question": "Who was the primary author of the\nDeclaration of Independence?", "options": ["George Washington", " Thomas Jefferson", " John Adams", "Benjamin Franklin"],
                 "answer": "Thomas Jefferson"},
                {"question": "The Battle of Gettysburg was a significant\nengagement during which war?", "options": [" American Revolution", "Civil War", "  War of 1812", " Spanish-American War"],
                 "answer": "Civil War"},
                {"question": "The Industrial Revolution began\nin which country?", "options": [" France", " Germany", " Britain", " United States"],
                 "answer": " Britain"},
                {"question": "What is the historical period known\nfor the revival of art, literature, and\nlearning in Europe, lasting from the 14th\nto the 17th century?", "options": ["Middle Ages", " Renaissance", " Enlightenment", "Baroque Era"],
                 "answer": "Renaissance"},
                {"question":  "The Great Depression, a severe\nworldwide economic downturn, started\nin which decade?", "options": ["1910s", " 1920s", " 1930s", "1940s"],
                 "answer": " 1930s"},
                {"question": "Who was the Egyptian queen famous for\nher relationships with Julius Caesar\nand Mark Antony?", "options": ["Nefertiti", " Hatshepsut", "Cleopatra", " Ramses II"],
                 "answer": "Cleopatra"},
                {"question": "The Treaty of Ghent, signed in 1814,\nended which conflict between the\nUnited States and Britain?", "options": [" Revolutionary War", "  War of 1812", " Civil War", " French and Indian War"],
                 "answer": " War of 1812"},
                {"question": "Who was the founder of the Mongol\nEmpire in the 13th century?", "options": ["Genghis Khan", " Kublai Khan", " Attila the Hun", "Tamerlane"],
                 "answer": "Genghis Khan"},
                {"question": "What ancient wonder was a massive\ntomb built for an Indian emperor's wife in\nthe 17th century BCE?", "options": ["Great Pyramid of Giza", " Hanging Gardens of Babylon", "  Taj Mahal", "Mausoleum at Halicarnassus"],
                 "answer": "Taj Mahal"},
                {"question": "The Emancipation Proclamation, issued by\nPresident Abraham Lincoln during the American\nCivil War, declared the freedom of slaves\nin which region?", "options": [" Northern states", " Western states", " Southern states", "Eastern states"],
                 "answer": "Southern states"},
                {"question": "The Treaty of Tordesillas, signed in 1494,\ndivided newly discovered lands between\nwhich two European powers?", "options": ["Spain and Portugal", "France and England", "  England and Portugal", "Spain and France"],
                 "answer": " Spain and Portugal"},
                {"question": "The Battle of Stalingrad was a\nturning point in which conflict?", "options": ["World War I", "  Russian Revolution", " World War II", "Cold War"],
                 "answer": " World War I"},
                {"question": " What ancient civilization is known for\nbuilding the city of Troy?", "options": ["Greek", "  Roman", "  Persian", "Hittite"],
                 "answer": "Hittite"},
                {"question": "The Louisiana Purchase, a land deal\nin 1803, involved the United States purchasing\nterritory from which country?", "options": [" Spain", " France", " Britain", "Mexico"],
                 "answer": " France"},
                {"question": "Who was the leader of the Soviet\nUnion during the Cuban Missile Crisis?", "options": ["Joseph Stalin", " Nikita Khrushchev", " Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Boxer Rebellion, a violent anti-foreigner\nand anti-Christian uprising, took place\nin which country?", "options": [" China", " Japan", "India", " Korea"],
                 "answer": "China"},
                {"question": "What famous speech did Martin Luther King Jr.\ndeliver in 1963 during the March on\nWashington for Jobs and Freedom?", "options": ["I Have a Dream", " Give Me Liberty or Give Me Death", " The Gettysburg Address", "We Shall Overcome"],
                 "answer": "I Have a Dream"},
                {"question": " The Treaty of Paris (1763) ended\nwhich conflict between European powers?", "options": ["Napoleonic Wars", " Seven Years' War", "Franco-Prussian War", " Thirty Years' War"],
                 "answer": "Seven Years' War"},
                {"question": "Who was the first female Prime\nMinister of the United Kingdom?", "options": ["Angela Merkel", " Margaret Thatcher", " Theresa May", " Indira Gandhi"],
                 "answer": " Margaret Thatcher"},
                {"question": "What event marked the beginning of\nthe Protestant Reformation in the\nearly 16th century?", "options": ["Council of Trent", " Diet of Worms", " Peace of Augsburg", "Ninety-Five Theses"],
                 "answer": "Ninety-Five Theses"},
                {"question": " The Berlin Wall, which divided East\nand West Berlin during the Cold War,\nfell in which year?", "options": [" 1989", " 1991", " 1985", "1975"],
                 "answer": "1975"},
                {"question": "Who was the leader of the Bolshevik Party\nduring the Russian Revolution of 1917?", "options": ["Vladimir Lenin", "Joseph Stalin", "  Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": " Vladimir Lenin"},
                {"question": "The Treaty of Westphalia, signed in\n1648, ended which prolonged conflict in Europe?", "options": ["Hundred Years' War", " Thirty Years' War", " War of the Roses", "Wars of the Roses"],
                 "answer": "Thirty Years' War"},
                {"question": "The Battle of Saratoga, a pivotal engagement\nduring the American Revolution, occurred in which year?", "options": ["1763", "  1776", "1781", " 1777"],
                 "answer": " 1777"},
                {"question": " The Trail of Tears refers to the\nforced relocation of which Native American tribe\nin the 1830s?", "options": [ "Apache", " Cherokee", "Sioux", " Navajo"],
                 "answer": "Cherokee"},
                {"question": "Who was the primary author of 'The Prince',\na political treatise on leadership and governance?", "options": ["Niccolò Machiavelli", " Thomas More", " John Locke", "Voltaire"],
                 "answer": "Niccolò Machiavelli"},
                {"question": "The Battle of Midway, a decisive naval\nbattle in the Pacific during World War II,\ntook place in which year?", "options": ["1941", " 1942", " 1944", "1945"],
                 "answer": " 1942"},
                {"question": "Who was the first Emperor of China\nand the founder of the Qin Dynasty?", "options": ["Confucius", "  Sun Tzu", " Qin Shi Huang", "Han Wudi"],
                 "answer": " Qin Shi Huang"},
                {"question": "T The Ottoman Empire was centered\naround which city?", "options": [" Istanbul", " Cairo", " Baghdad", " Tehran"],
                 "answer": " Tehran"},
                {"question": "The Battle of Hastings in 1066 led to\nthe Norman conquest of which country?", "options": [" France", " England", " Scotland", " Ireland"],
                 "answer": "England"},
                {"question": "Who was the Roman general and statesman\nresponsible for the conquest of Gaul and\nlater became dictator for life?", "options": ["Julius Caesar", "Augustus Caesar", " Mark Antony", "Cicero"],
                 "answer": " Julius Caesar"},
                {"question": "The Indian independence movement, led by Mahatma\nGandhi, called for nonviolent resistance\nagainst which colonial power?", "options": ["France", " Britain", " Spain", "Portugal"],
                 "answer": " Britain"},
                {"question": "The Treaty of Nanking, signed in 1842,\nmarked the end of which conflict between\nChina and Britain?", "options": [" Opium Wars", " Boxer Rebellion", " Taiping Rebellion", " Sino-Japanese War"],
                 "answer": "Opium Wars"},
                {"question": "The Apollo 11 mission, in 1969,\nsuccessfully landed the first humans on\nwhich celestial body?", "options": ["Mars", "Venus", " Moon", "Jupiter"],
                 "answer": "Moon"},
                {"question": "The Monroe Doctrine, articulated in 1823,\nwarned against European intervention in the\naffairs of which region?", "options": ["Asia", " Africa", " Europe", "Americas"],
                 "answer": "Americas"},
                {"question": "Who was the leader of the Soviet Union during the Cuban Missile Crisis?", "options": [" Joseph Stalin", "  Nikita Khrushchev", " Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": " The Battle of Stalingrad was a turning\npoint in which conflict?", "options": ["World War I", "  Russian Revolution", " World War II", "Cold War"],
                 "answer": "World War II"},
                {"question": "What ancient civilization is known\nfor building the city of Troy?", "options": ["Greek", " Roman", " Persian", " Hittite"],
                 "answer": " Hittite"},
                {"question": "The Louisiana Purchase, a land deal in 1803,\ninvolved the United States purchasing territory\nfrom which country?", "options": ["Spain", " France", "  Britain", "Mexico"],
                 "answer": "France"},
                {"question": " Who was the leader of the Bolshevik Party\nduring the Russian Revolution of 1917?", "options": [" Vladimir Lenin", "  Joseph Stalin", " Leon Trotsky", " Mikhail Gorbachev"],
                 "answer": " Vladimir Lenin"},
                {"question": "Who was the first President of the\nUnited States?", "options": ["Thomas Jefferson", " George Washington", "John Adams", "James Madison"],
                 "answer": "George Washington"},
                {"question": "In which year did Christopher Columbus reach the Americas?", "options": [" 1492", "  1512", " 1607", " 1620"],
                 "answer": " 1492"},
                {"question": "The Battle of Gettysburg was a significant\nbattle during which war?", "options": ["World War I", " American Civil War", " Revolutionary War", "War of 1812"],
                 "answer": "American Civil War"},
                {"question": "Who was the first woman to win a Nobel Prize?", "options": [" Marie Curie", " Amelia Earhart", " Florence Nightingale", "Rosa Parks"],
                 "answer": "Marie Curie"},
                {"question": "What ancient wonder of the world was located in Egypt?", "options": ["Colossus of Rhodes", " Hanging Gardens of Babylon", " Great Pyramid of Giza", "Statue of Zeus at Olympia"],
                 "answer": "Great Pyramid of Giza"},
                {"question": "Who was the leader of the Soviet Union\nduring World War II?", "options": [" Vladimir Lenin", " Joseph Stalin", " Nikita Khrushchev", "Mikhail Gorbachev"],
                 "answer": "Joseph Stalin"},
                {"question": "The Magna Carta, signed in 1215, is considered\na cornerstone of which concept?", "options": ["Democracy", " Communism", " Feudalism", " Absolute monarchy"],
                 "answer":"Democracy"},
                {"question": " The Renaissance originated in\nwhich European city?", "options": [" Paris", " Rome", " Athens", " Florence"],
                 "answer": "Florence"},
                {"question": " What event marked the beginning of\nWorld War I?", "options": [" Assassination of Archduke Franz Ferdinand", " Invasion of Poland", "  Treaty of Versailles", "Battle of the Somme"],
                 "answer": " Assassination of Archduke Franz Ferdinand"},
                {"question": "Who wrote 'The Communist Manifesto' with Karl Marx?", "options": ["Friedrich Engels", "Vladimir Lenin", " Leon Trotsky", "Mao Zedong"],
                 "answer": "Friedrich Engels"},
                {"question": "Which ancient civilization built the city of Machu Picchu?", "options": [" Mayans", " Egyptians", "  Greeks", " Incas"],
                 "answer": " Incas"},
                {"question": "The Battle of Waterloo took place during which war?", "options": ["Napoleonic Wars", " American Civil War", "  World War I", " Hundred Years' War"],
                 "answer": "Napoleonic Wars"},
                {"question": "Who was the first Emperor of China,\nknown for the Terracotta Army?", "options": ["Qin Shi Huang", "Han Wudi", " Emperor Wu", "Confucius"],
                 "answer": "Qin Shi Huang"},
                {"question": "The Renaissance is often described as\nthe rebirth of what?", "options": ["Art and culture", "  Feudalism", " Monarchy", "Religious orthodoxy"],
                 "answer": "Art and culture"},
                {"question": "The Bubonic Plague, also known as the\nBlack Death, originated in which continent?", "options": ["Asia", " Africa", "  Europe", "North America"],
                 "answer": "Europe"},
                {"question": "Who was the primary author of the Declaration\nof Independence in the United States?", "options": [" Thomas Jefferson", " John Adams", "Benjamin Franklin", " George Washington"],
                 "answer": "Thomas Jefferson"},
                {"question": "The Treaty of Versailles marked the\nend of which conflict?", "options": ["World War I", "  World War II", " Korean War", "Vietnam War"],
                 "answer": "World War I"},
                {"question": "Which ancient civilization is known for creating\nthe first written language, cuneiform?", "options": ["Egyptians", " Sumerians", "  Greeks", "Romans"],
                 "answer": " Sumerians"},
                {"question": "The French Revolution began in which year?", "options": [" 1776", "  1789", " 1812", "1848"],
                 "answer": "1789"},
                {"question": "Who was the first woman to fly solo\nacross the Atlantic Ocean?", "options": [" Amelia Earhart", " Bessie Coleman", "  Harriet Quimby", " Jacqueline Cochran"],
                 "answer": " Amelia Earhart"},
                {"question": "The Great Wall of China was built to protect\nagainst invasions from which group?", "options": [" Mongols", " Huns", " Vikings", "Persians"],
                 "answer": " Mongols"},
                {"question": "The Industrial Revolution began in which country?", "options": ["England", " France", " Germany", "United States"],
                 "answer": "England"},
                {"question": "Who was the leader of the Soviet Union\nduring the Cuban Missile Crisis?", "options": ["Vladimir Putin", "Leon Trotsky", "Nikita Khrushchev", " Joseph Stalin"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Emancipation Proclamation, issued\nby Abraham Lincoln, aimed to free slaves\nduring which conflict?", "options": ["American Revolution", " American Civil War", "  War of 1812", "Spanish-American War"],
                 "answer": "American Civil War"},
                {"question": " What ancient city was home to the\nfamous Hanging Gardens?", "options": ["Rome", " Athens", "Babylon", "Alexandria"],
                 "answer": "Babylon"},
                {"question": "Who was the first woman to win a\nNobel Prize for Peace?", "options": ["Marie Curie", "Mother Teresa", "Aung San Suu Kyi", "Bertha von Suttner"],
                 "answer": "Bertha von Suttner"},
                {"question": "The Battle of Stalingrad was a major\nturning point in which conflict?", "options": ["World War I", " World War II", " Korean War", "Vietnam War"],
                 "answer": "World War II"},
                {"question": " The Marshall Plan was designed to aid\nthe economic recovery of which continent\nafter World War II?", "options": ["North America", " Europe", " Asia", "Africa"],
                 "answer": "Europe"},
                {"question": "Who was the longest-reigning monarch\nin British history?", "options": ["Queen Elizabeth II", " Queen Victoria", " King George III", "King Henry VII"],
                 "answer": " Queen Victoria"},
                {"question": "The Treaty of Brest-Litovsk marked the end\nof Russia's involvement in which conflict?", "options": ["World War I", "Russian Revolution", " Napoleonic Wars", "Crimean War"],
                 "answer": "World War I"},
                {"question": "The Berlin Wall was built to divide which\ncity during the Cold War?", "options": ["Paris", "Rome", "  Berlin", " Vienna"],
                 "answer": "Berlin"},
                {"question": "Who was the leader of the Mongol\nEmpire during its peak?", "options": ["Genghis Khan", "Kublai Khan", "  Attila the Hun", "Tamerlane"],
                 "answer": "Genghis Khan"},
                {"question": "The signing of the Magna Carta in 1215\nwas a significant event in the history\nof which country?", "options": [" France", "England", "Spain", "Italy"],
                 "answer": "England"},
                {"question": "The Treaty of Tordesillas, signed in 1494,\ndivided newly discovered lands between\nwhich two countries?", "options": ["Spain and Portugal", " England and France", " Italy and Germany", "Netherlands and Belgium"],
                 "answer": "Spain and Portugal"},
                {"question": "The Opium Wars were fought between\nChina and which European power?", "options": ["France", "Spain", " Portugal", "Britain"],
                 "answer": "Britain"},
                {"question": "Who was the first woman to serve as\nPrime Minister of the United Kingdom?", "options": ["Margaret Thatcher", "Theresa May", " Angela Merkel", " Indira Gandhi"],
                 "answer": " Indira Gandhi"},
                {"question": "The Russian Revolution of 1917 led to the\nestablishment of which government?", "options": ["Constitutional monarchy", "  Absolute monarchy", " Communist government", " Parliamentary democracy"],
                 "answer": " Communist government"},
                {"question": "The Battle of Saratoga, a crucial turning\npoint in the American Revolution, occurred\nin which year?", "options": ["1763", " 1776", "1781", " 1777"],
                 "answer": " 1777"},
                {"question": "Who was the first Emperor of Rome?", "options": [" Julius Caesar", " Augustus", "  Nero", "Caligula"],
                 "answer": "Augustus"},
                {"question": "The Boxer Rebellion took place in which\ncountry during the late 19th century?", "options": [" Japan", " China", "  India", " Korea"],
                 "answer": " China"},
                {"question": " The Treaty of Ghent, signed in 1814,\nended which conflict?", "options": ["American Revolution", " War of 1812", "  French Revolution", "Napoleonic Wars"],
                 "answer": "War of 1812"},
                {"question": "The Zimmermann Telegram, intercepted during\nWorld War I, revealed a secret alliance\nbetween Germany and which country?", "options": ["Russia", " Mexico", " Japan", " Italy"],
                 "answer": "Mexico"},
                {"question": "The Battle of Midway, a pivotal naval battle\nin World War II, involved which two countries?", "options": ["United States and Japan", " Germany and Soviet Union", "  Britain and Italy", "France and China"],
                 "answer": "United States and Japan"},
                {"question": " The Treaty of Nanking, signed in 1842,\nmarked the end of hostilities in which conflict?", "options": [" Opium Wars", "  Crimean War", " Franco-Prussian War", "Spanish-American War"],
                 "answer": "Opium Wars"},
                {"question": "Who was the last Pharaoh of Ancient Egypt?", "options": ["Cleopatra VII", " Ramses II", "  Tutankhamun", "Hatshepsut"],
                 "answer": "Cleopatra VII"},
                {"question": " The Treaty of Kanagawa, signed in 1854,\nopened trade relations between Japan and\nwhich country?", "options": ["China", " United States", "  Britain", "Russia"],
                 "answer": "United States"},
            ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Biology":
            self.topics = [
                {"question": "What is the primary function of the ribosomes in a cell?", "options": ["Energy production", "protein systhesis", "", "",],
                 "answer": "Protein systhesis"},
                {"question": "In which organelle does cellular respiration occur?", "options": ["nucleus", "chloroplast", "Mitochondrion", "endoplasmic reticulum"],
                 "answer": "Mitochondrion"},
                {"question": "what is the function of the enzyme amylase", "options": ["break down proteins", "break down lipids","break down carbohydrates", "synthesize DNA"],
                 "answer": "break down carbohydrates"},
                {"question": "Which gas is produced during photosysthesis", "options": ["oxygen", "carbon dioxide", "nitrogen", "hydrogen"],
                 "answer": "oxygen"},
                {"question": "what is the role of galgi apparatus in the cell?", "options": ["energy production", "protein synthesis", "pakaging and modifying proteins", "photosynthesis"],
                 "answer": "pakaging and modifying proteins"},
                {"question": "which of the following is a characteristric of eukaryotic cells?", "options": ["lack of nucleus", "circular DNA", "membrane bound organelles", "small size"],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the cell membrane?", "options": ["energy production", "support and structure", "regulation of substances entering and leaving the cell", "protein synthesis"],
                 "answer": "regulation of substances entering and leaving the cell"},
                {"question": "which of the following is a nitrogeus base in a DNA?", "options": ["adenine", "guanine", "thymine", "all of the above"],
                 "answer": "all of the above"},
                {"question": "what is the purpose of mitosis in cell division?", "options": ["production of gametes", "growth and repair of body cells", "membrane bound organelles", "endoplasmic reticulum"],
                 "answer": "growth and repair of body cells"},
                {"question": "what is the function of the chloroplast in plant cells?", "options": ["energy production", "protein synthesis", "photosynthesis", "lipid synthesis"],
                 "answer": "photosynthesis"},
                {"question": "which of the following is a type of white blood cell involved to immune response?", "options": ["eosonophil", "neutronphil", "basophil", "monacyte"],
                 "answer": "eosonophil"},
                {"question": "what is the main function of the pancreas in digestion?", "options": ["producing pile", "producing insulin and enzymes for digestion", "absorbing nutrients", "storing gyclogen"],
                 "answer": "producing insulin and enzymes for digestion"},
                {"question": "in humams, where does fertilazion typically occur?", "options": ["ovary", "uterus", "fallopian tube", "cervix"],
                 "answer": "fallopian tube"},
                {"question": "which of the following is a function of the nervous system?", "options": ["transporting oxygen", "regulating body temperature", "transmitting electric signals", "producing hormones"],
                 "answer": "transmitting electric signals"},
                {"question": "what is the purpose of the lymphatic system?", "options": ["pumping blood", "fighting infection and transportting fluids", "digesting foods", "producing antibioties"],
                 "answer": "fighting infection and transportting fluids"},
                {"question": "what is the role od RNA in protein synthesis?", "options": ["carries amino acids to the ribosomes", "provides energy for the process", "acts as a structural component of ribosomes", "carries genetic information to DNA to ribosomes"],
                 "answer": "carries genetic information to DNA to ribosomes"},
                {"question": "which of the following is a function of the skeletal system?", "options": ["producing hormones", "providing supports and protection", "digesting food", "regulating blood pressure"],
                 "answer": "providing support and protection"},
                {"question": "what is the name of the process by which cells specialize into different cell types?", "options": ["mitosis", "meiosis", "differentiation", "replication"],
                 "answer": "differentiation"},
                {"question": "what is the purpose of the enzymes DNA polymerase?", "options": ["transcription", "translation", "DNA replication", "protein synthesis"],
                 "answer": "DNA replication"},
                {"question":"what is the function of the ednoplasmic reticulum (ER) in a cell?", "options": ["synthesizing lipids", "modifying and packaging proteins", "producing atp", "staring genetic information"],
                 "answer": "modifying and packaging problems"},
                {"question":"which of the following is an example of a passive transport process in cell?", "options": ["facilatated diffusion", "active transport", "endocytosis", "exocytosis"],
                 "answer": "facilatated diffusion"},
                {"question": "wwhat is the role of thymuys gland in the immune system?", "options": ["producing insulin", "maturation of T lymphocytes (T cells)", "filtering blood", "producing antibodies"],
                 "answer": "maturation T lymphocates (T cells)"},
                {"question": "which of the following is a function of kidney?", "options": ["regulation of blood pressure", "production of red blood cells", "digestion of proteins", "storage of urines"],
                 "answer": "regulation of blood pressure"},
                {"question": "what is the purpose of krebs cycle in cellular respiration?", "options": ["production of ATP", "oxidation of glucose", "breakdown of pyruvate to generate energy", "synthesis of glucose"],
                 "answer": "breakdown of pyruvate to generate energy"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "what is the primary role of the hemoglobin in red blood cells?", "options": ["carrying oxygen", "fighting infections", "blood clotting", "breaking down toxins"],
                 "answer": "carrying oxygen"},
                {"question": "which of the following is a function of hormone insulin?", "options": ["stimulating glycogen", "increaasing blood sugar levels", "promoting glucose uptake by cells", "inhibating protein synthesis"],
                 "answer": "promoting glucose uptake by cell"},
                {"question": "what is the function of cillia and flagella in cells?", "options": ["protein synthesis", "movement", "energy production", "DNA replication"],
                 "answer": "DNA replication"},
                {"question": "which of the following is a nitregenous base in RNA but not in DNA?", "options": ["adenine", "guanine", "uracil", "thymine"],
                 "answer": "uracil"},
                {"question": "what is the  main function of the enzyme amylase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown carbohydrates"},
                {"question": "in which cellular organelle does photosynthesis occur in plant cells?", "options": ["nucleus", "chloroplast", "mitochondrion", "ednoplasmic reticulum"],
                 "answer": "chloroplast"},
                {"question": "which of the following is a function of the circulatory system?", "options": ["digestion of food", "transport of nutrients and oxygen", "synthesis of hormones", "excreation of waste products"],
                 "answer": "transport of nutrients and oxygen "},
                {"question": "what is the function of the hormone adrenaline in the human body?", "options": ["regulating blood sugar levels", "controlling metabolism", "initiating fight or flight response", "stimulating growth"],
                 "answer": "initiating fight or flight response"},
                {"question": "which of the following is a function pf the skelatal muscles?", "options": ["pumping blood", "providing structural", "contraction for movements", "producing hormones"],
                 "answer": "contraction of movements"},
                {"question": "what is the function of the hormone progerostone in the female reproductive system?", "options": ["stimulating the realese of eggs from the ovaries", "maintaining the uterine lining during pregnancy","regulating blood pressure", "initiatiing milk production"],
                 "answer": "maintinaning the uterine lining during pregnancy"},
                {"question": "which of the following is a function of the respiratory system?", "options": ["producing antibodies", "regulating body temperature", "exchange of oxygen and carbong dioxide", "synthezing glucose"],
                 "answer": "exchange of oxygen and carbon dioxide"},
                {"question": "what is the primary function of the lymph nodes in the immune system?", "options": ["production of antibodies", "filtration of lymph and trapping pathogens", "pumping blood", "digestion fats"],
                 "answer": "filtration of lymph and trapping pathogens"},
                {"question": "in which part of the digestive system does the majority of nutrient absorption take place?", "options": ["stomach", "small intestine", "large intestine", "esophagus"],
                 "answer": "small intestine"},
                {"question": "what is the function of the enzyme lipase?", "options": ["break down proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown lipids"},
                {"question": "what is the primary function of the enzyme pepsin in the stomach?", "options": ["production of pile", "absorption of nutrient", "storage of food", "synthesis of insulin"],
                 "answer": "production of pile"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the hormone insulin in the regulation of blood sugar levels?", "options": ["increase blood sugar levels", "breakdown glucose", "promote glucose uptake by cells", "stimulate the release of glucagon"],
                 "answer": "promote of glucose uptake by cells"},
                {"question": "which type of cell division is rensposible for growth and repair in multi cellular organisms?", "options": ["mitosis", "meitosis", "binary fission", "budding"],
                 "answer": "mitosis"},
                {"question": "in the proccess of transcription what is the role of RNA polymerase?", "options": ["synthesize mRNA from DNA", "synthesize tRNA from DNA", "synthesize DNA from RNA", "synthesize proteins"],
                 "answer": "synthesize mRNA from DNA"},
                {"question": "which of the following is a function of the smooth endoplasmic reticulum?", "options": ["protein synthesizes", "lipid synthesize and detoxification", "modifying and packaging proteins", "energy production"],
                 "answer": "lipid synthesize and detoxification"},
                {"question": "what is the purpose of the nitrogen cycle in ecosystems?", "options": ["carbon fixation", "nitrogen fixiation", "oxygen production", "ATP synthesize"],
                 "answer": "nitrogen fixiation"},
                {"question": "what is the role of the hormone melatonin?", "options": ["regulation of blood sugar levels", "sleep wake cycle and cardian ryhthm", "regulation of body temperature", "stimulating growth"],
                 "answer": "sleep wake cycle and cardian ryhthm"},
                {"question": "which of the following is an example os a symbiotic relationship where both organism benefit?", "options": ["parasitsm", "nutualism", "commensalism", "predation "],
                 "answer": "mutualism"},
                {"question": "in humans, what is the primary function of the epiglottis?", "options": ["taste sensation", "breathing", "speech production", "swalowing "],
                 "answer": "swallowing"},
                {"question": "which of the following is golgi apparatus?", "options": ["protein synthesize", "cellular respiration", "packaging", "photosynthesis"],
                 "answer": "packaging"},
                {"question": "what is the term for the process by which a cell engulfs large particles or other cells?", "options": ["pinocytosis", "phagocytosis", "exocytosis", "osmosis"],
                 "answer": "phagocytosis"},
                {"question": "which of the characteristics of a eukaryotic cell?", "options": ["lack of nucleus", "circullar DNA", "membrane bound organelles", "small size "],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the enzyme catalase in cells?", "options": ["breakdown carbo", "breakdown lipids", "breakdown hydrogen", "synthesize DNA"],
                 "answer": "breakdown hydrogen"},
                {"question": "which of the following is a greenhouse gas contributing gto climate change?", "options": ["oxygen", "nitrogen", "methane", "hydrogen "],
                 "answer": "methane"},
                {"question": "what is the main function of the cornea in the human eye?", "options": ["color vision", "focusing light onto the retina", "light perception", "controlling the amount"],
                 "answer": "focusing light onto the retina"},
                {"question": "in plant cells what structure is responsible for storing water nutrients and waste production?", "options": ["nucleus", "vacuole", "clhoroplast", "ribosome "],
                 "answer": "vacuole"},
                {"question": "wht is the process  by which a catterpillar tranforms into butterfly?", "options": ["metamhorposis", "fission", "budding", "fragmentation"],
                 "answer": "metamorphosis"},
                {"question": "what is the primary function of the cilliary bodybin the human eye?", "options": ["producing tears", "changing the shape", "detecting light", "converting light"],
                 "answer": "changing the shape"},
                {"question": "which of the following is a nitrogen fixing bacterium commmonly \nfound in the root nodules of legumiunsvplants?", "options": ["escherichia coli", "rhzobium", "streptococcus", "bacillus subtilis"],
                 "answer": "rhizobium"},
                {"question": "what is the primary function of the hormones prolactin in females?", "options": ["stimulating milk", "regulating blood sugar", "intiating fight", "controlling metabolism "],
                 "answer": "stimulating milk"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "what is the primary role of the hemoglobin in red blood cells?", "options": ["carrying oxygen", "fighting infections", "blood clotting", "breaking down toxins"],
                 "answer": "carrying oxygen"},
                {"question": "which of the following is a function of hormone insulin?", "options": ["stimulating glycogen", "increaasing blood sugar levels", "promoting glucose uptake by cells", "inhibating protein synthesis"],
                 "answer": "promoting glucose uptake by cell"},
                {"question": "what is the function of cillia and flagella in cells?", "options": ["protein synthesis", "movement", "energy production", "DNA replication"],
                 "answer": "DNA replication"},
                {"question": "which of the following is a nitregenous base in RNA but not in DNA?", "options": ["adenine", "guanine", "uracil", "thymine"],
                 "answer": "uracil"},
                {"question": "what is the  main function of the enzyme amylase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown carbohydrates"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the hormone insulin in the regulation of blood sugar levels?", "options": ["increase blood sugar levels", "breakdown glucose", "promote glucose uptake by cells", "stimulate the release of glucagon"],
                 "answer": "promote of glucose uptake by cells"},
                {"question": "which type of cell division is rensposible for growth and repair in multi cellular organisms?", "options": ["mitosis", "meitosis", "binary fission", "budding"],
                 "answer": "mitosis"},
                {"question": "in which part of the digestive system does the majority of nutrient absorption take place?", "options": ["stomach", "small intestine", "large intestine", "esophagus"],
                 "answer": "small intestine"},
                {"question": "what is the function of the enzyme lipase?", "options": ["break down proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown lipids"},
                {"question": "what is the primary function of the enzyme pepsin in the stomach?", "options": ["production of pile", "absorption of nutrient", "storage of food", "synthesis of insulin"],
                 "answer": "production of pile"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the enzyme amylase", "options": ["break down proteins", "break down lipids","break down carbohydrates", "synthesize DNA"],
                 "answer": "break down carbohydrates"},
                {"question": "Which gas is produced during photosysthesis", "options": ["oxygen", "carbon dioxide", "nitrogen", "hydrogen"],
                 "answer": "oxygen"},
                {"question": "what is the role of galgi apparatus in the cell?", "options": ["energy production", "protein synthesis", "pakaging and modifying proteins", "photosynthesis"],
                 "answer": "pakaging and modifying proteins"},
                {"question": "which of the following is a characteristric of eukaryotic cells?", "options": ["lack of nucleus", "circular DNA", "membrane bound organelles", "small size"],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the cell membrane?", "options": ["energy production", "support and structure", "regulation of substances entering and leaving the cell", "protein synthesis"],
                 "answer": "regulation of substances entering and leaving the cell"},
                {"question": "which of the following is a nitrogeus base in a DNA?", "options": ["adenine", "guanine", "thymine", "all of the above"],
                 "answer": "all of the above"},
                {"question": "what is the name of the process by which cells specialize into different cell types?", "options": ["mitosis", "meiosis", "differentiation", "replication"],
                 "answer": "differentiation"},
                {"question": "what is the purpose of the enzymes DNA polymerase?", "options": ["transcription", "translation", "DNA replication", "protein synthesis"],
                 "answer": "DNA replication"},
                {"question":"what is the function of the ednoplasmic reticulum (ER) in a cell?", "options": ["synthesizing lipids", "modifying and packaging proteins", "producing atp", "staring genetic information"],
                 "answer": "modifying and packaging problems"},
                {"question":"which of the following is an example of a passive transport process in cell?", "options": ["facilatated diffusion", "active transport", "endocytosis", "exocytosis"],
                 "answer": "facilatated diffusion"},
                {"question": "wwhat is the role of thymuys gland in the immune system?", "options": ["producing insulin", "maturation of T lymphocytes (T cells)", "filtering blood", "producing antibodies"],
                 "answer": "maturation T lymphocates (T cells)"},
                {"question": "which of the following is a function of kidney?", "options": ["regulation of blood pressure", "production of red blood cells", "digestion of proteins", "storage of urines"],
                 "answer": "regulation of blood pressure"},
                {"question": "what is the purpose of krebs cycle in cellular respiration?", "options": ["production of ATP", "oxidation of glucose", "breakdown of pyruvate to generate energy", "synthesis of glucose"],
                 "answer": "breakdown of pyruvate to generate energy"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "in humans where does spermatogenesis occur?", "options": ["ovary", "testes", "uterus", "fallopian tube"],
                 "answer": "testes"},
                {"question": "what is the primary function of the enzyme sucrase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown sucrose", "synthesize DNA"],
                 "answer": "breakdown sucrose"},
                {"question": "in genetics, what is the term for the physical expression of an organism genetic traits?", "options": ["genotype", "phenotype", "allele", "homozygote"],
                 "answer": "phenotype"},
                {"question": "in which part of the human digestive system dooes nutrient absorpotion primarily occur?", "options": ["stomach", "large intestine", "small intestine", "mouth"],
                 "answer": "small intestine"},
                {"question": "which of the following is an example of an exocrine gland in the human boyd?", "options": ["thyroid gland", "pituiry gland", "salivvary gland", "adrenal gland"],
                 "answer": "salivary gland"},
                {"question": "in the context of plant reproduction what is the male reproductive organ called?", "options": ["ovule", "pistl", "stamen", "carpel"],
                 "answer": "stamen"},
                {"question": "in the context of ecology what is the term for the study of the interactions among organism and their envinronment?", "options": ["genetics", "physiology", "ecology", "ethology"],
                 "answer": "ecology"},
                {"question": "which of the following is a nitrogen fixing bacterium commonly \nfound in the root nodules of leguminous plants?", "options": ["escherichia coli", "rhizobium", "streptococcus", "bacillis"],
                 "answer": "rhizobium"},
                {"question": "in humans what is the mai function of the kidneys?", "options": ["digestion", "filtration of blood", "respiration", "pumping blood"],
                 "answer": "filtration of blood "},
                {"question": " what is the molecule that carries genetic information for the development and functioning of an organism.?", "options": ["DNA", "RNA", "RMA", "RTA"],
                 "answer":"DNA"},
            ]
            random.shuffle(self.topics)
                    
        elif self.subject_var.get() == "TEST HERE":
            self.topics = [
                {
                    "question": "What is the result of 7 x 9?",
                    "options": ["54", "63", "72","48"],
                    "answer": "63"
                },
                {
                    "question": "If a rectangle has a length of 10 units\nand a width of 5 units, what is its area?",
                    "options": ["20 square units", "30 square units", "40 square units","50 square units"],
                    "answer": "40 square units"
                },
                {
                    "question": "What is the result of (12 ÷ 4) + 5?",
                    "options": ["  7  ", "  8  ", "  9  ","  10  "],
                    "answer": "  8  "
                },
                {
                    "question": "Ano ang iyong paboritong kulay?",
                    "options": ["pula", "asul", "  9  ","  10  "],
                    "answer": "pula"
                },
                {
                    "question": "Ano ang iyong paboritong planeta sa solar system??",
                    "options": ["Pluto", "Mars", "Neptune","Pizza"],
                    "answer": "Pizza"
                },
            ]
            random.shuffle(self.topics)
        # questions frame
        quiz1_frame = tk.Frame(self.root, bg="#2A225A") # violet 
        quiz1_frame.pack()
        self.currentFrame = quiz1_frame
        
        # Score label
        self.score_label = tk.Label(quiz1_frame,
                                    text=f"Score: {self.score}",
                                    bg="black",  # background color for the score label
                                    fg="#4FDD0C",
                                    padx=20,
                                    font=("Comic sans MS", 20, "bold"))
        self.score_label.pack(side=tk.TOP,pady=10,padx=(40))

        # Lives label
        self.lives_label = tk.Label(quiz1_frame,
                                    padx=20,
                                    text=f"Lives: {self.lives}",
                                    bg="black",  # background color for the lives label
                                    fg="#07B9AE",
                                    font=("Comic sans MS", 20, "bold"))
        self.lives_label.pack(side=tk.TOP,padx=(40))

        # Question label
        self.question_label = tk.Label(quiz1_frame,
                                       text=self.topics[self.currentQuestionIndex]["question"],
                                       bg="#2A225A", # violet 
                                       fg="white",                                      
                                       font=("Comic sans MS", 20, "bold"))
        self.question_label.pack(pady=40)

        self.player_answer.set("") # nag rereset ng napiling sagot bagu mag next questions
        
        # Arrange choices in two columns
        num_choices = len(self.topics[self.currentQuestionIndex]["options"])
        num_columns = 2
        num_rows = (num_choices + num_columns - 1) // num_columns
        
        rbs=[]  #list of radiobutton choices
         
        # choices frame color  
        choices_frame = tk.Frame(quiz1_frame,bg="#2A225A")
        choices_frame.pack()
         
        # function na nag chechange ng kulay pag nag select ng answer 
        def select(choice_button):
            choice_button.config(foreground='yellow')
            for choice_button_ in rbs:
                if choice_button_ != choice_button:
                   choice_button_.config(fg='#F66868') # this will be the color ng ibang choices pag hindi napili
                   
        # ito ay function para ma arrange ang pagpipiliang sagot sa 2 rows and 2 column
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < num_choices:
                    
                    # function ng choices dito pede ibahin kulay ng text background
                    choice_text = self.topics[self.currentQuestionIndex]["options"][index]
                    choice_button = tk.Radiobutton(choices_frame,
                                                   text=choice_text,
                                                   variable=self.player_answer,
                                                   value=choice_text,                                                
                                                   background="#2A225A",
                                                   foreground="orange", # color of texts choices
                                                   activebackground="green",                                                                                              
                                                   cursor='hand2',
                                                   font=("Comic sans MS", 20, "bold"))
                    choice_button.config(command=lambda arg=choice_button:select(arg))
                    choice_button.grid(row=i, column=j, padx=10, pady=20, sticky="w")
                    rbs.append(choice_button) # adding choice button

        button_frame = tk.Frame(quiz1_frame, bg="#2A225A")
        button_frame.pack(pady=20)
        
        self.submit_button = tk.Button(button_frame, text=" Submit ",
                                     command=self.submit_button_sound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#990066",
                                     foreground="white",
                                     activebackground="#FF0066",
                                     activeforeground="white",
                                     font=("Comic sans MS",25, "bold"))
        self.submit_button.pack(side=tk.LEFT, padx=25,pady=15)
        
        self.save_button = tk.Button(button_frame, text="  Save  ",
                                     command=self.save_button_sound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#009900",
                                     foreground="white",
                                     activebackground="#00FF00",
                                     activeforeground="white",
                                     font=("Comic sans MS",25, "bold"))                                    
        self.save_button.pack(side=tk.LEFT, padx=25,pady=15)
        
        self.back_button = tk.Button(button_frame,
                                     text=" Give Up ",
                                     command=self.gameover2_withsound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#000066",
                                     foreground="white",
                                     activebackground="#0033CC",
                                     activeforeground="white",
                                     font=("Comic sans MS", 25, "bold"))
        self.back_button.pack(side=tk.LEFT, padx=25,pady=15)
        # new progress button sounds
    def submit_button_sound(self):
        self.button_music.play()
        self.check_answer()
        
    def save_button_sound(self):
        self.button_music.play()
        self.saved_progress() 
        
    def gameover2_withsound(self):
        self.button_music.play()
        self.give_up()
         
     # GENERATING QUIZ FRAME FOR "LOAD PROGRESS"
    def generate_quiz_frame2(self):
       
        if self.topic == "Universe":
            self.topics = [
                {"question": "Approximately, what is the age of the universe?", "options": ["365 Days", "366 Days", "23.9 Billion Years", "13.8 Billion Years"],
                 "answer": "13.8 Billion Years"},
                {"question": "What is the famous theory of creation of the universe?", "options": ["Information Theory", "Game Theory", "Big Bang Theory", "Quantum Theory"],
                 "answer": "Big Bang Theory"},
                {"question": "What is this mysterious component of the universe\ncalled?", "options": ["Dark Energy", "Dark Star", "Dark Matter", "Black Hole"],
                 "answer": "Dark Energy"},
                {"question": "A space wherein the gravity’s so strong not even light can\nescape.", "options": ["Butt Hole", "Black Hole", "Black Jack", "Black Butt"],
                 "answer": "Black Hole"},
                {"question": "What is the estimated count of galaxies in the observable universe?", "options": ["100 to 200 Galaxies", "10 to 20 Galaxies", "100 to 200 Billion Galaxies", "Eight Galaxies"],
                 "answer": "100 to 200 Billion Galaxies"},
                {"question": "What is the prevailing cosmological model that explains the\norigin and evolution of the observable universe?", "options": ["Big Bang Theory", "Information Theory", "Quantum Theory", "God's Creation Theory"],
                 "answer": "Big Bang Theory"},
                {"question": "What is the form of matter that is invisible and undetectable\nthrough electromagnetic radiation?", "options": ["Dark Energy", "Dark Star", "Dark Matter", "Black Hole"],
                 "answer": "Dark Matter"},
                {"question": "This concept proposes a rapid and exponential expansion of the\nearly universe during the first moments after the Big Bang.", "options": ["Cosmic Inflation", "Continental Drift Theory", "Game Theory", "Information Theory"],
                 "answer": "Cosmic Inflation"},
                {"question": "Formed through the gravitational collapse of massive objects,\ntypically the remnants of massive stars.", "options": ["Meteorite", "Meteor", "Black Hole", "Star"],
                 "answer": "Black Hole"},
                {"question": "This is a formation of rock debris flying freely in the universe?", "options": ["Meteorite", "Meteor", "Asteroid", "Asteroid Belt"],
                 "answer": "Asteroid"},
                {"question": "What’s the three possible shape of the universe?", "options": ["Oblique,Sphere,Trapezoid", "Flat,Open,Close", "Rectangle,Triangle,Sphere,", "Flat,Sphere,Oblique"],
                 "answer": "Flat,Open,Close"},
                {"question": "What do you call the processes of star formation, stellar death\nand feedback, influencing their appearance and characteristics?", "options": ["Galactic Evolution", "Galactic Rebirth", "Galactic Revolution", "Galaxy Overhaul"],
                 "answer": "Galactic Evolution"},
                {"question": "This matter is incredibly dense and compact stellar remnants\nthat form when massive stars undergo a supernova explosion.", "options": ["Neuron Stars", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Fascinating objects that push the limits of our\nunderstanding of matter and gravity.", "options": ["Neuron Stars", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Possess extremely strong magnetic fields, often trillions\nof times stronger than Earth's magnetic field.", "options": ["Neuron Star", "Neutron Star", "Sun", "Asteroids"],
                 "answer": "Neutron Star"},
                {"question": "Hypothetical tunnel-like structure that connects\ntwo separate points in space-time.", "options": ["Wormhole", "Funnel", "Asshole", "Black Hole"],
                 "answer": "Wormhole"},
                {"question": "It consists of two ends, often referred to as mouths or throats.\nEach mouth is a separate entrance or exit point in space time.", "options": ["Wormhole", "Funnel", "Asshole", "Black Hole"],
                 "answer": "Wormhole"},
                {"question": "The simplest type of wormhole, known as a _, is a hypothetical\nsolution to the equations of general relativity.", "options": ["Wormhole", "White Hole", "Black Hole", "Einstein-Rosen Bridge"],
                 "answer": "Einstein-Rosen Bridge"},
                {"question": "Responsible for the formation of celestial bodies, such as\nstars, planets, galaxies, and galaxy clusters.", "options": ["Gravity", "Stars", "Meteor", "Meteorites"],
                 "answer": "Gravity"},
                {"question": "Gravity governs the ___ of celestial bodies in the universe.", "options": ["Orbital Motion", "Revolution", "Gravitational Pull", "Meteorites"],
                 "answer": "Orbital Motion"},
                {"question": "It is the primary force shaping the dynamics of galaxies.", "options": ["Gravity", "Force", "UV rays", "Meteorite"],
                 "answer": "Gravity"},
                {"question": ". __ is a fundamental force that governs the behavior of matter,\nfrom the smallest particles to largest structures.", "options": ["Gravity", "Force", "UV rays", "Meteorite"],
                 "answer": "Gravity"},
                {"question": "These planets are not located within the Sun's family of planets\nbut instead orbit stars that may be light-years away from Earth.", "options": ["Wormhole", "Exoplanets", "Neuroplanets", "Dwarf Planets"],
                 "answer": "Exoplanets"},
                {"question": "Also known as Goldilocks Zone", "options": ["Restricted Zone", "Habitable Zone", "Danger Zone", "Deadly Zone"],
                 "answer": "Habitable Zone"},
                {"question": "What is the three detection method?", "options": ["Transit, Direct Imaging, Radar", "Transit, Radial Velocity,\nDirect imaging", "Tracking, Recording, Surveillance", "Transmit, Monitor, Radar"],
                 "answer": "Transit, Radial Velocity,\nDirect imaging"},
                {"question": "This equation is a probabilistic formula that was developed\nby the American astrophysicist Dr. Frank Drake in 1961.", "options": ["Probability & Statistics", "Mathematical Equation", "Drake Equation", "Pythagorean Theorem"],
                 "answer": "Drake Equation"},
                {"question": "__is a large-scale structure of the universe, composed of\ninterconnected filaments of dark matter and gas.", "options": ["Star", "Cosmic Web", "Black Hole", "Worm Hole"],
                 "answer": "Cosmic Web"},
                {"question": "What is the three elements of cosmic web?", "options": ["Filaments, Nodes, Voids", "Gas, Dark Energy, Dark Matter", "Filaments, Voids, Dark Energy", "Nodes, Dark Energy, Dark Matter"],
                 "answer": "Filaments, Nodes, Voids"},
                {"question": "The __ of the cosmic web is primarily composed of\ndark matter,a mysterious form of matter that does not interact with light.", "options": ["Backbone", "Heart", "Brain", "Center"],
                 "answer": "Backbone"},
                {"question": "__ thought to trace the underlying distribution of dark matter.", "options": ["Backbone", "Cosmic Web", "Dark Energy", "Ordinary Matter"],
                 "answer": "Ordinary Matter"},
                {"question": ". __ is a scientific concept that addresses the universe's\nphysical constants and conditions allow for the existence of \nlife.", "options": ["Genetics", "Properties of Matter", "Big Bang Theory", "Anthropic Principle"],
                 "answer": "Anthropic Principle"},
                {"question": "What is the two (2) types of anthropic Principle?", "options": ["SAP & WAP", "SAP & PWD", "WAP & DSWD", "AAP & SAP"],
                 "answer": "SAP & WAP"},
                {"question": "__ is a highly magnetized, rotating neutron star that emits\nbeams of electromagnetic radiation along its magnetic poles.", "options": ["Void", "Pulsar", "Pulse", "Electron"],
                 "answer": "Pulsar"},
                {"question": "Composed primarily of neutrons, with incredibly high densities.", "options": ["Void", "Pulsar", "Pulse", "Electron"],
                 "answer": "Pulsar"},
                {"question": "Have extremely strong magnetic fields, typically trillions\nof times stronger than Earth's magnetic field.", "options": ["Neutron Star", "Pulsar", "Moon", "Sun"],
                 "answer": "Pulsar"},
                {"question": "Three types of radiation Pulsar produce.", "options": ["Gamma ray, X-ray, Radio Waves", "Gamma ray,Pulse,UV ray", "X-ray,Pulse,Radio waves", "Sun Ray,UV ray,Micro Waves"],
                 "answer": "Gamma ray, X-ray, Radio Waves"},
                {"question": "Hypothetical one-dimensional topological defects in the\nfabric of space time.", "options": ["Common String", "Cosmic Strings", "Coil Spring", "Pulse String"],
                 "answer": "Cosmic Strings"},
                {"question": "Topological defects because their existence is not dependent on\nspecific physical properties or the material they are made of.", "options": ["Common String", "Cosmic Strings", "Coil Spring", "Pulse String"],
                 "answer": "Cosmic Strings"},
                {"question": ". __ expected to generate gravitational effects.", "options": ["Gravity", "Cosmic Strings", "Sun", "Pulsar"],
                 "answer": "Cosmic Strings"},
                {"question": "Considered as a possible mechanism for seeding the formation of\nlarge-scale structures such as galaxies and galaxy clusters.", "options": ["Duplicating", "Cosmic Strings", "Replicating", "Reproduction"],
                 "answer": "Cosmic Strings"},
                {"question": "What are the two types of supernova?", "options": ["Type C&Prototype", "Type C&B", "Type 1&2", "Type II & la"],
                 "answer": "Type II & la"},
                {"question": "Responsible for synthesizing and dispersing heavy elements,\nsuch as iron and gold, into space.", "options": ["Planet Collision", "Star Explosion", "Meteor Collision", "Supernova"],
                 "answer": "Supernova"},
                {"question": "Consists of particles with the same mass as\nordinary matter particles but with opposite charge.", "options": ["Core", "Anti-Matter", "Dark Matter", "Sun"],
                 "answer": "Anti-Matter"},
                {"question": "Hypothetical substance that combines dark matter and\ndark energy into a unified framework.", "options": ["Dark Energy", "Dark Matter", "Dark Fluid", "Dark Liquid"],
                 "answer": "Dark Fluid"},
                {"question": "Late-stage star that has exhausted its core hydrogen,\nexpanded, and cooled.", "options": ["Dwarf Planet", "Dead Star", "Dark Fluid", "Red-Giant"],
                 "answer": "Red-Giant"},
                {"question": "Region of the solar system beyond Neptune that\ncontains many small, icy bodies.", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "It is similar to the asteroid belt, which is located\nbetween Mars and Jupiter, but much larger and \nfarther from the Sun.", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "Named after Dutch-American astronomer Gerard Kuiper, who\nfirst proposed the existence of such a region in the\n1950s?", "options": ["Orbit", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Kuiper Belt"},
                {"question": "Hypothetical region in the outermost reaches of the\nsolar system, believed to contain icy bodies and comets.", "options": ["Oort Cloud", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Oort Cloud"},
                {"question": "Named after the Dutch astronomer Jan Oort, who\nproposed its existence in 1950?", "options": ["Oort Cloud", "Asteroid Belt", "Orion Belt", "Kuiper Belt"],
                 "answer": "Oort Cloud"},
                {"question": "The remnant core of a star that has exhausted\nits nuclear fuel.", "options": ["Oort Cloud", "Asteroid Belt", "White Dwarf", "Red-Giant"],
                 "answer": "White Dwarf"},
                {"question": "Characterized by their small size, high density, and relatively low\nluminosity compared to their earlier stages as main-sequence\nstars.", "options": ["Oort Cloud", "Asteroid Belt", "White Dwarf", "Red-Giant"],
                 "answer": "White Dwarf"},
                {"question": "Extremely luminous and energetic active galactic nucleus,\npowered by a supermassive black hole.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Can exhibit rapid and extreme variability in their brightness\nover short timescales, ranging from days to months.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Appear as point sources, they are\nassociated with host galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "This astronomical object helps\nscientists study the early universe.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Study of active galactic nuclei and the understanding of\nthe energetic processes occurring in the centers of galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Among the most luminous objects in the universe,\noutshining entire galaxies.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "First identified as unusual point sources of\nradio waves in the 1960s.", "options": ["Pulsar", "Core", "Quasar", "Red-Giant"],
                 "answer": "Quasar"},
                {"question": "Measure of the rate at\nwhich the universe is expanding.", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "Named after the American astronomer Edwin Hubble, understanding\nof the expansion of the universe.", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "Expressed in units of kilometers per second\nper megaparsec (km/s/Mpc).", "options": ["Area", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "States that the velocity at which a galaxy\nis moving away from an observer is directly\nproportional to its distance.", "options": ["Boyle's Law", "Hubble's Law", "Charles's Law", "Law of Attraction"],
                 "answer": "Hubble's Law"},
                {"question": "Denoted by the symbol (H₀).", "options": ["Velocity", "Hubble Constant", "Perimeter", "Ratio"],
                 "answer": "Hubble Constant"},
                {"question": "According to quantum mechanics, it's a phenomenon\nknown as vacuum fluctuations.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Inversely proportional to the mass of the\nblack hole. Smaller black holes emit more intense\nradiation than larger ones.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Not been directly observed because the effect is\nextremely weak for astrophysical black holes.", "options": ["Velocity", "Hubble Constant", "Hawking Radiation", "Black Hole"],
                 "answer": "Hawking Radiation"},
                {"question": "Occurs when the Moon passes between the Earth\nand the Sun, blocking part or all of\nthe Sun's light.", "options": ["Supernova", "Meteor Shower", "Lunar Eclipse", "Solar Eclipse"],
                 "answer": "Solar Eclipse"},
                {"question": "Can happen only when the Sun, Moon, and\nEarth are aligned in a straight line, with\nthe Moon casting a shadow on Earth.", "options": ["Supernova", "Meteor Shower", "Lunar Eclipse", "Solar Eclipse"],
                 "answer": "Solar Eclipse"},
                {"question": "The Moon completely covers the Sun from the\nviewpoint of observers on Earth.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Total Solar Eclipse"},
                {"question": "Only a portion of the Sun is covered\nby the Moon, and the Sun appears as\na crescent.", "options": ["Partial Solar Eclipse", "Annual Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Partial Solar Eclipse"},
                {"question": "Occurs when the Moon is too far from\nEarth to completely cover the Sun.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Annular Solar Eclipse"},
                {"question": "The Sun's outer atmosphere, called the solar\ncorona, becomes visible during totality.", "options": ["Partial Solar Eclipse", "Annular Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Total Solar Eclipse"},
                {"question": "The extent of coverage depends on the\nobserver's location within the eclipse's path.", "options": ["Partial Solar Eclipse", "Annual Solar Eclipse", "Total Lunar Eclipse", "Total Solar Eclipse"],
                 "answer": "Partial Solar Eclipse"},
                {"question": "These bursts are the most energetic events in\nthe universe, emitting more energy in a few\nseconds.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Gamma Ray Burst"},
                {"question": "Stellar explosion that is more energetic and powerful\nthan a supernova. It represents the extreme life cycle\nof massive stars.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Hypernova"},
                {"question": "Stellar explosion that results from the merger\nof two stars in a binary system.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Luminous Red Nova"},
                {"question": "Temporary increase in the brightness of a star,\ntypically by a factor of several thousand.", "options": ["Nova", "Supernova", "Hypernova", "Luminouse Red Nova"],
                 "answer": "Nova"},
                {"question": "It is a minor type of stellar explosion.", "options": ["Gamma Ray Burst", "Supernova", "Hypernova", "Solar Flares"],
                 "answer": "Solar Flares"},
                {"question": "What is the unit used to indicate the\ndistance of the galaxy in the universe?", "options": ["Light Year", "Parsec", "Miles", "Kilometers"],
                 "answer": "Parsec"},
                {"question": "Used to describe a hypothetical space that exists\nbeyond the three spatial dimensions we are familiar\nwith.", "options": ["Light Year", "Parsec", "Hyperspace", "Kilometers"],
                 "answer": "Hyperspace"},
                {"question": "Speculative concept that arises in various scientific and\nphilosophical discussions,and it suggests the existence of multiple, possibly\ninfinite, universes or realities.", "options": ["Universe", "Multiverse", "Parallel Universe", "Alternate Reality"],
                 "answer": "Multiverse"},
                {"question": "Theoretical framework in physics that attempts to describe\nthe building blocks of the universe as one-\ndimensional, suggests the possibility of multiple compactified dimensions.", "options": ["Universe", "Multiverse", "String Theory", "Alternate Reality"],
                 "answer": "String Theory"},
                {"question": "Typically refers to a hypothetical or fictional version\nof reality that differs from the one we\nexperience in our everyday lives.", "options": ["Universe", "Multiverse", "String Theory", "Alternate Reality"],
                 "answer": "Alternate Reality"},
                {"question": "Also known as an alternate universe or a\nparallel dimension.", "options": ["Universe", "Multiverse", "String Theory", "Parallel Universe"],
                 "answer": "Parallel Universe"},
                {"question": "This wave ripples in the fabric of spacetime\ncaused by the acceleration of massive objects.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "__ waves are a form of radiation, similar\nto electromagnetic waves, but with distinct properties.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "__ waves are produced by accelerating masses,\nespecially those involved in violent astrophysical events.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "Travel at the speed of light and can\npass through matter without being significantly affected.", "options": ["Sound Wave", "Gravitational Wave", "Micro Wave", "Tidal Wave"],
                 "answer": "Gravitational Wave"},
                {"question": "This one main formulation takes a more metaphysical stance\nand suggests that the universe must have properties\nthat allow for the existence of observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Strong Anthropic Principle"},
                {"question": "This main formulation is the more modest form\nand states that the properties of the universe\nmust be consistent with the existence of observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Weak Anthropic Principle"},
                {"question": "The __ is often used to explain why\ncertain physical constants and conditions appear finely tuned\nfor the existence of life.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Weak Anthropic Principle"},
                {"question": "Some proponents of the __ go further, suggesting\nthat the universe is, in some sense, compelled\nto bring forth conscious observers.", "options": ["Mild Anthropic Principle", "Moderate Anthropic Principle", "Strong Anthropic Principle", "Weak Anthropic Principle"],
                 "answer": "Strong Anthropic Principle"},
                {"question": "He is a Soviet cosmonaut, was the first\nhuman to journey into outer space.", "options": ["Yuri Gagarin", "Albert Einstein", "Charles Darwin", "Robert Boyle"],
                 "answer": "Yuri Gagarin"},
                {"question": "His mission lasted approximately 108 minutes, during which\nhe experienced weightlessness and observed Earth from orbit.", "options": ["Yuri Gagarin", "Albert Einstein", "Charles Darwin", "Robert Boyle"],
                 "answer": "Yuri Gagarin"},
                {"question": "__ is a massive, gravitationally bound system consisting\nof stars, stellar remnants, interstellar gas, dust, and\ndark matter.", "options": ["Star", "Sun", "Universe", "Galaxy"],
                 "answer": "Galaxy"},
                {"question": "Come in various shapes and sizes and can\ncontain millions to trillions of stars.", "options": ["Star", "Sun", "Universe", "Galaxy"],
                 "answer": "Galaxy"},
                {"question": "This galaxy shape have a more spheroidal or\nellipsoidal shape and lack well-defined spiral arms.", "options": ["Sphere Galaxy", "Flat Galaxy", "Lunar Galaxy", "Elliptical Galaxy"],
                 "answer": "Elliptical Galaxy"},
                {"question": "Who is the first person to\nset foot on the Moon?", "options": ["Neil Armstrong", "Isaac Newton", "Charles Darwin", "Albert Einstein"],
                 "answer": "Neil Armstrong"}
            ]
            random.shuffle(self.topics)
            
        if self.subject_var.get() == "Tricky":
            self.topics = [
                {"question": " What is the capital of Canada?", "options": ["Ottawa", "Toronto", "Vancouver", "Montreal"],
                 "answer": "Montreal"},
                
                {"question": "Who is the author of 'To Kill a Mockingbird'?", "options": ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "F. Scott Fitzgerald"],
                 "answer": "Harper Lee"},
                
                {"question": "How many continents are there on Earth?", "options": ["5", "6", "7", "8"],
                 "answer": "6"},
                
                {"question": "Which planet is known as the 'Red Planet'?", "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                 "answer": "Mars"},
                
                {"question": "What is the square root of 144?", "options": ["12", "10", "14", "16"],
                 "answer": "12"},
                
                {"question": "In what year did World War I begin?", "options": ["1914", "1916", "1918", "1920"],
                 "answer": "1914"},
                
                {"question": "Who painted the Mona Lisa?", "options": ["Michelangelo", "Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"],
                 "answer": "Leonardo da Vinci"},
                
                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},
                
                {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Endoplasmic reticulum", "Golgi apparatus"],
                 "answer": "Mitochondria"},
                
                {"question": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"],
                 "answer": "6"},
                
                {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                 "answer": "William Shakespeare"},
                
                {"question": "What is the chemical symbol for gold?", "options": ["Gd", "Au", "Ag", "Pt"],
                 "answer": "Au"},
                
                {"question": "Which planet is known as the 'Morning Star'?", "options": ["Mars", "Venus", "Mercury", "Jupiter"],
                 "answer": "Venus"},
                
                {"question": "In what year did the Titanic sink?", "options": ["1910", "1912", "1915", "1918"],
                 "answer": "1912"},
                
                {"question": "What is the largest mammal in the world?", "options": ["Elephant", "Blue whale", "Giraffe", "Hippopotamus"],
                 "answer": "Blue whale"},
                
                {"question": "Who discovered penicillin?", "options": ["Marie Curie", "Alexander Fleming", "Louis Pasteur", "Jonas Salk"],
                 "answer": "Alexander Fleming"},
                
                {"question": "Which country is known as the Land of the Rising Sun?", "options": ["China", "Japan", "South Korea", "Vietnam"],
                 "answer": "Japan"},
                
                {"question": "What is the speed of light?", "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "200,000 km/s"],
                 "answer": "300,000 km/s"},
                
                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Who is the lead singer of the band Queen?", "options": ["Freddie Mercury", "John Lennon", "Mick Jagger", "David Bowie"],
                 "answer": "Freddie Mercury"},

                {"question": "What is the currency of Japan?", "options": ["Yuan", "Yen", "Won", "Baht"],
                 "answer": "Yen"},

                {"question": "Which element has the chemical symbol 'He'?", "options": ["Helium", "Hydrogen", "Hafnium", "Hassium"],
                 "answer": "Helium"},

                {"question": "What is the square of 9?", "options": ["81", "64", "49", "81"],
                 "answer": "81"},
                
                {"question": "In which year did Christopher Columbus first reach the Americas?", "options": ["1492", "1500", "1510", "1498"],
                 "answer": "1492"},
                
                {"question": "What is the main ingredient in guacamole?", "options": ["Tomatoes", "Avocado", "Onions", "Peppers"],
                 "answer": "Avocado"},
                
                {"question": "Who painted 'Starry Night'?", "options": ["Claude Monet", "Pablo Picasso", "Vincent van Gogh", "Salvador Dali"],
                 "answer": "Vincent van Gogh"},

                {"question": "What is the largest desert in the world?", "options": ["Sahara Desert", "Gobi Desert", "Antarctic Desert", "Arabian Desert"],
                 "answer": "Antarctic Desert"},

                {"question": "Which element has the chemical symbol 'K'?", "options": ["Potassium", "Calcium", "Cobalt", "Krypton"],
                 "answer": "Potassium"},

                {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Endoplasmic reticulum", "Golgi apparatus"],
                 "answer": "Mitochondria"},
                
                {"question": "How many chromosomes do humans typically have?", "options": ["42", "46", "50", "52"],
                 "answer": "46"},

                {"question": "What is the largest organ in the human body?", "options": ["Liver", "Skin", "Heart", "Brain"],
                 "answer": "Skin"},

                {"question": "Who wrote '1984'?", "options": ["George Orwell", "Aldous Huxley", "Ray Bradbury", "J.K. Rowling"],
                 "answer": "George Orwell"},

                {"question": "What is the capital of Australia?", "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
                 "answer": "Canberra"},
                
                {"question": "How many colors are there in a rainbow?", "options": ["5", "7", "9", "12"],
                 "answer": "7"},

                {"question": "What is the largest planet in our solar system?", "options": ["Mars", "Earth", "Jupiter", "Saturn"],
                 "answer": "Jupiter"},

                {"question": "Which of the following is a noble gas?", "options": ["Oxygen", "Helium", "Nitrogen", "Carbon dioxide"],
                 "answer": "Helium"},

                {"question": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "N2"],
                 "answer": "H2O"},

                {"question": "How many sides does a dodecagon have?", "options": ["10", "11", "12", "13"],
                 "answer":"12"},

                {"question": "Who wrote 'The Great Gatsby'?", "options": ["F. Scott Fitzgerald", "Ernest Hemingway", "J.D. Salinger", "Jane Austen"],
                 "answer": "F. Scott Fitzgerald"},

                {"question": "What is the largest bird in the world?", "options": ["Eagle", "Ostrich", "Penguin", "Albatross"],
                 "answer": "Ostrich"},
                
                {"question": "Which of the following is a prime number?", "options": ["1", "2", "4", "6"],
                 "answer": "2"},

                {"question": "What is the chemical symbol for iron?", "options": ["I", "Fe", "Au", "Ag"],
                 "answer": "Fe"},

                {"question": "In what year did the first manned moon landing occur?", "options": ["1967", "1969", "1971", "1973"],
                 "answer": "1969"},
                {"question": "What is the largest mountain range on Earth?", "options": ["Rocky Mountains", "Himalayas", "Andes", "Alps"], "answer": "Himalayas"},

                {"question": "Who wrote 'The Catcher in the Rye'?", "options": ["J.K. Rowling", "J.D. Salinger", "Ernest Hemingway", "F. Scott Fitzgerald"],
                 "answer": "J.D. Salinger"},

                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Which planet is known as the 'Red Planet'?", "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                 "answer": "Mars"},

                {"question": "What is the capital of Brazil?", "options": ["Rio de Janeiro", "Brasília", "Sao Paulo", "Salvador"],
                 "answer": "Brasília"},

                {"question": "What is the chemical symbol for gold?", "options": ["Gd", "Au", "Ag", "Pt"],
                 "answer": "Au"},

                {"question": "How many bones are there in the adult human body?", "options": ["206", "180", "220", "250"],
                 "answer": "206"},

                {"question": "Who painted the Sistine Chapel ceiling?", "options": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
                 "answer": "Michelangelo"},

                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},
                {"question": "What is the capital of China?", "options": ["Beijing", "Shanghai", "Hong Kong", "Taipei"],
                 "answer": "Beijing"},

                {"question": "How many planets in our solar system have rings?", "options": ["1", "2", "4", "6"],
                 "answer": "6"},

                {"question": "What is the smallest prime number?", "options": ["0", "1", "2", "3"],
                 "answer": "2"},

                {"question": "Who is the author of 'The Odyssey'?", "options": ["Homer", "Virgil", "Dante", "Sophocles"],
                 "answer": "Homer"},

                {"question": "What is the chemical symbol for oxygen?", "options": ["O2", "O", "Ox", "Om"],
                 "answer": "O"},

                {"question": "In what year did the Berlin Wall fall?", "options": ["1987", "1989", "1991", "1993"],
                 "answer": "1989"},

                {"question": "What is the capital of South Korea?", "options": ["Seoul", "Busan", "Incheon", "Daegu"],
                 "answer": "Seoul"},

                {"question": "Who developed the theory of relativity?", "options": ["Isaac Newton", "Albert Einstein", "Stephen Hawking", "Galileo Galilei"],
                 "answer": "Albert Einstein"},

                {"question": "What is the chemical symbol for silver?", "options": ["Si", "S", "Ag", "Sr"],
                 "answer": "Ag"},
                
                
                {"question": "What is the speed of sound in air?", "options": ["343 meters per second", "500 meters per second", "700 meters per second", "1000 meters per second"],
                 "answer": "343 meters per second"},

                {"question": "Which gas is responsible for the greenhouse effect?", "options": ["Nitrogen", "Carbon dioxide", "Oxygen", "Methane"],
                 "answer": "Carbon dioxide"},

                {"question": "Who wrote 'Pride and Prejudice'?", "options": ["Jane Austen", "Emily Brontë", "Charlotte Brontë", "F. Scott Fitzgerald"],
                 "answer": "Jane Austen"},

                {"question": "What is the largest mammal on land?", "options": ["Elephant", "Giraffe", "Blue whale", "African Elephant"],
                 "answer": "African Elephant"},

                {"question": "What is the chemical symbol for lead?", "options": ["Ld", "Pb", "Le", "Pt"],
                 "answer": "Pb"},

                {"question": "In what year did the United States declare independence?", "options": ["1765", "1776", "1789", "1799"],
                 "answer": "1776"},

                {"question": "Which of the following is a prime number?", "options": ["15", "23", "30", "42"],
                 "answer": "23"},

                {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"],
                 "answer": "Paris"},

                {"question": "Who is known as the 'Father of Computers'?", "options": ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"],
                 "answer": "Charles Babbage"},
                
                {"question": "What is the chemical symbol for sodium?", "options": ["So", "Sd", "Na", "No"],
                 "answer": "Na"},

                {"question": "How many chambers are there in the human heart?", "options": ["2", "3", "4", "5"],
                 "answer": "3"},

                {"question": "Who wrote 'The Canterbury Tales'?", "options": ["William Shakespeare", "Geoffrey Chaucer", "John Milton", "Dante Alighieri"],
                 "answer": "Geoffrey Chaucer"},
                
                {"question": "What is the boiling point of water in Fahrenheit?", "options": ["100°F", "212°F", "150°F", "32°F"],
                 "answer": "212°F"},
                
                {"question": "What is the chemical symbol for helium?", "options": ["H", "He", "Ha", "Hu"],
                 "answer": "He"},
                
                {"question": "In what year did the Renaissance begin?", "options": ["1200", "1300", "1400", "1500"],
                 "answer": "1400"},

                {"question": "What is the capital of Russia?", "options": ["St. Petersburg", "Moscow", "Kiev", "Warsaw"],
                 "answer": "Moscow"},

                {"question": "Who discovered the law of gravity?", "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Johannes Kepler"],
                 "answer": "Isaac Newton"},


                {"question": "What is the chemical symbol for carbon?", "options": ["Ca", "C", "Co", "Cr"],
                 "answer": "C"},

                {"question": "What is the largest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Southern Ocean", "Pacific Ocean"],
                 "answer": "Pacific Ocean"},

                {"question": "Who painted 'The Last Supper'?", "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
                 "answer": "Leonardo da Vinci"},

                {"question": "What is the capital of Argentina?", "options": ["Rio de Janeiro", "Buenos Aires", "Santiago", "Lima"],
                 "answer": "Buenos Aires"},

                {"question": "What is the chemical symbol for nitrogen?", "options": ["N2", "Ni", "No", "Na"],
                 "answer": "N2"},

                {"question": "How many players are there on a standard soccer team?", "options": ["9", "11", "13", "15"],
                 "answer": "11"},
                
                {"question": "Who wrote 'War and Peace'?", "options": ["Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Vladimir Nabokov"],
                 "answer": "Leo Tolstoy"},
                
                {"question": "What is the capital of South Africa?", "options": ["Cape Town", "Johannesburg", "Pretoria", "Bloemfontein"],
                 "answer": "Cape Town"},
                
                {"question": "What is the chemical symbol for potassium?", "options": ["P", "K", "Pt", "Ka"],
                 "answer": "K"},
                
                {"question": "In what year was the Declaration of Independence signed?", "options": ["1776", "1789", "1800", "1812"],
                 "answer": "1776"},
                
                {"question": "What is the largest moon in our solar system?", "options": ["Titan", "Ganymede", "Io", "Europa"],
                 "answer": "Ganymede"},
                
                
                {"question": "Who is the author of 'The Grapes of Wrath'?", "options": ["Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "Harper Lee"],
                 "answer": "John Steinbeck"},
                
                {"question": "What is the chemical symbol for tin?", "options": ["Ti", "Tn", "Sn", "Si"],
                 "answer": "Sn"},
                
                {"question": "In what year did the French Revolution begin?", "options": ["1776", "1789", "1804", "1815"],
                 "answer": "1789"},
                
                {"question": "What is the capital of Turkey?", "options": ["Ankara", "Istanbul", "Athens", "Budapest"],
                 "answer": "Ankara"},
                
                {"question": "Who painted 'The Persistence of Memory'?", "options": ["Salvador Dali", "Pablo Picasso", "Claude Monet", "Vincent van Gogh"],
                 "answer": "Salvador Dali"},
                
                {"question": "What is the chemical symbol for uranium?", "options": ["Ur", "Un", "U", "Ut"],
                 "answer": "U"},
                
                {"question": "In what year did the Great Fire of London occur?", "options": ["1600", "1666", "1700", "1755"],
                 "answer": "1666"},
                
                {"question": "What is the largest desert in Africa?", "options": ["Sahara Desert", "Kalahari Desert", "Namib Desert", "Libyan Desert"],
                 "answer": "Sahara Desert"},
                
                {"question": "Who wrote 'The Scarlet Letter'?", "options": ["Nathaniel Hawthorne", "Emily Brontë", "Herman Melville", "F. Scott Fitzgerald"],
                 "answer": "Nathaniel Hawthorne"},
                
                {"question": "What is the chemical symbol for magnesium?", "options": ["Mg", "Mn", "Mo", "Me"],
                 "answer": "Mg"},
                
                {"question": "In what year did World War II end?", "options": ["1943", "1945", "1947", "1950"],
                 "answer": "1945"},
            ]
            random.shuffle(self.topics)
            
        elif self.subject_var.get() == "Brain Teaser":
            self.topics = [
                {"question": " What has keys but can't open locks?", "options": ["Piano", "Guitar", "Typewriter", "Drum"],
                 "answer": "Drum"},
                
                {"question": "What has keys but can't open locks?","options": ["Piano", "Computer", "Book", "Clock"],
                 "answer": "Clock"},
                
                {"question": "What has a heart that doesn't beat?","options": ["Apple", "Artichoke", "Tomato", "Lettuce"],
                 "answer": "Lettuce"},
                
                {"question": "I speak without a mouth and hear without ears.\n What am I?","options": ["Echo", "Wind", "Radio", "Thunder"],
                 "answer": "Echo"},
                
                {"question": "The more you take, the more you leave behind.\n What am I?","options": ["Footsteps", "Memories", "Choices", "Mistakes"],
                 "answer": "Footsteps"},
                
                {"question": "What comes once in a minute, twice in a moment,\n but never in a thousand years?","options": ["M", "E", "A", "O"],
                 "answer": "M"},
                
                {"question": "What has a head, a tail, is brown,\n and has no legs?","options": ["Penny", "Snake", "Earthworm", "Stick"],
                 "answer": "Penny"},
                
                {"question": "Forward I am heavy, but backward I am not. What am I?","options": ["Ton", "Weight", "Light", "Mass"],
                 "answer": "Ton"},
                
                {"question": "What has a neck but no head?","options": ["Bottle", "Giraffe", "Shirt", "Snake"],
                 "answer": "Bottle"},
                
                {"question": "I have keys but open no locks. What am I?","options": ["Keyboard", "Guitar", "Locksmith", "Calculator"],
                 "answer": "Locksmith"},
                
                {"question": "What has an endless supply of letters but starts empty?","options": ["Library", "Inbox", "Dictionary", "Envelope"],
                 "answer": "Library"},
                
                {"question": "What has a face and two hands but no body?","options": ["Clock", "Watch", "Mirror", "Doll"],
                 "answer": "Clock"},
                
                {"question": "I have cities but no houses, forests but no trees,\n and rivers but no water. What am I?","options": ["Map", "Dictionary", "Globe", "Puzzle"],
                 "answer": "Map"},
                
                {"question": "I can fly without wings. I can cry without eyes.\n Wherever I go, darkness follows me. What am I?","options": ["Cloud", "Wind", "Night", "Bat"],
                 "answer": "Cloud"},
                
                {"question": "What is as big as you are and yet does not weigh anything?","options": ["A Shadow", "A Thought", "A Dream", "A Reflection"],
                 "answer": "A Shadow"},
                
                {"question": "In a year, there are 12 months,\n seven months have 31 days.\n How many months have 28 days?","options": ["One", "Six", "Twelve", "All Twelve"],
                 "answer": "All Twelve"},
                
                {"question": "I’m tall when I’m young, and I’m short when I’m old,\n what am I?","options": ["A Tree", "A Person", "A Candle", "A Giraffe"],
                 "answer": "A Candle"},
                
                {"question": "What is so fragile that saying its name breaks it?","options": ["Silence", "Glass", "Egg", "Whisper"],
                 "answer": "Silence"},

                {"question": "What word is spelled wrong in the dictionary?","options": ["Incorrect", "Misspelled", "Dictionary", "Wrong"],
                 "answer": "Wrong"},

                {"question": "What can travel around the world while staying in a corner?","options": ["Stamp", "Postcard", "Airplane", "Stamp"],
                 "answer": "Stamp"},
                
                {"question": "What can run but not walk,\n has a mouth but never talks,\n has a head but never weeps, has a bed but never sleeps?","options": ["River", "Clock", "Car", "Wind"],
                 "answer": "River"},
                
                {"question": "Do you know what you can hold without ever touching it?","options": ["Breath", "Thought", "Emotion", "Memory"],
                 "answer": "Breath"},
                
                {"question": "Flat as a leaf, round as a ring;\n Has two eyes,\n can't see a thing. What is it?","options": ["Coin", "Button", "Camera", "Mirror"],
                 "answer": "Button"},
                
                {"question": "Where can you find roads without cars,forests without trees, \n and cities without houses  (without people)?","options": ["Map", "Imagination", "Dream", "Desert"],
                 "answer": "Map"},
                
                {"question": "What loses its head in the morning and gets it back at night?","options": ["Pillow", "Sunflower", "Clock", "Coin"],
                 "answer": "Pillow"},
                
                {"question": "A man pushes his car to a hotel and tells its owner that he is bankrupt. Why?","options": ["He lost a bet", "He's playing a game", "The car is a toy", "He's playing charades"],
                 "answer": "He's playing charades"},
                
                {"question": "When young, I am sweet in the sun.\n When middle-aged,I make you gay.\n When old, I am valued more than ever.","options": ["Wine", "Honey", "Friendship", "Gold"],
                 "answer": "Wine"},
                
                {"question": "How can you throw a ball as hard as you can and have it come back to you, \n even if it doesn't bounce off anything? There is nothing attached to it, \n and no one else catches or throws it back to you.","options": ["Throw it up", "Throw it underwater", "Throw it at a wall", "Throw it with a boomerang"],
                 "answer": "Throw it up"},
                
                {"question": "Imagine you’re in a room that is filling with water. \nThere are no windows or doors. How do you get out?","options": ["Stop imagining", "Swim through the water", "Evaporate the water", "Wait for it to drain"],
                 "answer": "Stop imagining"},
                
                {"question": "Feed me and I live, yet give me a drink and I die.","options": ["Fire", "Plant", "Air", "Time"],
                 "answer": "Fire"},
                
                {"question": "You are a cyclist in a cross-country race. \nJust before the crossing finish line you overtake the person in second place!\n What place did you finish in?","options": ["First", "Second", "Third", "Impossible to determine"],
                 "answer": "Second"},
                
                {"question": "With pointed fangs I sit and wait;\n With piercing force I crunch out fate; Grabbing victims, proclaiming might; \n Physically joining with a single bite. What am I?","options": ["Snake", "Spider", "Mosquito", "Vampire"],
                 "answer": "Mosquito"},
                
                {"question": "A farmer has 17 sheep and all but 9 die. How many are left?","options": ["8", "9", "17", "None"],
                 "answer": "9"},
                
                {"question": "A man was driving a black truck.\n His lights were not on. The moon was not out.,\n A lady was crossing the street. How did the man see her?","options": ["It was daytime", "He had night vision", "Street lights were on", "The lady had a flashlight"],
                 "answer": "It was daytime"},
                
                {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?","options": ["The Letter M", "An Idea", "A Memory", "A Dream"],
                 "answer": "The Letter M"},
                
                {"question": "What has six faces, but does not wear makeup, \n has twenty-one eyes, but cannot see? What is it?","options": ["Dice", "Spider", "Book", "Potato"],
                 "answer": "Dice"},
                
                {"question": "You live in a one-story house made entirely of redwood. What color would the stairs be?","options": ["Red", "There are no stairs", "Brown", "White"],
                 "answer": "There are no stairs"},
                
                {"question": "You are in a room with 3 monkeys. One monkey has a banana, one has a stick, and one has nothing.\n Who is the smartest primate?","options": ["Banana monkey", "Stick monkey", "Monkey with nothing", "All equally smart"],
                 "answer": "All equally smart"},
                
                {"question": "This old one runs forever, but never moves at all. He has not lungs nor throat,\n but still a mighty roaring call. What is it?","options": ["A River", "A Mountain", "A Waterfall", "Time"],
                 "answer": "Time"},
                
                {"question": "What five-letter word becomes shorter when you add two letters to it?","options": ["Short", "Brief", "Small", "Quick"],
                 "answer": "Short"},
                
                {"question": "If you drop a white hat into the red sea what does it become?","options": ["Wet", "Pink", "Lost", "Nothing"],
                 "answer": "Wet"},
                
                {"question": "One company owner asks another:\n 'Tell me, Bill, how come your employees are always on time in the mornings?'","options": ["Good Discipline", "Strict Rules", "Early Shifts", "They work from home"],
                 "answer": "They work from home"},
                
                {"question": "When it is alive we sing, when it is dead we clap our hands. What is it?","options": ["Birthday Cake", "Candle", "Fireworks", "Concert"],
                 "answer": "Candle"},
                
                {"question": "What is special about these words: job, polish, herb?","options": ["Pronounced differently","Same number of letters","Palindromes","Start with the same letter"],
                 "answer": "Start with the same letter"},
                
                {"question": "I am taken from a mine, \n and shut up in a wooden case, \n from which I am never released, \n and yet I am used by almost everybody. What am I?","options": ["Gold", "Diamond", "Silver", "Pencil"],
                 "answer": "Pencil"},
                
                {"question": "A man stands on one side of a river,\n his dog on the other. The man calls his dog, \n who immediately crosses the river without getting wet and without using a bridge or a boat.\n How did the dog do it?","options": [ "The river is frozen","The man throws a stick","There is a bridge","The man and the dog are not real"],
                 "answer": "The man and the dog are not real"},
                
                {"question": "I can't be bought, \n but I can be stolen with a glance. \n I'm worthless to one, \n but priceless to two. What am I?","options": ["Love", "Diamond", "Time", "Happiness"],
                 "answer": "Love"},

                {"question": "Turn me on my side and I am everything. Cut me in half and I am nothing. What am I?","options": ["8", "Infinity", "Zero", "O"],
                 "answer": "Infinity"},
                
                {"question": "No matter how little or how much you use me, you change me every month. What am I?","options": ["Water", "Soap", "Money", "Calendar"],
                 "answer": "Calendar"},
                
                {"question": "How can 8 + 8 = 4?","options": ["Roman numerals", "Magic", "Math error", "Cryptic code"],
                 "answer": "Math error"},
                
                {"question": "What has cities, but no houses; forests, but no trees; and water, but no fish?","options": ["Map", "Globe", "Library", "Internet"],
                 "answer": "Map"},
                
                {"question": "A red house is made from red bricks. \n A blue house is made from blue bricks. \n A yellow house is made from yellow bricks. \n What is a greenhouse made from?","options": ["Green bricks", "Plastic", "Glass", "Wood"],
                 "answer": "Glass"},
                
                {"question": "There is a word in the English language in which the first two letters signify a male, \n the first three letters signify a female, \nthe first four signify a great man, and the whole word, \n a great woman. What is the word?","options": ["History", "Future", "Present", "Past"],
                 "answer": "Present"},
                
                {"question": "In my hand I have two coins that are newly minted. \n Together,they total 30 cents. One isn’t a nickel. \n What are the coins?","options": ["Quarter and Nickel", "Dime and Nickel", "Dime and Penny", "Quarter and Dime"],
                 "answer": "Dime and Penny"},
                
                {"question": "What is harder to catch the faster you run?","options": ["Breath", "Cold", "Illness", "Time"],
                 "answer": "Time"},

                {"question": "What kind of running means walking?","options": ["Running water", "Running out", "Running shoes", "Running nose"],
                 "answer": "Running nose"},
                
                {"question": "What can be swallowed, but can also swallow you?","options": ["Pride", "Fear", "Anger", "Water"],
                 "answer": "Water"},
                
                {"question": "They fill me up and you empty me, \n almost every day; if you raise my arm, \n I work the opposite way. What am I?","options": ["Bank", "Pocket", "Gas tank", "Cup"],
                 "answer": "Gas tank"},
                
                {"question": "Which three letters can frighten a thief away? ICU","options": ["BOO", "ICE", "SOS", "911"],
                 "answer": "ICE"},
                
                {"question": "First I am dried, then I am wet. The longer I swim, the more taste you get. What am I?","options": ["Fish", "Tea", "Soup", "Sponge"],
                 "answer": "Tea"},
                
                {"question": "Lovely and round, I shine with pale light, grown in the darkness, A lady's delight. What am I?","options": ["Diamond", "Pearl", "Moon", "Sun"],
                 "answer": "Pearl"},
                
                {"question": "My voice is tender, my waist is slender \n and I'm often invited to play. Yet wherever I go I must take my bow \n or else I have nothing to say. What am I?","options": ["Flute", "Guitar", "Violin", "Trumpet"],
                 "answer": "Violin"},
                
                {"question": "I am a box that holds keys without locks, yet they can unlock your soul. What am I?","options": ["Safe", "Chest", "Piano", "Book"],
                 "answer": "Piano"},

                {"question": "I have a big mouth and I am also quite loud! \n I am NOT a gossip but I do get involved with everyone's dirty business. \n What am I?","options": ["Gossip", "Speaker", "Mouthwash", "Vacuum cleaner"],
                 "answer": "Mouthwash"},
                
                {"question": "I have four wings, but cannot fly,\n I never laugh and never cry; \n On the same spot I'm always found, \n toiling away with little sound. What am I?","options": ["Dragonfly", "Windmill", "Airplane", "Butterfly"],
                 "answer": "Windmill"},
                
                {"question": "What can be stolen, mistaken, or altered, yet never leaves you your entire life?","options": ["Memory", "Identity", "Heart", "Time"],
                 "answer": "Identity"},
                
                {"question": "Until I am measured, I am not known. Yet you miss me when I have flown. What am I?","options": ["Distance", "Time", "Air", "Love"],
                 "answer": "Time"},
                
                {"question": "Some try to hide, some try to cheat,\n  but time will show, we always will meet.\n Try as you might, to guess my name, \n I promise you'll know, when you do claim. Who am I?","options": ["Fate", "Destiny", "Death", "Life"],
                 "answer": "Death"},
                
                {"question": "Four cars come to a four-way stop,\n all coming from a different direction.\n They can't decide who got there first, \n so they all go forward at the same time. \n They do not crash into each other, but all four cars go. How is this possible?","options": ["Nighttime", "Traffic signal", "Roundabout", "They all made right-hand turns"],
                 "answer": "They all made right-hand turns"},
                
                {"question": "Take one out and scratch my head, I am now black but once was red. What am I?","options": ["Apple", "Tomato", "Match", "Cherry"],
                 "answer": "Match"},
                
                {"question": "I weaken all men for hours each day. I show you strange visions while you are away.\n I take you by night, by day take you back. None suffer to have me, but do from my lack. What am I?","options": ["Dream", "Imagination", "Sleep", "Nightmare"],
                 "answer": "Sleep"},

                {"question": "He has married many women, but has never been married. Who is he?","options": ["A polygamist", "A pastor", "A groom", "A preacher"],
                 "answer": "A preacher"},
                
                {"question": "My life is often a volume of grief,\n your help is needed to turn a new leaf.\n Stiff is my spine and my body is pale, \n but I'm always ready to tell a tale. What am I?","options": ["A book", "A candle", "A diary", "A letter"],
                 "answer": "A book"},
                
                {"question": "What has no hands but might knock on your door, and if it does you better open up?","options": ["Opportunity", "A storm", "A ghost", "A friend"],
                 "answer": "Opportunity"},
                
                {"question": "What do you throw out when you want to use it but take in when you don't want to use it?","options": ["Trash", "A lifeline", "An anchor", "A net"],
                 "answer": "An anchor"},
                
                {"question": "I can be short and sometimes hot. When displayed, I rarely impress. What am I?","options": ["Coffee", "Temperature", "Temper", "Fire"],
                 "answer": "Temper"},
                
                {"question": "What can be driven although it doesn't have wheels, sliced but stays whole?","options": ["A pie", "A golf ball", "A pizza", "A loaf of bread"],
                 "answer": "A golf ball"},
                
                {"question": "The cost of making only the maker knows, Valueless if bought,\n but sometimes traded. A poor man may give one as easily as a king. \nWhen one is broken, pain and deceit are assured. What is it?","options": ["A promise", "A diamond", "A secret", "A friendship"],
                 "answer": "A promise"},
                
                {"question": "What rocks but does not roll?","options": ["A mountain", "A boulder", "A chair", "A rocking chair"],
                 "answer": "A rocking chair"},
                
                {"question": "Shoot at me a thousand times and I may still survive.\n But, one scratch from me \n and you will find your prospects take a dive.\n What am I?","options": ["A bulletproof vest", "An eight-ball", "A shield", "A mirror"],
                 "answer": "An eight-ball"},
                
                {"question": "Why is the letter F like death?","options": ["It's the end", "It signifies failure", "Because without it life is a lie, or it makes life a lie.", "It's forbidden"],
                 "answer": "Because without it life is a lie, or it makes life a lie."},
                
                {"question": "You do not want to have it, But when you do have it, You do not want to lose it. What is it?","options": ["A headache", "A job", "A lawsuit", "A friend"],
                 "answer": "A lawsuit"},
                
                {"question": "Guess the next three letters in the series GTNTL.","options": ["I, T, S", "L, E, T", "F, O, R", "O, N, E"],
                 "answer": "I, T, S"},
                
                {"question": "Arnold Schwarzenegger has a long one. Michael J. Fox has a short one.\n Madonna does not use hers. Bill Clinton always uses his.\n The Pope never uses his. What is it?","options": ["A middle name", "A last name", "A stage name", "A nickname"],
                 "answer": "A last name"},
                
                {"question": "The number 8,549,176,320 is a unique number. What is so special about it?","options": ["It's a prime number", "It's the largest number", "It's a palindrome", "This is the only number that includes all the digits arranged in alphabetical order."],
                 "answer": "This is the only number that includes all the digits arranged in alphabetical order."},
                
                {"question": "Find a number less than 100 that is increased by \n one-fifth of its value when its digits are reversed.","options": ["27", "45", "63", "81"],
                 "answer": "45"},
                
                {"question": "What letter comes next in the following sequence? D R M F S L T _","options": ["X", "A", "E", "I"],
                 "answer": "E"},
    
                {"question": "You are in a place called Wally’s World and there is only one law. \n There is a mirror, but no reflection. There is pizza with cheese, but not sausage.\n There is pepper, but no salt. There is a door, yet no entrance or exit. What is the law?","options": ["No mirrors allowed", "No sausage on pizza", "No salt with pepper", "No entrance or exit allowed"],
                 "answer": "No salt with pepper"},
                
                {"question": "I come in different shapes and sizes. Parts of me are curved, \n other parts are straight. You can put me anywhere you like, \n but there is only one right place for me. What am I?","options": ["A tool", "A puzzle piece", "A toy", "A building block"],
                 "answer": "A puzzle piece"},
                
                {"question": "I have no eyes, no legs, or ears, and I help move the earth. What am I?","options": ["A tractor", "An earthworm", "A shovel", "A bulldozer"],
                 "answer": "An earthworm"},
                
                {"question": "A sundial has the fewest moving parts of any timepiece. Which has the most?","options": ["An hourglass, with thousands of grains of sand", "A digital clock", "A pendulum clock", "A wall clock"],
                 "answer": "An hourglass, with thousands of grains of sand"},
                
                {"question": "Put a coin into an empty bottle and insert a cork into the neck.\n How can you remove the coin \n without removing the cork or breaking the bottle?","options": ["Use a straw to push the coin out", "Turn the bottle upside down and shake the coin out", "Break the bottle to get the coin", "Use a vacuum cleaner"],
                 "answer": "Turn the bottle upside down and shake the coin out"},
                
                {"question": "In 1990, a person was 15 years old. In 1995,\n that same person was 10 years old. How can this be?","options": ["Time travel", "The person ages backward", "It's a mistake", "The person has a twin"],
                 "answer": "The person ages backward"},

                {"question": "Two boxers are in a match scheduled for 12 rounds. \n One of the boxers gets knocked out after only six rounds, yet no man throws a punch. \n How is this possible?","options": ["They are practicing shadow boxing", "Both the boxers were female", "The match was canceled", "The knocked-out boxer was injured"],
                 "answer": "Both the boxers were female"},
                
                {"question": "What does this mean? I RIGHT I","options": ["I have the right", "Turn right", "Right between the eyes", "I am right"],
                 "answer": "Right between the eyes"},
                
                {"question": "I have a large money box, 10 inches wide and 5 inches tall.\n Roughly how many coins can I place until \n my money box is no longer empty?","options": ["One", "Five", "As many as you want", "Just one, after which it will no longer be empty."],
                 "answer": "Just one, after which it will no longer be empty."},
                
                {"question": "Brothers and sisters I have none but this man's father is my father's son. Who is the man?","options": ["My son", "My nephew", "My brother", "My cousin"],
                 "answer": "My brother"},
                
                {"question": "Who makes it, has no need of it. Who buys it, has no use for it.\n Who uses it can neither see nor feel it. What is it?","options": ["A coffin", "A hat", "A shoe", "A wedding ring"],
                 "answer": "A coffin"},
                
                {"question": "What can you keep after giving to someone?","options": ["A promise", "A secret", "A smile", "A loan"],
                 "answer": "A promise"}
            ]
            random.shuffle(self.topics)
            
        elif self.topic == "Mythology":
            self.topics = [
                {"question": " In Greek mythology, who was the\ngod of the sky?", "options": ["Zeus", "Poseidon", "Hades", "Apollo"],
                 "answer": "Apollo"},
                {"question": "In Norse mythology, what is the\nname of the hammer wielded by Thor?", "options": ["Gungnir", "Mjolnir", "Excalibur", "Caladbolg"],
                 "answer": "Mjolnir"},
                {"question": " In Hindu mythology, who is the\ngod of destruction?", "options": ["Vishnu", "Shiva", "Brahma", "Indra"],
                 "answer": "Shiva"},
                {"question": " In Egyptian mythology, who is\nthe god of the afterlife?", "options": [" Anubis", "Osiris", "Horus", "Ra"],
                 "answer": "Osiris"},
                {"question": "In Greek mythology, who is the god of wine?", "options": ["Dionysus", "Hermes", "Apollo", "Ares"],
                 "answer": "Dionysus"},
                {"question": " In Norse mythology, what is the name of the\nserpent that encircles the world?", "options": ["Jormungand", "Nidhogg", "Fenrir", "Hel"],
                 "answer": "Jormungand"},
                {"question": "In Greek mythology, who is the god of the sea?", "options": ["Poseidon", "Zeus", "Hades", "Apollo"],
                 "answer": "Poseidon"},
                {"question": "In Hindu mythology, who is the god of love?", "options": ["Vishnu", "Shiva", "Brahma", "Kama"],
                 "answer": "Kama"},
                {"question": "In Egyptian mythology, who is\nthe goddess of magic?", "options": ["Isis", "Hathor", "Bastet", "Sekhmet"],
                 "answer": "Isis"},
                {"question": " In Greek mythology, who is the god of war?", "options": ["Ares", "Hermes", "Apollo", "Dionysus"],
                 "answer": "Ares"},
                {"question": "Who is the king of the gods?", "options": ["Ares", "Zeus", "Apollo", "Dionysus"],
                 "answer": "Zeus"},
                {"question": " Who is the goddess of beauty and love?", "options": ["Ares", "Zeus", "Apollo", "Aphrodite"],
                 "answer": "Aphrodite"},
                {"question": " Who is the queen of the gods?", "options": ["Hera", "Hermes", "Apollo", "Dionysus"],
                 "answer": "Hera"},
                {"question": "Who was the leader of the Argonauts?", "options": ["Ares", "Hermes", "Jason", "Dionysus"],
                 "answer": "Jason"},
                {"question": " Who was the nymph Apollo chased?", "options": ["Ares", "Daphne", "Jason", "Dionysus"],
                 "answer": "Daphne"},
                {"question": " What did Prometheus gift to humanity?", "options": ["Earth", "Fire", "Water", "Wind"],
                 "answer": "Fire"},
                {"question": "Who flew too close to the sun?", "options": ["Ares", "Icarus", "Jason", "Dionysus"],
                 "answer": "Icarus"},
                {"question": " Who was the goddess of the rainbow?", "options": ["Hera", "Hermes", "Iris", "Dionysus"],
                 "answer": "Iris"},
                {"question": " How many Greek gods lived on Mount Olympus?", "options": ["8", "16", "10", "12"],
                 "answer": "12"},
                {"question": "Who was the Greek goddess of Earth?", "options": ["Gaia", "Hermes", "Iris", "Dionysus"],
                 "answer": "Gaia"},
                {"question": "Who was the first human woman\ncreated by the Greek gods?", "options": ["Ares", "Daphne", "Pandora", "Dionysus"],
                 "answer": "Pandora"},
                {"question": "Which Greek goddess had snakes for hair?", "options": ["Gaia", "Hermes", "Medusa", "Dionysus"],
                 "answer": "Medusa"},
                {"question": "How long did it take Odysseus to\nget home from the Trojan War?", "options": ["8 years", "16 years", "10 years", "12 years"],
                 "answer": "10 years"},
                {"question": "What monster did Theseus slay?", "options": ["Minotaur", "Nidhogg", "Fenrir", "Hel"],
                 "answer": "Minotaur"},
                {"question": "Who were the parents of all Titans?", "options": ["Apollo and Daphne", "Zeus and Hera", "Gaea and Uranus", "Hades abd Aprodite"],
                 "answer": "Gaea and Uranus"},
                {"question": "Who designed the labyrinth for King Minos?", "options": ["Gaia", "Hermes", "Iris", "Daedalus"],
                 "answer": "Daedalus"},
                {"question": "Which Greek god formed dreams?", "options": ["Morpheus", "Hermes", "Iris", "Daedalus"],
                 "answer": "Morpheus"},
                {"question": "What’s the staff carried by Hermes called?", "options": ["Xiphos", "Gastraphetes", "Caduceus", "Sarissa"],
                 "answer": "Caduceus"},
                {"question": "Who was the Greek goddess of memory?", "options": ["Morpheus", "Hermes", "Iris", "Mnemosyne"],
                 "answer": "Mnemosyne"},
                {"question": "Who was the Greek goddess of victory?", "options": ["Nike", "Hermes", "Medusa", "Dionysus"],
                 "answer": "Nike"},
                {"question": "Which goddess is Apollo’s twin sister?", "options": ["Morpheus", "Artemis", "Iris", "Mnemosyne"],
                 "answer": "Artemis"},
                {"question": "What was the name of the horse Bellerophon rode?", "options": ["Jormungand", "Nidhogg", "Fenrir", "Pegasus"],
                 "answer": "Pegasus"},
                {"question": "Who was the Greek god of the underworld?", "options": ["Zeus", "Hades", "Poseidon", "Apollo"],
                 "answer": "Hades"},
                {"question": "Who was the Greek goddess of wisdom and war?", "options": ["Athena", "Hades", "Poseidon", "Apollo"],
                 "answer": "Athena"},
                {"question": "How many times did Hercules defeat Ares?", "options": ["Once", "twice", "Trice", "All of Above"],
                 "answer": "Twice"},
                {"question": " Who was the god of blacksmiths and fire?", "options": ["Zeus", "Hades", "Poseidon", "Hephaestus"],
                 "answer": "Hephaestus"},
                {"question": " Whose sacred animal is the quail?", "options": ["Jormungand", "Nidhogg", "Asteria", "Pegasus"],
                 "answer": "Asteria"},
                {"question": "Who was the goddess of music and dance?", "options": ["Athena", "Mousai", "Poseidon", "Apollo"],
                 "answer": "Mousai"},
                {"question": "Which Greek god rode a panther?", "options": ["Zeus", "Dionysus", "Poseidon", "Hephaestus"],
                 "answer": "Dionysus"},
                {"question": "Who held up the sky?", "options": ["Atlas", "Artemis", "Iris", "Mnemosyne"],
                 "answer": "Atlas"},
                {"question": "Who was the Greek god of sleep?", "options": ["Zeus", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Hypnos"},
                {"question": "Who was the Greek counterpart of Cupid?", "options": ["Atlas", "Artemis", "Iris", "Eros"],
                 "answer": "Eros"},
                {"question": "How many heads did the ant-eating\nserpent Amphisbaena have?", "options": ["3", "6", "1", "2"],
                 "answer": "2"},
                {"question": "Who was placed among the stars as\nthe constellation Aquarius?", "options": ["Ganymedes", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Ganymedes"},
                {"question": " What was a female monster with the lion’s body,\neagle’s wings, and woman’s head and breasts?", "options": ["Jormungand", "Nidhogg", "The Sphinx", "Pegasus"],
                 "answer": "The Sphinx"},
                {"question": "Who was the goddess of the dawn?", "options": ["Eos", "Dionysus", "Hypnos", "Hephaestus"],
                 "answer": "Eos"},
                {"question": "Who was the first wife of Zeus?", "options": ["Hera", "Athena", "Daphne", "Meis"],
                 "answer": "Metis"},
                {"question": "Who was the king of Pherae in the region\nof Thessaly and son of Pheres?", "options": ["Percy", "Kratos", "Hector", "Admetus"],
                 "answer": "Admetus"},
                {"question": "Which Trojan prince was considered\nthe greatest warrior of Troy?", "options": ["Percy", "Kratos", "Hector", "Admetus"],
                 "answer": "Hector"},
                {"question": "Which of Poseidon’s sons became the\ndemigod of the sea?", "options": ["Triton", "Kratos", "Hector", "Admetus"],
                 "answer": "Triton"},
                {"question": "Which Greek monster had 12 tentacles\nand six heads?", "options": ["Fenrir", "Hel", "Nidhogg", "Scylla"],
                 "answer": "Scylla"},
                {"question": "Who did Zeus put in an eternal sleep?", "options": ["Eos", "Dionysus", "Endymion", "Hephaestus"],
                 "answer": "Endymion"},
                {"question": "Who helped Theseus escape the Labyrinth?", "options": ["Ariadne", "Dionysus", "Endymion", "Hephaestus"],
                 "answer": "Ariadne"},
                {"question": " Who was the god of questioning\nand the inquisitive mind?", "options": ["Hera", "Coeus", "Daphne", "Meis"],
                 "answer": "Coeus"},
                {"question": " Who cut out Philomela’s tongue?", "options": ["Eos", "Dionysus", "Endymion", "Tereus"],
                 "answer": "Tereus"},
                {"question": "Who understood the language of animals?", "options": ["Triton", "Kratos", "Melampus", "Admetus"],
                 "answer": "Melampus"},
                {"question": " Who did the Isthmian Games honor?", "options": ["Athena", "Hades", "Poseidon", "Apollo"],
                 "answer": "Poseidon"},
                {"question": " Who built the Trojan Horse?", "options": ["Athena", "Epeius", "Poseidon", "Apollo"],
                 "answer": "Epeius"},
                {"question": "Who was the goddess of magic and ghosts?", "options": ["Hecate", "Epeius", "Poseidon", "Apollo"],
                 "answer": "Hecate"},
                {"question": " Who wished that everything he\ntouched would turn into gold?", "options": ["Hecate", "Epeius", "Poseidon", "King Midas"],
                 "answer": "King Midas"},
                {"question": " Who gave Athens its name?", "options": ["Triton", "Kratos", "Cecrops", "Admetus"],
                 "answer": "Cecrops"},
                {"question": "Who did Hades abduct?", "options": ["Athena", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Persephone"},
                {"question": " How man goddesses were in the Kharites?", "options": ["4", "6", "1", "3"],
                 "answer": "3"},
                {"question": " Who was the Titan goddess of\ndivine law and order?", "options": ["Themis", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Themis"},
                {"question": "Who was the Greek god of wine-making\nand drunkenness?", "options": ["Themis", "Persephone", "Silenus", "Apollo"],
                 "answer": "Silenus"},
                {"question": " Who fell in love with a statue he carved?", "options": ["Pygmalion", "Kratos", "Melampus", "Admetus"],
                 "answer": "Pygmalion"},
                {"question": " Who was the Greek god of medicine?", "options": ["Athena", "Asclepius", "Poseidon", "Apollo"],
                 "answer": "Asclepius"},
                {"question": "Which Greek goddess helped Troy\nin the Trojan War?", "options": ["Penthesilea", "Persephone", "Poseidon", "Apollo"],
                 "answer": "Penthesilea"},
                {"question": " Lord Rama belonged to which of\nthe following era or yuga?", "options": ["Dwapara", "Tret Yuga", "None of the above", "Kali"],
                 "answer": "Tret Yuga"},
                {"question": " According to Hindu mythology,\nKing Kansa was the uncle of ______.", "options": ["Rama", "Arjuna", "Krishna", "Duryodhana"],
                 "answer": "Krishna"},
                {"question": "Who among the following is the\ncharioteer of Lord Surya?", "options": ["Arjun", "Jallandhar", "Arun", "Karna"],
                 "answer": "Arjun"},
                {"question": " In Hindu mythology, who is also called ‘Mihira’?", "options": ["Indra", "Balrama", "Surya", "Bheema"],
                 "answer": "Surya"},
                {"question": " In Hindu mythology, who was the first man to die?", "options": ["Ganesha", "Narada", "Yama", "Indra"],
                 "answer": "Yama"},
                {"question": "Who is the god of death in Hindu mythology?", "options": ["Yama", "Indra", "Varuna", "Agni"],
                 "answer": "Yama"},
                {"question": " Who is the goddess of wealth and\nprosperity in Hindu mythology?", "options": ["Saraswati", "Lakshmi", "Durga", "Kali"],
                 "answer": "Lakshmi"},
                {"question": " In Mahabharat, Devavrata was the other name of:", "options": ["Arjun", "Bhishma", "Krishna", "Balaram"],
                 "answer": "Bhishma"},
                {"question": " How many incarnations of Vishnu appeared in\nSatya or Krita Yuga from his Dashavatar?", "options": ["3", "2", "5", "4"],
                 "answer": "4"},
                {"question": " Which one is the first avatar of\nLord Vishnu from his Dashavatar?", "options": ["Matsya", "Kurma", "Varah", "Narasimbha"],
                 "answer": "Matsya"},
                {"question": " In the Narasimbha avatar, Lord Vishnu killed:", "options": ["Hiranyakashipu", "Bali", "Ravan", "Mayasura"],
                 "answer": "Hiranyakashipu"},
                {"question": " In which Yuga, Shree Rama was born in Ayodhya?", "options": ["Satya Yuga", "Treta Yuga", "Dwapara Yuga", "Kali Yuga"],
                 "answer": "Treta Yuga"},
                {"question": " Sati (wife of Lord Shiva) was the daughter of:", "options": ["Kubera", "Daksha Prajapati", "Himavan", "None of the above"],
                 "answer": "Daksha Prajapati"},
                {"question": " Who wrote down the epic Mahabharata\nwhile Vyasa was dictating?", "options": ["Narada", "Vishwakarma", "Ganesha", "Shiva"],
                 "answer": "Ganesha"},
                {"question": " Who brought the River goddess Ganga to\nEarth from the heavens?", "options": ["Shree Rama", "Krishna", "Bhagiratha", "Raja Harishchandra"],
                 "answer": "Bhagiratha"},
                {"question": " In which Yuga, Krishna was born?", "options": ["Satya Yuga", "Treta Yuga", "Dwapara Yuga", "Kal Yuga"],
                 "answer": "Kal Yuga"},
                {"question": " What is the final incarnation of\nLord Vishnu in his Dashavatara?", "options": ["Kurma", "Krishna", "Parashuram", "Kalki"],
                 "answer": "Kalki"},
                {"question": " Who was the son of Fergus mac Roigh,\nwho was mortally wounded by Conall Cernach?", "options": ["Ith", "Iollan", "Iuchar", "Lucharba"],
                 "answer": "Lucharba"},
                {"question": " How many distinct chronological\ncycles are there in Irish mythology?", "options": ["3", "2", "5", "4"],
                 "answer": "4"},
                {"question": " Which one is the first cycle in Irish mythology?", "options": ["Mythological Cycle", "Ulster Cycle", "Fenian Cycle", "Historical Cycle"],
                 "answer": "Mythological Cycle"},
                {"question": " What is the name of the Brazilian goddess of the moon?", "options": ["Iansã", "Oxum", "Nanã", "Jaci"],
                 "answer": "Jaci"},
                {"question": " Who was the Great Queen, the archetypal form of the\nGoddess in Ireland, and often associated with war?", "options": ["Morrigan", "Morfessa", "Moriath", "Murine"],
                 "answer": "Morrigan"},
                {"question": " Which one is the Land of Youth and immortality where\ngods and men lived together in a world of beauty?", "options": ["Tir Na n’Og", "Tir Na mBeo", "Tir Na mBan", "Tir Tairngire"],
                 "answer": "Tir Na n’Og"},
                {"question": " Who was the wife of Mongan and was\nborn the same night as he?", "options": ["Dubhlaing", "Dubh Lacha", "Donn", "Diuran"],
                 "answer": "Dubh Lacha"},
                {"question": " Who was the hag who helped Mongan retrieve his wife?", "options": ["Coinchend", "Cuirithir", "Cuimhne", "Creidne"],
                 "answer": "Coinchend"},
                {"question": " Who was the leader of the first\ninvasion of Ireland and the chief of every craft?", "options": ["Patrick", "Paddy", "Pooka", "Partholon"],
                 "answer": "Partholon"},
                {"question": " Who was the master of wisdom who gave in to Lugh’s\nkeeping of the spear, which gave victory in battle?", "options": ["Esras", "Eremon", "Etain", "Esriu"],
                 "answer": "Esras"},
                {"question": " Who is the god of the underworld in Japanese mythology?", "options": ["Izanami", "Amaterasu", "Susanoo", "Emma-ö"],
                 "answer": "Emma-ö"},
                {"question": " Who is the god of wisdom and\nintelligence in Japanese mythology?", "options": ["Hachiman", "Inari", "Omoikane", "Susanoo"],
                 "answer": "Omoikane"},
                {"question": " Who is the god of the wind in Japanese mythology?", "options": ["Fujin", "Raijin", "Tsukuyomi", "Ryujin"],
                 "answer": "Fujin"},
                {"question": " Who is the god of agriculture in Japanese mythology?", "options": ["Inari", "Hachiman", "Susanoo", "Amaterasu"],
                 "answer": "Inari"},
                {"question": " Who is the god of war in Japanese mythology?", "options": ["Hachiman", "Inari", "Kagutsuchi", "Tsukuyomi"],
                 "answer": "Hachiman"},
            ]
            random.shuffle(self.topics)
     
        elif self.topic == "Music":
            self.topics = [
                 {"question": " What singer is known as The Vocal Bible?", "options": ["Brandy", "Michael Jackson", "Prince", "Madonna"],
                 "answer": "Brandy"},
                {"question": " Who is known as the King of Pop?", "options": ["Elvis Presley", "Michael Jackson", "Madonna  D. Prince"],
                 "answer": "Michael Jackson"},
                {"question": "Which instrument does Yo-Yo Ma play?", "options": ["Violin","Cello", "Piano", "Flute "],
                 "answer": "Violin"},
                {"question": "What is the main ingredient in\ntraditional Irish folk music?", "options": ["Bagpipes", "Banjo", "Fiddle", "Accordion"],
                 "answer": "Fiddle"},
                {"question": "Who wrote the famous musical Les Misérables?", "options": ["Andrew Lloyd Webber", "Stephen Sondheim", "Claude-Michel Schönberg", "Rodgers and Hammerstein"],
                 "answer": "Claude-Michel Schönberg"},
                {"question": "Which rock band released the album\nThe Dark Side of the Moon?", "options": ["The Rolling Stones", "The Beatles", "Pink Floyd", "Led Zeppelin"],
                 "answer": "Pink Floyd"},
                {"question": "What genre is associated with Bob Marley?", "options": ["Reggae", "Hip-hop", "Country", "Blues"],
                 "answer": "Reggae"},
                {"question": "Who is known as the Queen of Soul?", "options": ["Whitney Houston", "Aretha Franklin", "Diana Ross", "Etta James"],
                 "answer": "Aretha Franklin"},
                {"question": "In classical music, which period does Beethoven belong to?", "options": ["Baroque", "Romantic", "Classical", "Renaissance"],
                 "answer": "Classical"},
                {"question": "What is the most common time signature in Western music?", "options": ["4/4", "3/4", "6/8", "2/2"],
                 "answer": "4/4"},
                {"question": "Who was the lead singer of the band Queen?", "options": ["Freddie Mercury", "David Bowie", "Roger Taylor", "Brian May"],
                 "answer": "Freddie Mercury"},
                {"question": "Which instrument is central to a mariachi band?", "options": ["Trumpet", "Guitar", "Violin", "Accordion"],
                 "answer": "Violin"},
                {"question": "What is the name of the classical composer known for his famous\nRide of the Valkyries?", "options": ["Ludwig van Beethoven", "Richard Strauss", "Wolfgang Amadeus Mozart", "Richard Wagner"],
                 "answer": "Richard Wagner"},
                {"question": "Which genre is often associated with artists like\nMuddy Waters and B.B. King?", "options": ["Jazz", "Blues", "Rock and Roll", "Country"],
                 "answer": "Blues"},
                {"question": "What is the primary woodwind\ninstrument in an orchestra?", "options": ["Clarinet", "Flute", "Oboe", "Bassoon"],
                 "answer": "Flute"},
                {"question": "Who sang the theme song for the\nJames Bond film Skyfall?", "options": ["Adele", "Beyoncé", "Rihanna", "Katy Perry"],
                 "answer": "Adele"},
                {"question": "Which Beatles album features the song Hey Jude?", "options": ["Reggae", "Hip-hop", "Country", "Blues"],
                 "answer": "Reggae"},
                {"question": "What genre is associated with Bob Marley?", "options": ["Abbey Road", "The White Album", "Sgt. Pepper's Lonely Hearts Club Band", "Let It Be"],
                 "answer": "The White Album"},
                {"question": "What is the highest male singing voice?", "options": ["Tenor", "Baritone", "Bass", "Countertenor"],
                 "answer": "Tenor"},
                {"question": "In which country did the flamenco\nmusic and dance originate?", "options": ["Spain", "Italy", "France", "Portugal"],
                 "answer": "Spain"},
                {"question": "Who composed The Four Seasons?", "options": ["Antonio Vivaldi", "Johann Sebastian Bach", "George Frideric Handel", "Wolfgang Amadeus Mozart"],
                 "answer": "Antonio Vivaldi"},
                {"question": "Who sang the hit song Careless Whisper?", "options": ["George Michael", "Michael Jackson", "Prince", "Madonna"],
                 "answer": "George Michael"},
                {"question": "Which band had a hit with\nthe song Sweet Child O’ Mine?", "options": ["Guns N’ Roses", "Bon Jovi", "Aerosmith", "Van Halen"],
                 "answer": "Guns N’ Roses"},
                {"question": "Who sang the song Billie Jean?", "options": ["Michael Jackson", "Prince", "Madonna", "Whitney Houston"],
                 "answer": "Michael Jackson"},
                {"question": "Which band had a hit with\nthe song Livin’ on a Prayer?", "options": ["Bon Jovi", "Guns N’ Roses", "Aerosmith", "Van Halen"],
                 "answer": "Bon Jovi"},
                {"question": "Who sang the song Like a Virgin?", "options": ["Madonna", "Whitney Houston", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Madonna"},
                {"question": "Which band had a hit with the song Jump?", "options": ["Van Halen", "Bon Jovi", "Guns N’ Roses", "Aerosmith"],
                 "answer": "Van Halen"},
                 {"question": "Who sang the song I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Whitney Houston"},
                 {"question": "Which band had a hit with\nthe song Every Breath You Take?", "options": ["The Police", "U2", "Duran Duran", "The Cure"],
                 "answer": "The Police"},
                 {"question": "Who sang the song Girls Just Want to Have Fun?", "options": ["Cyndi Lauper", "Madonna", "Whitney Houston", "Tina Turner"],
                 "answer": "Cyndi Lauper"},
                 {"question": "Which band had a hit with the song Take on Me?", "options": ["A-ha", "Duran Duran", "The Cure", "U2"],
                 "answer": "A-ha"},
                 {"question": "Who sang the hit song Stairway to Heaven?", "options": ["Led Zeppelin", "Pink Floyd", "The Rolling Stones", "The Beatles"],
                 "answer": "Led Zeppelin"},
                 {"question": "Which band had a hit with\nthe song Bohemian Rhapsody?", "options": ["Queen", "The Who", "The Doors", "The Kinks"],
                 "answer": "Queen"},
                 {"question": "Who sang the song Stayin’ Alive?", "options": ["Bee Gees", "ABBA", "The Jackson 5", "The Temptations"],
                 "answer": "Bee Gees"},
                 {"question": "Which band had a hit with\nthe song Hotel California?", "options": ["Eagles", "Fleetwood Mac", "Journey", "Boston"],
                 "answer": "Eagles"},
                 {"question": "Who sang the song I Will Survive?", "options": ["Gloria Gaynor", "Donna Summer", "Diana Ross", "Cher"],
                 "answer": "Gloria Gaynor"},
                 {"question": "Which band had a hit with the song Dream On?", "options": ["Aerosmith", "Van Halen", "Guns N’ Roses", "Bon Jov"],
                 "answer": "Aerosmith"},
                 {"question": "Who sang the song Imagine?", "options": ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"],
                 "answer": "John Lennon"},
                 {"question": "Which band had a hit with the song We Will Rock You?", "options": ["Queen", "AC/DC", "Black Sabbath", "Deep Purple"],
                 "answer": "Queen"},
                 {"question": "Who sang the song American Pie?", "options": ["Don McLean", "Bob Dylan", "Neil Young", "Jim Croce"],
                 "answer": "Don McLean"},
                 {"question": "Which band had a hit with the song Stayin’ Alive?", "options": ["Bee Gees", "ABBA", "The Jackson 5", "The Temptations"],
                 "answer": "Bee Gees"},
                 {"question": "Who sang the hit song What a Wonderful World?", "options": ["Louis Armstrong", "Frank Sinatra", "Elvis Presley", "The Beatles"],
                 "answer": "Louis Armstrong"},
                 {"question": "Which rock-and-roll star\nwas famously nicknamed The King?", "options": ["Elvis Presley", "Chuck Berry", "Little Richard", "Jerry Lee Lewis"],
                 "answer": "Elvis Presley"},
                 {"question": "Who sang Brown Eyed Girl?", "options": ["Van Morrison", "Bob Dylan", "Neil Young", "Jim Croce"],
                 "answer": "Van Morrison"},
                 {"question": "Which band recorded the album\nSgt. Pepper’s Lonely Hearts Club Band?", "options": ["The Beatles", "The Rolling Stones", "The Who", "Pink Floyd"],
                 "answer": "The Beatles"},
                 {"question": "Who sang the song\nI Heard It Through the Grapevine?", "options": ["Marvin Gaye", "Stevie Wonder", "Otis Redding", "James Brown"],
                 "answer": "Marvin Gaye"},
                 {"question": "Who sang the song My Girl?", "options": ["The Temptations", "The Four Tops", "The Supremes", "The Miracles"],
                 "answer": "The Temptations"},
                 {"question": "Who sang the song Respect?", "options": ["Aretha Franklin", "Diana Ross", "Gladys Knight", "Tina Turner"],
                 "answer": "Aretha Franklin"},
                 {"question": "Which band had a hit with the song Light My Fire?", "options": ["The Doors", "The Who", "The Kinks", "The Rolling Stones"],
                 "answer": "The Doors"},
                 {"question": "Who sang the song Ain’t No Mountain High Enough?", "options": ["Marvin Gaye and Tammi Terrell", "Diana Ross", "Stevie Wonder", "The Temptations "],
                 "answer": "Marvin Gaye and Tammi Terrell"},
                 {"question": "Who sang the song Blowin’ in the Wind?", "options": ["Bob Dylan", "Neil Young", "Jim Croce", "Simon & Garfunkel"],
                 "answer": "Bob Dylan"},
                 {"question": "Which of the following is\nnot a member of the Beatles?", "options": ["John Lennon", "Paul McCartney", "George Harrison", "Marvin Gaye"],
                 "answer": "Marvin Gaye"},
                 {"question": "Who is the lead singer of the band Coldplay?", "options": ["Chris Martin", "Jonny Buckland", "Guy Berryman", "Will Champion"],
                 "answer": "Chris Martin"},
                 {"question": "Which of the following is\nnot a song by Michael Jackson?", "options": ["Beat It", "Billie Jean", "Thriller", "Like a Virgin"],
                 "answer": "Like a Virgin"},
                 {"question": "Who is the lead singer of the band Queen?", "options": ["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"],
                 "answer": "Freddie Mercury"},
                 {"question": "Which of the following is not a song by Elvis Presley?", "options": ["Jailhouse Rock", "Hound Dog", "Blue Suede Shoes", "Imagine"],
                 "answer": "Whitney Houston"},
                 {"question": "Who sang the song “I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Imagine"},
                 {"question": "Who is the lead singer of the band U2?", "options": ["Bono", "The Edge", "Adam Clayton", "Larry Mullen Jr."],
                 "answer": "Bono"},
                 {"question": "Which of the following\nis not a song by The Rolling Stones?", "options": ["Satisfaction", "Paint It Black", "Brown Sugar", "Stairway to Heaven"],
                 "answer": "Stairway to Heaven"},
                 {"question": "Who is the lead singer of the band Led Zeppelin?", "options": ["Robert Plant", "Jimmy Page", "John Paul Jones", "John Bonham"],
                 "answer": "Robert Plant"},
                 {"question": "Who sang the song “I Wanna Dance with Somebody?", "options": ["Whitney Houston", "Madonna", "Cyndi Lauper", "Tina Turner"],
                 "answer": "Whitney Houston"},
                 {"question": "Who is the lead singer of the band Led Zeppelin?", "options": ["Robert Plant", "Jimmy Page", "John Paul Jones", "John Bonham"],
                 "answer": "Robert Plant"},
                 {"question": "Which of the following is not a song by The Beatles?", "options": ["Hey Jude", "Let It Be", "Imagine", "Yesterday"],
                 "answer": "Hey Jude"},
                 {"question": "Who is the lead singer of the band Pink Floyd?", "options": ["David Gilmour", "Roger Waters", "Syd Barrett", "Nick Mason"],
                 "answer": "Syd Barrett"},
                 {"question": "Who is the lead singer of the band Aerosmith?", "options": ["Steven Tyler", "Joe Perry", "Brad Whitford", "Tom Hamilton"],
                 "answer": "Steven Tyler"},
                 {"question": " Which of the following is not a song by The Doors?", "options": ["Riders on the Storm", "Light My Fire", "Break on Through", "Love Me Tender"],
                 "answer": "Love Me Tender"},
                 {"question": "Who is the lead singer of the band Guns N’ Roses?", "options": ["Axl Rose", "Slash", "Duff McKagan", "Izzy Stradlin "],
                 "answer": "Axl Rose"},
                 {"question": "Which of the following is not a song by Nirvana?", "options": ["Smells Like Teen Spirit", "Marvine Gaye", "Lithium", "Heart-Shaped Box", "John Bonham"],
                 "answer": "Marvine Gaye"},
                 {"question": "Who is the lead singer of the band Red Hot Chili Peppers?", "options": ["Anthony Kiedis", "Flea", "Chad Smith", "John Frusciante"],
                 "answer": "Anthony Kiedis"},
                 {"question": "Which of the following is not a song by The Who?", "options": ["Baba O’Riley", "Pinball Wizard", "Won’t Get Fooled Again", "Jumpin’ Jack Flash"],
                 "answer": "Jumpin’ Jack Flash"},
                 {"question": "Who is the lead singer of the band Van Halen?", "options": ["David Lee Roth", "Eddie Van Halen", "Alex Van Halen", "Michael Anthony"],
                 "answer": "David Lee Roth"},
                 {"question": "Which of the following is not a song by AC/DC?", "options": ["Back in Black", "Thunderstruck", "Highway to Hell", "Sweet Child O’ Mine"],
                 "answer": "Sweet Child O’ Mine"},
                 {"question": "Who is the lead singer of the band Pearl Jam?", "options": ["Eddie Vedder", "Stone Gossard", "Jeff Ament", "Mike McCready"],
                 "answer": "Eddie Vedder"},
                 {"question": "Which of the following is not a song by Pink Floyd?", "options": ["Another Brick in the Wall", "Comfortably Numb", "Time", "Money"],
                 "answer": "Time"},
                 {"question": " What singer has had a Billboard No. 1 hit in each of\nthe last four decades?", "options": ["The Rolling Stones", "Mariah Carey", "Pink Floyd", "Led Zeppelin"],
                 "answer": "Mariah Carey"},
                 {"question": "Who was the very first American Idol winner?", "options": ["Eddie Vedder", "Stone Gossard", "Jeff Ament", "Kelly Clarkson"],
                 "answer": "Kelly Clarkson"},
                 {"question": "Before Bleachers and fun., Jack Antonoff fronted what band?", "options": ["Steel Train", "Thunderstruck", "Highway to Hell", "Sweet Child O’ Mine"],
                 "answer": "Steel Train"},
                 {"question": "Before Miley Cyrus recorded Wrecking Ball\nit was offered to which singer?", "options": ["Axl Rose", "Slash", "Beyoncé", "Izzy Stradlin"],
                 "answer": "Beyoncé"},
                 {"question": "Which artist's entire 1985 Live Aid\nset consisted of just a single cover song?", "options": ["Elvis Costello", "Brian Adams", "Roger Taylor", "John Deacon"],
                 "answer": "Brian Adams"},
                 {"question": "What rock icon was the founder of The Society\nfor the Prevention of Cruelty to Long-haired Men?", "options": ["Anthony Kiedis", "David Bowie", "Chad Smith", "John Frusciante"],
                 "answer": "David Bowie"},
                 {"question": "Keith Moon and John Entwistle of The Who are said to\nhave inspired the name of which other classic rock band?", "options": ["Anthony Kiedis", "David Bowie", "Led Zeppelin", "John Frusciante"],
                 "answer": "Led Zeppelin"},
                 {"question": "Before Phil Collins, who was the lead singer of Genesis?", "options": ["Don McLean", "Bob Dylan", "Neil Young", "Peter Gabriel"],
                 "answer": "Peter Gabriel"},
                 {"question": "Who was Marvin Gaye's duet partner?", "options": ["Tammi Terrell", "Paul McCartney", "George Harrison", "Ringo Starr"],
                 "answer": "Tammi Terrell"},
                 {"question": "Who was the first woman ever inducted into the\nRock and Roll Hall of Fame?", "options": ["Don McLean", "Aretha Franklin", "Neil Young", "Peter Gabriel"],
                 "answer": "Aretha Franklin"},
                 {"question": "Who replaced Ozzy Osbourne as Black Sabbath’s lead singer?", "options": ["Ronnie James Dio", "Judas Priest", "Dokken", "Whitesnake"],
                 "answer": "Ronnie James Dio"},
                 {"question": "To consider a band as a Big Band, what is\nthe minimum number of musicians needed?", "options": [" 11", "21", "12", "10"],
                 "answer": "10"},
                 {"question": "Bjork was the lead singer of what\nIcelandic band before pursuing a solo career?", "options": ["Kukl", "The Sugarcubes", "Cocteau Twins", "The Elgar sisters"],
                 "answer": "The Sugarcubes"},
                 {"question": " In an Orchestra, which is the largest brass section instrument?", "options": ["Trumpet", "Tenor", "French horns", "Tuba"],
                 "answer": "Tuba"},
                 {"question": "Who released the album Alf?", "options": ["Alison Moyet", "Aretha Louise Franklin", "Michael Joseph Jackson", "Christopher Maurice"],
                 "answer": "Alison Moyet"},
                 {"question": "Who released the album Here, My Dear?", "options": ["Frankie Gaye", "Bruno Mars", "Elton John", "Marvin Gaye"],
                 "answer": "Marvin Gaye"},
                 {"question": "Which classical composer was deaf?", "options": ["Frankie Gaye", "Ludwig van Beethoven", "Elton John", "Marvin Gaye"],
                 "answer": "Ludwig van Beethoven"},
                 {"question": "A tribute to David Bowie’s ex-wife was given\nwith a song by The Rolling Stones, name the song?", "options": ["Wild Horses", "Gimme Shelter", "Angie", "Satisfaction"],
                 "answer": "Angie"},
                 {"question": "Who was the blues great born Ellas Otha Bates?", "options": ["Little Richard", "Muddy Waters", "Bo Diddley", "Chuck Berry"],
                 "answer": "Bo Diddley"},
                 {"question": "Which band has its name after a\nscientist from the movie Barbarella?", "options": ["Duran Duran", "A Ha", "Nile Rodgers", "Tears for fears"],
                 "answer": "Duran Duran"},
                 {"question": "Name the orchestral instrument that can play high notes?", "options": ["Viola", "Piccolo", "Violin", "Cellos"],
                 "answer": "Piccolo"},
                 {"question": "What is the all-time bestselling movie soundtrack?", "options": ["I have nothing", "My love is your love", "Waiting to exhale", "The Bodyguard: Original Soundtrack Album"],
                 "answer": "The Bodyguard: Original Soundtrack Album"},
                {"question": "What is the most played song on American\nradio during the 20th century?", "options": ["You’ve Lost That Loving Feeling", "Just Once in My Life", "Danger Zone", "Soul and Inspiration"],
                 "answer": "You’ve Lost That Loving Feeling"},
                {"question": "Who was the musical director of the\nNew York Philharmonic from 1958 to 1970?", "options": ["Jaap Van Zweden", "Alan Gilbert", "Leonard Bernstein", "Kurt Masur"],
                 "answer": "Leonard Bernstein"},
                {"question": "The Clawhammer is a playing style\nassociated with which instrument?", "options": ["Ukulele", "Banjo", "Mandolin", "Fiddle"],
                 "answer": "Banjo"},
                {"question": "Who won the 2001 Grammy Award for Best New Artist?", "options": ["Sam Smith", "Amy Winehouse", "Meghan Trainor", "Alicia Keys"],
                 "answer": "Alicia Keys"},
                {"question": "Who recorded Groove is in the Heart?", "options": ["Q-Tip", "Deee-Lite", "Technotronic", "The B-52’s"],
                 "answer": "Deee-Lite"},
                {"question": "Who is the lead singer of Evanescence?", "options": ["Jen Majura", "Lzzy Hale", "Ben Moody", "Amy Lee"],
                 "answer": "Amy Lee"},
                {"question": "Which musical group had the 1967 Top 10 single,\nI Think We’re Alone Now?", "options": ["The Beatles", "The Monkees", "The Turtles", "Tommy James and the Shondells"],
                 "answer": "Tommy James and the Shondells"},
                {"question": "Who wrote the musical composition Rhapsody in Blue?", "options": ["Leonard Bernstein", "Cole Porter", "Claude Debussy", "George Gershwin"],
                 "answer": "Tommy James and the Shondells"},
            ]
            random.shuffle(self.topics)
        
        elif self.topic == "History":
            self.topics = [
                {"question": "  In which year did the French Revolution begin?", "options": ["1776", "1789", " 1804", "1820"],
                 "answer": " 1789"},
                {"question": " Who was the first President of the United States?", "options": ["Thomas Jefferson", " John Adams", "George Washington", " James Madison"],
                 "answer": "George Washington"},
                {"question": "The Magna Carta, signed in 1215, limited\nthe power of which monarch?", "options": ["Henry VIII", " Richard the Lionheart", " John I", "Edward I"],
                 "answer": "John I"},
                {"question": "Which ancient civilization built the city of Machu Picchu?", "options": ["Mayans", "Aztecs", " Incas", " Egyptians"],
                 "answer": " Incas"},
                {"question": "The Battle of Waterloo took place in which year?", "options": ["1805", "1815", " 1820", " 1835"],
                 "answer": "1815"},
                {"question": "Who wrote The Communist Manifesto \nalongside Karl Marx?", "options": ["Friedrich Engels", " Vladimir Lenin", "  Attack on Pearl Harbo", "  D-Day"],
                 "answer": "Friedrich Engels"},
                {"question": "What event marked the beginning of\nWorld War II in Europe?", "options": ["Invasion of Poland", " Battle of Britain", " John I", "Edward I"],
                 "answer": "Invasion of Poland"},
                {"question": "The Renaissance originated in which Italian city?", "options": [" Florence", "  Rome", "  Venice", "Milan"],
                 "answer": " Florence"},
                {"question": "Who was the first woman to win a Nobel Prize and\nremains the only person to win Nobel Prizes\nin two different scientific fields?", "options": ["Marie Curie", " Rosalind Franklin", " Jane Goodall", "Dorothy Crowfoot Hodgkin"],
                 "answer": "Marie Curie"},
                {"question": "The Boston Tea Party occurred in protest\nof which British taxation policy?", "options": [" Stamp Act", " Sugar Act", " Townshend Acts", "Tea Act"],
                 "answer": "Tea Act"},
                {"question": " In which year did Christopher Columbus\nfirst reach the Americas?", "options": ["1492", "  1500", " 1510", "1525"],
                 "answer": "1492"},
                {"question": "Who was the leader of the Soviet Union\nduring the Cuban Missile Crisis?", "options": ["Joseph Stalin", "  Nikita Khrushchev", " Leon Trotsky", " Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Opium Wars involved conflicts between\nChina and which European power?", "options": [" France", "   Britain", "Spain", "Portugal"],
                 "answer": "Britain"},
                {"question": " The Treaty of Versailles officially\nended which major conflict?", "options": [" World War I", " World War II", " Korean War", " Vietnam War"],
                 "answer": "World War I"},
                {"question": "Who was the primary author of the\nDeclaration of Independence?", "options": ["George Washington", " Thomas Jefferson", " John Adams", "Benjamin Franklin"],
                 "answer": "Thomas Jefferson"},
                {"question": "The Battle of Gettysburg was a significant\nengagement during which war?", "options": [" American Revolution", "Civil War", "  War of 1812", " Spanish-American War"],
                 "answer": "Civil War"},
                {"question": "The Industrial Revolution began\nin which country?", "options": [" France", " Germany", " Britain", " United States"],
                 "answer": " Britain"},
                {"question": "What is the historical period known\nfor the revival of art, literature, and\nlearning in Europe, lasting from the 14th\nto the 17th century?", "options": ["Middle Ages", " Renaissance", " Enlightenment", "Baroque Era"],
                 "answer": "Renaissance"},
                {"question":  "The Great Depression, a severe\nworldwide economic downturn, started\nin which decade?", "options": ["1910s", " 1920s", " 1930s", "1940s"],
                 "answer": " 1930s"},
                {"question": "Who was the Egyptian queen famous for\nher relationships with Julius Caesar\nand Mark Antony?", "options": ["Nefertiti", " Hatshepsut", "Cleopatra", " Ramses II"],
                 "answer": "Cleopatra"},
                {"question": "The Treaty of Ghent, signed in 1814,\nended which conflict between the\nUnited States and Britain?", "options": [" Revolutionary War", "  War of 1812", " Civil War", " French and Indian War"],
                 "answer": " War of 1812"},
                {"question": "Who was the founder of the Mongol\nEmpire in the 13th century?", "options": ["Genghis Khan", " Kublai Khan", " Attila the Hun", "Tamerlane"],
                 "answer": "Genghis Khan"},
                {"question": "What ancient wonder was a massive\ntomb built for an Indian emperor's wife in\nthe 17th century BCE?", "options": ["Great Pyramid of Giza", " Hanging Gardens of Babylon", "  Taj Mahal", "Mausoleum at Halicarnassus"],
                 "answer": "Taj Mahal"},
                {"question": "The Emancipation Proclamation, issued by\nPresident Abraham Lincoln during the American\nCivil War, declared the freedom of slaves\nin which region?", "options": [" Northern states", " Western states", " Southern states", "Eastern states"],
                 "answer": "Southern states"},
                {"question": "The Treaty of Tordesillas, signed in 1494,\ndivided newly discovered lands between\nwhich two European powers?", "options": ["Spain and Portugal", "France and England", "  England and Portugal", "Spain and France"],
                 "answer": " Spain and Portugal"},
                {"question": "The Battle of Stalingrad was a\nturning point in which conflict?", "options": ["World War I", "  Russian Revolution", " World War II", "Cold War"],
                 "answer": " World War I"},
                {"question": " What ancient civilization is known for\nbuilding the city of Troy?", "options": ["Greek", "  Roman", "  Persian", "Hittite"],
                 "answer": "Hittite"},
                {"question": "The Louisiana Purchase, a land deal\nin 1803, involved the United States purchasing\nterritory from which country?", "options": [" Spain", " France", " Britain", "Mexico"],
                 "answer": " France"},
                {"question": "Who was the leader of the Soviet\nUnion during the Cuban Missile Crisis?", "options": ["Joseph Stalin", " Nikita Khrushchev", " Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Boxer Rebellion, a violent anti-foreigner\nand anti-Christian uprising, took place\nin which country?", "options": [" China", " Japan", "India", " Korea"],
                 "answer": "China"},
                {"question": "What famous speech did Martin Luther King Jr.\ndeliver in 1963 during the March on\nWashington for Jobs and Freedom?", "options": ["I Have a Dream", " Give Me Liberty or Give Me Death", " The Gettysburg Address", "We Shall Overcome"],
                 "answer": "I Have a Dream"},
                {"question": " The Treaty of Paris (1763) ended\nwhich conflict between European powers?", "options": ["Napoleonic Wars", " Seven Years' War", "Franco-Prussian War", " Thirty Years' War"],
                 "answer": "Seven Years' War"},
                {"question": "Who was the first female Prime\nMinister of the United Kingdom?", "options": ["Angela Merkel", " Margaret Thatcher", " Theresa May", " Indira Gandhi"],
                 "answer": " Margaret Thatcher"},
                {"question": "What event marked the beginning of\nthe Protestant Reformation in the\nearly 16th century?", "options": ["Council of Trent", " Diet of Worms", " Peace of Augsburg", "Ninety-Five Theses"],
                 "answer": "Ninety-Five Theses"},
                {"question": " The Berlin Wall, which divided East\nand West Berlin during the Cold War,\nfell in which year?", "options": [" 1989", " 1991", " 1985", "1975"],
                 "answer": "1975"},
                {"question": "Who was the leader of the Bolshevik Party\nduring the Russian Revolution of 1917?", "options": ["Vladimir Lenin", "Joseph Stalin", "  Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": " Vladimir Lenin"},
                {"question": "The Treaty of Westphalia, signed in\n1648, ended which prolonged conflict in Europe?", "options": ["Hundred Years' War", " Thirty Years' War", " War of the Roses", "Wars of the Roses"],
                 "answer": "Thirty Years' War"},
                {"question": "The Battle of Saratoga, a pivotal engagement\nduring the American Revolution, occurred in which year?", "options": ["1763", "  1776", "1781", " 1777"],
                 "answer": " 1777"},
                {"question": " The Trail of Tears refers to the\nforced relocation of which Native American tribe\nin the 1830s?", "options": [ "Apache", " Cherokee", "Sioux", " Navajo"],
                 "answer": "Cherokee"},
                {"question": "Who was the primary author of 'The Prince',\na political treatise on leadership and governance?", "options": ["Niccolò Machiavelli", " Thomas More", " John Locke", "Voltaire"],
                 "answer": "Niccolò Machiavelli"},
                {"question": "The Battle of Midway, a decisive naval\nbattle in the Pacific during World War II,\ntook place in which year?", "options": ["1941", " 1942", " 1944", "1945"],
                 "answer": " 1942"},
                {"question": "Who was the first Emperor of China\nand the founder of the Qin Dynasty?", "options": ["Confucius", "  Sun Tzu", " Qin Shi Huang", "Han Wudi"],
                 "answer": " Qin Shi Huang"},
                {"question": "T The Ottoman Empire was centered\naround which city?", "options": [" Istanbul", " Cairo", " Baghdad", " Tehran"],
                 "answer": " Tehran"},
                {"question": "The Battle of Hastings in 1066 led to\nthe Norman conquest of which country?", "options": [" France", " England", " Scotland", " Ireland"],
                 "answer": "England"},
                {"question": "Who was the Roman general and statesman\nresponsible for the conquest of Gaul and\nlater became dictator for life?", "options": ["Julius Caesar", "Augustus Caesar", " Mark Antony", "Cicero"],
                 "answer": " Julius Caesar"},
                {"question": "The Indian independence movement, led by Mahatma\nGandhi, called for nonviolent resistance\nagainst which colonial power?", "options": ["France", " Britain", " Spain", "Portugal"],
                 "answer": " Britain"},
                {"question": "The Treaty of Nanking, signed in 1842,\nmarked the end of which conflict between\nChina and Britain?", "options": [" Opium Wars", " Boxer Rebellion", " Taiping Rebellion", " Sino-Japanese War"],
                 "answer": "Opium Wars"},
                {"question": "The Apollo 11 mission, in 1969,\nsuccessfully landed the first humans on\nwhich celestial body?", "options": ["Mars", "Venus", " Moon", "Jupiter"],
                 "answer": "Moon"},
                {"question": "The Monroe Doctrine, articulated in 1823,\nwarned against European intervention in the\naffairs of which region?", "options": ["Asia", " Africa", " Europe", "Americas"],
                 "answer": "Americas"},
                {"question": "Who was the leader of the Soviet Union during the Cuban Missile Crisis?", "options": [" Joseph Stalin", "  Nikita Khrushchev", " Leon Trotsky", "Mikhail Gorbachev"],
                 "answer": "Nikita Khrushchev"},
                {"question": " The Battle of Stalingrad was a turning\npoint in which conflict?", "options": ["World War I", "  Russian Revolution", " World War II", "Cold War"],
                 "answer": "World War II"},
                {"question": "What ancient civilization is known\nfor building the city of Troy?", "options": ["Greek", " Roman", " Persian", " Hittite"],
                 "answer": " Hittite"},
                {"question": "The Louisiana Purchase, a land deal in 1803,\ninvolved the United States purchasing territory\nfrom which country?", "options": ["Spain", " France", "  Britain", "Mexico"],
                 "answer": "France"},
                {"question": " Who was the leader of the Bolshevik Party\nduring the Russian Revolution of 1917?", "options": [" Vladimir Lenin", "  Joseph Stalin", " Leon Trotsky", " Mikhail Gorbachev"],
                 "answer": " Vladimir Lenin"},
                {"question": "Who was the first President of the\nUnited States?", "options": ["Thomas Jefferson", " George Washington", "John Adams", "James Madison"],
                 "answer": "George Washington"},
                {"question": "In which year did Christopher Columbus reach the Americas?", "options": [" 1492", "  1512", " 1607", " 1620"],
                 "answer": " 1492"},
                {"question": "The Battle of Gettysburg was a significant\nbattle during which war?", "options": ["World War I", " American Civil War", " Revolutionary War", "War of 1812"],
                 "answer": "American Civil War"},
                {"question": "Who was the first woman to win a Nobel Prize?", "options": [" Marie Curie", " Amelia Earhart", " Florence Nightingale", "Rosa Parks"],
                 "answer": "Marie Curie"},
                {"question": "What ancient wonder of the world was located in Egypt?", "options": ["Colossus of Rhodes", " Hanging Gardens of Babylon", " Great Pyramid of Giza", "Statue of Zeus at Olympia"],
                 "answer": "Great Pyramid of Giza"},
                {"question": "Who was the leader of the Soviet Union\nduring World War II?", "options": [" Vladimir Lenin", " Joseph Stalin", " Nikita Khrushchev", "Mikhail Gorbachev"],
                 "answer": "Joseph Stalin"},
                {"question": "The Magna Carta, signed in 1215, is considered\na cornerstone of which concept?", "options": ["Democracy", " Communism", " Feudalism", " Absolute monarchy"],
                 "answer":"Democracy"},
                {"question": " The Renaissance originated in\nwhich European city?", "options": [" Paris", " Rome", " Athens", " Florence"],
                 "answer": "Florence"},
                {"question": " What event marked the beginning of\nWorld War I?", "options": [" Assassination of Archduke Franz Ferdinand", " Invasion of Poland", "  Treaty of Versailles", "Battle of the Somme"],
                 "answer": " Assassination of Archduke Franz Ferdinand"},
                {"question": "Who wrote 'The Communist Manifesto' with Karl Marx?", "options": ["Friedrich Engels", "Vladimir Lenin", " Leon Trotsky", "Mao Zedong"],
                 "answer": "Friedrich Engels"},
                {"question": "Which ancient civilization built the city of Machu Picchu?", "options": [" Mayans", " Egyptians", "  Greeks", " Incas"],
                 "answer": " Incas"},
                {"question": "The Battle of Waterloo took place during which war?", "options": ["Napoleonic Wars", " American Civil War", "  World War I", " Hundred Years' War"],
                 "answer": "Napoleonic Wars"},
                {"question": "Who was the first Emperor of China,\nknown for the Terracotta Army?", "options": ["Qin Shi Huang", "Han Wudi", " Emperor Wu", "Confucius"],
                 "answer": "Qin Shi Huang"},
                {"question": "The Renaissance is often described as\nthe rebirth of what?", "options": ["Art and culture", "  Feudalism", " Monarchy", "Religious orthodoxy"],
                 "answer": "Art and culture"},
                {"question": "The Bubonic Plague, also known as the\nBlack Death, originated in which continent?", "options": ["Asia", " Africa", "  Europe", "North America"],
                 "answer": "Europe"},
                {"question": "Who was the primary author of the Declaration\nof Independence in the United States?", "options": [" Thomas Jefferson", " John Adams", "Benjamin Franklin", " George Washington"],
                 "answer": "Thomas Jefferson"},
                {"question": "The Treaty of Versailles marked the\nend of which conflict?", "options": ["World War I", "  World War II", " Korean War", "Vietnam War"],
                 "answer": "World War I"},
                {"question": "Which ancient civilization is known for creating\nthe first written language, cuneiform?", "options": ["Egyptians", " Sumerians", "  Greeks", "Romans"],
                 "answer": " Sumerians"},
                {"question": "The French Revolution began in which year?", "options": [" 1776", "  1789", " 1812", "1848"],
                 "answer": "1789"},
                {"question": "Who was the first woman to fly solo\nacross the Atlantic Ocean?", "options": [" Amelia Earhart", " Bessie Coleman", "  Harriet Quimby", " Jacqueline Cochran"],
                 "answer": " Amelia Earhart"},
                {"question": "The Great Wall of China was built to protect\nagainst invasions from which group?", "options": [" Mongols", " Huns", " Vikings", "Persians"],
                 "answer": " Mongols"},
                {"question": "The Industrial Revolution began in which country?", "options": ["England", " France", " Germany", "United States"],
                 "answer": "England"},
                {"question": "Who was the leader of the Soviet Union\nduring the Cuban Missile Crisis?", "options": ["Vladimir Putin", "Leon Trotsky", "Nikita Khrushchev", " Joseph Stalin"],
                 "answer": "Nikita Khrushchev"},
                {"question": "The Emancipation Proclamation, issued\nby Abraham Lincoln, aimed to free slaves\nduring which conflict?", "options": ["American Revolution", " American Civil War", "  War of 1812", "Spanish-American War"],
                 "answer": "American Civil War"},
                {"question": " What ancient city was home to the\nfamous Hanging Gardens?", "options": ["Rome", " Athens", "Babylon", "Alexandria"],
                 "answer": "Babylon"},
                {"question": "Who was the first woman to win a\nNobel Prize for Peace?", "options": ["Marie Curie", "Mother Teresa", "Aung San Suu Kyi", "Bertha von Suttner"],
                 "answer": "Bertha von Suttner"},
                {"question": "The Battle of Stalingrad was a major\nturning point in which conflict?", "options": ["World War I", " World War II", " Korean War", "Vietnam War"],
                 "answer": "World War II"},
                {"question": " The Marshall Plan was designed to aid\nthe economic recovery of which continent\nafter World War II?", "options": ["North America", " Europe", " Asia", "Africa"],
                 "answer": "Europe"},
                {"question": "Who was the longest-reigning monarch\nin British history?", "options": ["Queen Elizabeth II", " Queen Victoria", " King George III", "King Henry VII"],
                 "answer": " Queen Victoria"},
                {"question": "The Treaty of Brest-Litovsk marked the end\nof Russia's involvement in which conflict?", "options": ["World War I", "Russian Revolution", " Napoleonic Wars", "Crimean War"],
                 "answer": "World War I"},
                {"question": "The Berlin Wall was built to divide which\ncity during the Cold War?", "options": ["Paris", "Rome", "  Berlin", " Vienna"],
                 "answer": "Berlin"},
                {"question": "Who was the leader of the Mongol\nEmpire during its peak?", "options": ["Genghis Khan", "Kublai Khan", "  Attila the Hun", "Tamerlane"],
                 "answer": "Genghis Khan"},
                {"question": "The signing of the Magna Carta in 1215\nwas a significant event in the history\nof which country?", "options": [" France", "England", "Spain", "Italy"],
                 "answer": "England"},
                {"question": "The Treaty of Tordesillas, signed in 1494,\ndivided newly discovered lands between\nwhich two countries?", "options": ["Spain and Portugal", " England and France", " Italy and Germany", "Netherlands and Belgium"],
                 "answer": "Spain and Portugal"},
                {"question": "The Opium Wars were fought between\nChina and which European power?", "options": ["France", "Spain", " Portugal", "Britain"],
                 "answer": "Britain"},
                {"question": "Who was the first woman to serve as\nPrime Minister of the United Kingdom?", "options": ["Margaret Thatcher", "Theresa May", " Angela Merkel", " Indira Gandhi"],
                 "answer": " Indira Gandhi"},
                {"question": "The Russian Revolution of 1917 led to the\nestablishment of which government?", "options": ["Constitutional monarchy", "  Absolute monarchy", " Communist government", " Parliamentary democracy"],
                 "answer": " Communist government"},
                {"question": "The Battle of Saratoga, a crucial turning\npoint in the American Revolution, occurred\nin which year?", "options": ["1763", " 1776", "1781", " 1777"],
                 "answer": " 1777"},
                {"question": "Who was the first Emperor of Rome?", "options": [" Julius Caesar", " Augustus", "  Nero", "Caligula"],
                 "answer": "Augustus"},
                {"question": "The Boxer Rebellion took place in which\ncountry during the late 19th century?", "options": [" Japan", " China", "  India", " Korea"],
                 "answer": " China"},
                {"question": " The Treaty of Ghent, signed in 1814,\nended which conflict?", "options": ["American Revolution", " War of 1812", "  French Revolution", "Napoleonic Wars"],
                 "answer": "War of 1812"},
                {"question": "The Zimmermann Telegram, intercepted during\nWorld War I, revealed a secret alliance\nbetween Germany and which country?", "options": ["Russia", " Mexico", " Japan", " Italy"],
                 "answer": "Mexico"},
                {"question": "The Battle of Midway, a pivotal naval battle\nin World War II, involved which two countries?", "options": ["United States and Japan", " Germany and Soviet Union", "  Britain and Italy", "France and China"],
                 "answer": "United States and Japan"},
                {"question": " The Treaty of Nanking, signed in 1842,\nmarked the end of hostilities in which conflict?", "options": [" Opium Wars", "  Crimean War", " Franco-Prussian War", "Spanish-American War"],
                 "answer": "Opium Wars"},
                {"question": "Who was the last Pharaoh of Ancient Egypt?", "options": ["Cleopatra VII", " Ramses II", "  Tutankhamun", "Hatshepsut"],
                 "answer": "Cleopatra VII"},
                {"question": " The Treaty of Kanagawa, signed in 1854,\nopened trade relations between Japan and\nwhich country?", "options": ["China", " United States", "  Britain", "Russia"],
                 "answer": "United States"},
            ]
            random.shuffle(self.topics)
            
        elif self.topic == "Biology":
            self.topics = [  
                {"question": "What is the primary function of the ribosomes in a cell?", "options": ["Energy production", "protein systhesis", "", "",],
                 "answer": "Protein systhesis"},
                {"question": "In which organelle does cellular respiration occur?", "options": ["nucleus", "chloroplast", "Mitochondrion", "endoplasmic reticulum"],
                 "answer": "Mitochondrion"},
                {"question": "what is the function of the enzyme amylase", "options": ["break down proteins", "break down lipids","break down carbohydrates", "synthesize DNA"],
                 "answer": "break down carbohydrates"},
                {"question": "Which gas is produced during photosysthesis", "options": ["oxygen", "carbon dioxide", "nitrogen", "hydrogen"],
                 "answer": "oxygen"},
                {"question": "what is the role of galgi apparatus in the cell?", "options": ["energy production", "protein synthesis", "pakaging and modifying proteins", "photosynthesis"],
                 "answer": "pakaging and modifying proteins"},
                {"question": "which of the following is a characteristric of eukaryotic cells?", "options": ["lack of nucleus", "circular DNA", "membrane bound organelles", "small size"],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the cell membrane?", "options": ["energy production", "support and structure", "regulation of substances entering and leaving the cell", "protein synthesis"],
                 "answer": "regulation of substances entering and leaving the cell"},
                {"question": "which of the following is a nitrogeus base in a DNA?", "options": ["adenine", "guanine", "thymine", "all of the above"],
                 "answer": "all of the above"},
                {"question": "what is the purpose of mitosis in cell division?", "options": ["production of gametes", "growth and repair of body cells", "membrane bound organelles", "endoplasmic reticulum"],
                 "answer": "growth and repair of body cells"},
                {"question": "what is the function of the chloroplast in plant cells?", "options": ["energy production", "protein synthesis", "photosynthesis", "lipid synthesis"],
                 "answer": "photosynthesis"},
                {"question": "which of the following is a type of white blood cell involved to immune response?", "options": ["eosonophil", "neutronphil", "basophil", "monacyte"],
                 "answer": "eosonophil"},
                {"question": "what is the main function of the pancreas in digestion?", "options": ["producing pile", "producing insulin and enzymes for digestion", "absorbing nutrients", "storing gyclogen"],
                 "answer": "producing insulin and enzymes for digestion"},
                {"question": "in humams, where does fertilazion typically occur?", "options": ["ovary", "uterus", "fallopian tube", "cervix"],
                 "answer": "fallopian tube"},
                {"question": "which of the following is a function of the nervous system?", "options": ["transporting oxygen", "regulating body temperature", "transmitting electric signals", "producing hormones"],
                 "answer": "transmitting electric signals"},
                {"question": "what is the purpose of the lymphatic system?", "options": ["pumping blood", "fighting infection and transportting fluids", "digesting foods", "producing antibioties"],
                 "answer": "fighting infection and transportting fluids"},
                {"question": "what is the role od RNA in protein synthesis?", "options": ["carries amino acids to the ribosomes", "provides energy for the process", "acts as a structural component of ribosomes", "carries genetic information to DNA to ribosomes"],
                 "answer": "carries genetic information to DNA to ribosomes"},
                {"question": "which of the following is a function of the skeletal system?", "options": ["producing hormones", "providing supports and protection", "digesting food", "regulating blood pressure"],
                 "answer": "providing support and protection"},
                {"question": "what is the name of the process by which cells specialize into different cell types?", "options": ["mitosis", "meiosis", "differentiation", "replication"],
                 "answer": "differentiation"},
                {"question": "what is the purpose of the enzymes DNA polymerase?", "options": ["transcription", "translation", "DNA replication", "protein synthesis"],
                 "answer": "DNA replication"},
                {"question":"what is the function of the ednoplasmic reticulum (ER) in a cell?", "options": ["synthesizing lipids", "modifying and packaging proteins", "producing atp", "staring genetic information"],
                 "answer": "modifying and packaging problems"},
                {"question":"which of the following is an example of a passive transport process in cell?", "options": ["facilatated diffusion", "active transport", "endocytosis", "exocytosis"],
                 "answer": "facilatated diffusion"},
                {"question": "wwhat is the role of thymuys gland in the immune system?", "options": ["producing insulin", "maturation of T lymphocytes (T cells)", "filtering blood", "producing antibodies"],
                 "answer": "maturation T lymphocates (T cells)"},
                {"question": "which of the following is a function of kidney?", "options": ["regulation of blood pressure", "production of red blood cells", "digestion of proteins", "storage of urines"],
                 "answer": "regulation of blood pressure"},
                {"question": "what is the purpose of krebs cycle in cellular respiration?", "options": ["production of ATP", "oxidation of glucose", "breakdown of pyruvate to generate energy", "synthesis of glucose"],
                 "answer": "breakdown of pyruvate to generate energy"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "what is the primary role of the hemoglobin in red blood cells?", "options": ["carrying oxygen", "fighting infections", "blood clotting", "breaking down toxins"],
                 "answer": "carrying oxygen"},
                {"question": "which of the following is a function of hormone insulin?", "options": ["stimulating glycogen", "increaasing blood sugar levels", "promoting glucose uptake by cells", "inhibating protein synthesis"],
                 "answer": "promoting glucose uptake by cell"},
                {"question": "what is the function of cillia and flagella in cells?", "options": ["protein synthesis", "movement", "energy production", "DNA replication"],
                 "answer": "DNA replication"},
                {"question": "which of the following is a nitregenous base in RNA but not in DNA?", "options": ["adenine", "guanine", "uracil", "thymine"],
                 "answer": "uracil"},
                {"question": "what is the  main function of the e amylase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown carbohydrates"},
                {"question": "in which cellular organelle does photosynthesis occur in plant cells?", "options": ["nucleus", "chloroplast", "mitochondrion", "ednoplasmic reticulum"],
                 "answer": "chloroplast"},
                {"question": "which of the following is a function of the circulatory system?", "options": ["digestion of food", "transport of nutrients and oxygen", "synthesis of hormones", "excreation of waste products"],
                 "answer": "transport of nutrients and oxygen "},
                {"question": "what is the function of the hormone adrenaline in the human body?", "options": ["regulating blood sugar levels", "controlling metabolism", "initiating fight or flight response", "stimulating growth"],
                 "answer": "initiating fight or flight response"},
                {"question": "which of the following is a function pf the skelatal muscles?", "options": ["pumping blood", "providing structural", "contraction for movements", "producing hormones"],
                 "answer": "contraction of movements"},
                {"question": "what is the function of the hormone progerostone in the female reproductive system?", "options": ["stimulating the realese of eggs from the ovaries", "maintaining the uterine lining during pregnancy","regulating blood pressure", "initiatiing milk production"],
                 "answer": "maintinaning the uterine lining during pregnancy"},
                {"question": "which of the following is a function of the respiratory system?", "options": ["producing antibodies", "regulating body temperature", "exchange of oxygen and carbong dioxide", "synthezing glucose"],
                 "answer": "exchange of oxygen and carbon dioxide"},
                {"question": "what is the primary function of the lymph nodes in the immune system?", "options": ["production of antibodies", "filtration of lymph and trapping pathogens", "pumping blood", "digestion fats"],
                 "answer": "filtration of lymph and trapping pathogens"},
                {"question": "in which part of the digestive system does the majority of nutrient absorption take place?", "options": ["stomach", "small intestine", "large intestine", "esophagus"],
                 "answer": "small intestine"},
                {"question": "what is the function of the enzyme lipase?", "options": ["break down proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown lipids"},
                {"question": "what is the primary function of the enzyme pepsin in the stomach?", "options": ["production of pile", "absorption of nutrient", "storage of food", "synthesis of insulin"],
                 "answer": "production of pile"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the hormone insulin in the regulation of blood sugar levels?", "options": ["increase blood sugar levels", "breakdown glucose", "promote glucose uptake by cells", "stimulate the release of glucagon"],
                 "answer": "promote of glucose uptake by cells"},
                {"question": "which type of cell division is rensposible for growth and repair in multi cellular organisms?", "options": ["mitosis", "meitosis", "binary fission", "budding"],
                 "answer": "mitosis"},
                {"question": "in the proccess of transcription what is the role of RNA polymerase?", "options": ["synthesize mRNA from DNA", "synthesize tRNA from DNA", "synthesize DNA from RNA", "synthesize proteins"],
                 "answer": "synthesize mRNA from DNA"},
                {"question": "which of the following is a function of the smooth endoplasmic reticulum?", "options": ["protein synthesizes", "lipid synthesize and detoxification", "modifying and packaging proteins", "energy production"],
                 "answer": "lipid synthesize and detoxification"},
                {"question": "what is the purpose of the nitrogen cycle in ecosystems?", "options": ["carbon fixation", "nitrogen fixiation", "oxygen production", "ATP synthesize"],
                 "answer": "nitrogen fixiation"},
                {"question": "what is the role of the hormone melatonin?", "options": ["regulation of blood sugar levels", "sleep wake cycle and cardian ryhthm", "regulation of body temperature", "stimulating growth"],
                 "answer": "sleep wake cycle and cardian ryhthm"},
                {"question": "which of the following is an example os a symbiotic relationship where both organism benefit?", "options": ["parasitsm", "nutualism", "commensalism", "predation "],
                 "answer": "mutualism"},
                {"question": "in humans, what is the primary function of the epiglottis?", "options": ["taste sensation", "breathing", "speech production", "swalowing "],
                 "answer": "swallowing"},
                {"question": "which of the following is golgi apparatus?", "options": ["protein synthesize", "cellular respiration", "packaging", "photosynthesis"],
                 "answer": "packaging"},
                {"question": "what is the term for the process by which a cell engulfs large particles or other cells?", "options": ["pinocytosis", "phagocytosis", "exocytosis", "osmosis"],
                 "answer": "phagocytosis"},
                {"question": "which of the characteristics of a eukaryotic cell?", "options": ["lack of nucleus", "circullar DNA", "membrane bound organelles", "small size "],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the enzyme catalase in cells?", "options": ["breakdown carbo", "breakdown lipids", "breakdown hydrogen", "synthesize DNA"],
                 "answer": "breakdown hydrogen"},
                {"question": "which of the following is a greenhouse gas contributing gto climate change?", "options": ["oxygen", "nitrogen", "methane", "hydrogen "],
                 "answer": "methane"},
                {"question": "what is the main function of the cornea in the human eye?", "options": ["color vision", "focusing light onto the retina", "light perception", "controlling the amount"],
                 "answer": "focusing light onto the retina"},
                {"question": "in plant cells what structure is responsible for storing water nutrients and waste production?", "options": ["nucleus", "vacuole", "clhoroplast", "ribosome "],
                 "answer": "vacuole"},
                {"question": "wht is the process  by which a catterpillar tranforms into butterfly?", "options": ["metamhorposis", "fission", "budding", "fragmentation"],
                 "answer": "metamorphosis"},
                {"question": "what is the primary function of the cilliary bodybin the human eye?", "options": ["producing tears", "changing the shape", "detecting light", "converting light"],
                 "answer": "changing the shape"},
                {"question": "which of the following is a nitrogen fixing bacterium commmonly \nfound in the root nodules of legumiunsvplants?", "options": ["escherichia coli", "rhzobium", "streptococcus", "bacillus subtilis"],
                 "answer": "rhizobium"},
                {"question": "what is the primary function of the hormones prolactin in females?", "options": ["stimulating milk", "regulating blood sugar", "intiating fight", "controlling metabolism "],
                 "answer": "stimulating milk"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "what is the primary role of the hemoglobin in red blood cells?", "options": ["carrying oxygen", "fighting infections", "blood clotting", "breaking down toxins"],
                 "answer": "carrying oxygen"},
                {"question": "which of the following is a function of hormone insulin?", "options": ["stimulating glycogen", "increaasing blood sugar levels", "promoting glucose uptake by cells", "inhibating protein synthesis"],
                 "answer": "promoting glucose uptake by cell"},
                {"question": "what is the function of cillia and flagella in cells?", "options": ["protein synthesis", "movement", "energy production", "DNA replication"],
                 "answer": "DNA replication"},
                {"question": "which of the following is a nitregenous base in RNA but not in DNA?", "options": ["adenine", "guanine", "uracil", "thymine"],
                 "answer": "uracil"},
                {"question": "what is the  main function of the enzyme amylase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown carbohydrates"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the hormone insulin in the regulation of blood sugar levels?", "options": ["increase blood sugar levels", "breakdown glucose", "promote glucose uptake by cells", "stimulate the release of glucagon"],
                 "answer": "promote of glucose uptake by cells"},
                {"question": "which type of cell division is rensposible for growth and repair in multi cellular organisms?", "options": ["mitosis", "meitosis", "binary fission", "budding"],
                 "answer": "mitosis"},
                {"question": "in which part of the digestive system does the majority of nutrient absorption take place?", "options": ["stomach", "small intestine", "large intestine", "esophagus"],
                 "answer": "small intestine"},
                {"question": "what is the function of the enzyme lipase?", "options": ["break down proteins", "breakdown lipids", "breakdown carbohydrates", "synthesize DNA"],
                 "answer": "breakdown lipids"},
                {"question": "what is the primary function of the enzyme pepsin in the stomach?", "options": ["production of pile", "absorption of nutrient", "storage of food", "synthesis of insulin"],
                 "answer": "production of pile"},
                {"question": "what is the purpose of the calvin cycle in photosynthesis?", "options": ["capture the light energy", "conversion of carbon dioxide to glucose", "breakdown glucose", "generation of ATP"],
                 "answer": "conversion of carbon dioxide to glucose"},
                {"question": "which of the following is an example of a vestigial organ in humans?", "options": ["appendix", "heart", "liver", "lungs"],
                 "answer": "appendix"},
                {"question": "what is the function of the enzyme amylase", "options": ["break down proteins", "break down lipids","break down carbohydrates", "synthesize DNA"],
                 "answer": "break down carbohydrates"},
                {"question": "Which gas is produced during photosysthesis", "options": ["oxygen", "carbon dioxide", "nitrogen", "hydrogen"],
                 "answer": "oxygen"},
                {"question": "what is the role of galgi apparatus in the cell?", "options": ["energy production", "protein synthesis", "pakaging and modifying proteins", "photosynthesis"],
                 "answer": "pakaging and modifying proteins"},
                {"question": "which of the following is a characteristric of eukaryotic cells?", "options": ["lack of nucleus", "circular DNA", "membrane bound organelles", "small size"],
                 "answer": "membrane bound organelles"},
                {"question": "what is the function of the cell membrane?", "options": ["energy production", "support and structure", "regulation of substances entering and leaving the cell", "protein synthesis"],
                 "answer": "regulation of substances entering and leaving the cell"},
                {"question": "which of the following is a nitrogeus base in a DNA?", "options": ["adenine", "guanine", "thymine", "all of the above"],
                 "answer": "all of the above"},
                {"question": "what is the name of the process by which cells specialize into different cell types?", "options": ["mitosis", "meiosis", "differentiation", "replication"],
                 "answer": "differentiation"},
                {"question": "what is the purpose of the enzymes DNA polymerase?", "options": ["transcription", "translation", "DNA replication", "protein synthesis"],
                 "answer": "DNA replication"},
                {"question":"what is the function of the ednoplasmic reticulum (ER) in a cell?", "options": ["synthesizing lipids", "modifying and packaging proteins", "producing atp", "staring genetic information"],
                 "answer": "modifying and packaging problems"},
                {"question":"which of the following is an example of a passive transport process in cell?", "options": ["facilatated diffusion", "active transport", "endocytosis", "exocytosis"],
                 "answer": "facilatated diffusion"},
                {"question": "wwhat is the role of thymuys gland in the immune system?", "options": ["producing insulin", "maturation of T lymphocytes (T cells)", "filtering blood", "producing antibodies"],
                 "answer": "maturation T lymphocates (T cells)"},
                {"question": "which of the following is a function of kidney?", "options": ["regulation of blood pressure", "production of red blood cells", "digestion of proteins", "storage of urines"],
                 "answer": "regulation of blood pressure"},
                {"question": "what is the purpose of krebs cycle in cellular respiration?", "options": ["production of ATP", "oxidation of glucose", "breakdown of pyruvate to generate energy", "synthesis of glucose"],
                 "answer": "breakdown of pyruvate to generate energy"},
                {"question": "which organelle is responsible for detoxifying harmful substances in the cell?", "options": ["peroxisome", "lysosome", "galgi apparatus", "ednoplasmic reticulum"],
                 "answer": "peroxisome"},
                {"question": "in humans where does spermatogenesis occur?", "options": ["ovary", "testes", "uterus", "fallopian tube"],
                 "answer": "testes"},
                {"question": "what is the primary function of the enzyme sucrase?", "options": ["breakdown proteins", "breakdown lipids", "breakdown sucrose", "synthesize DNA"],
                 "answer": "breakdown sucrose"},
                {"question": "in genetics, what is the term for the physical expression of an organism genetic traits?", "options": ["genotype", "phenotype", "allele", "homozygote"],
                 "answer": "phenotype"},
                {"question": "in which part of the human digestive system dooes nutrient absorpotion primarily occur?", "options": ["stomach", "large intestine", "small intestine", "mouth"],
                 "answer": "small intestine"},
                {"question": "which of the following is an example of an exocrine gland in the human boyd?", "options": ["thyroid gland", "pituiry gland", "salivvary gland", "adrenal gland"],
                 "answer": "salivary gland"},
                {"question": "in the context of plant reproduction what is the male reproductive organ called?", "options": ["ovule", "pistl", "stamen", "carpel"],
                 "answer": "stamen"},
                {"question": "in the context of ecology what is the term for the study of the interactions among organism and their envinronment?", "options": ["genetics", "physiology", "ecology", "ethology"],
                 "answer": "ecology"},
                {"question": "which of the following is a nitrogen fixing bacterium commonly found \nin the root nodules of leguminous plants?", "options": ["escherichia coli", "rhizobium", "streptococcus", "bacillis"],
                 "answer": "rhizobium"},
                {"question": "in humans what is the mai function of the kidneys?", "options": ["digestion", "filtration of blood", "respiration", "pumping blood"],
                 "answer": "filtration of blood"},
                {"question": " what is the molecule that carries genetic information for the development and functioning of an organism.?", "options": ["DNA", "RNA", "RMA", "RTA"],
                 "answer":"DNA"},
            ]
            random.shuffle(self.topics)
            
        elif self.topic == "TEST HERE":
            self.topics = [
                {
                    "question": "What is the result of 7 x 9?",
                    "options": ["54", "63", "72","48"],
                    "answer": "63"
                },
                {
                    "question": "If a rectangle has a length of 10 units\nand a width of 5 units, what is its area?",
                    "options": ["20 square units", "30 square units", "40 square units","50 square units"],
                    "answer": "40 square units"
                },
                {
                    "question": "What is the result of (12 ÷ 4) + 5?",
                    "options": ["  7.  ", "  8  ", "  9.  ","  10  "],
                    "answer": "  8  "
                },
            ]
            random.shuffle(self.topics)
        
        # quiz1 frame
        quiz1_frame = tk.Frame(self.root, bg="#2A225A")
        quiz1_frame.pack()
        self.currentFrame = quiz1_frame

        # Score label
        self.score_label = tk.Label(quiz1_frame,
                                    text=f"Score: {self.score}",
                                    padx=20,
                                    bg="black",  # Set the background color for the score label
                                    fg="#4FDD0C",
                                    font=("Comic sans MS", 20, "bold"))
        self.score_label.pack(side=tk.TOP,pady=10,padx=(40))

        # Lives label
        self.lives_label = tk.Label(quiz1_frame,
                                    padx=20,
                                    text=f"Lives: {self.lives}",
                                    bg="black",  # Set the background color for the lives label
                                    fg="#07B9AE",
                                    font=("Comic sans MS", 20, "bold"))
        self.lives_label.pack(side=tk.TOP,padx=(40))

        # Question label
        self.question_label = tk.Label(quiz1_frame,
                                       text=self.topics[self.currentQuestionIndex]["question"],
                                       bg="#2A225A",
                                       fg="white",
                                       font=("Comic sans MS", 20, "bold"))
        self.question_label.pack(pady=40)

        self.player_answer.set("")
        
        # mga variable na ginagamit para i-determine ang laki at
        # porma ng grid kung saan ilalagay ang mga choices ng tanong.
        num_choices = len(self.topics[self.currentQuestionIndex]["options"])
        num_columns = 2
        num_rows = (num_choices + num_columns - 1) // num_columns

        rbs=[]  # list na gagamitin para mapanatili ang references sa bawat Radiobutton na nilikha, upang maging madali ang pag-manage o pag-access sa mga ito.

        choices_frame = tk.Frame(quiz1_frame,bg="#2A225A")
        choices_frame.pack()
          
        # choices can change font color here  
        def select(choice_button):
            choice_button.config(foreground='yellow') # kulay ng answer pag na pili
            for choice_button_ in rbs:
                if choice_button_ != choice_button:
                   choice_button_.config(fg='#F66868') # kapag hindi napili magiging pula matitirang choices
         
         # function para ma arrange ang choices into grid row and column
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < num_choices:
                    
                    # Choices function can change font color here too
                    choice_text = self.topics[self.currentQuestionIndex]["options"][index]
                    choice_button = tk.Radiobutton(choices_frame,
                                                   text=choice_text,
                                                   variable=self.player_answer, # variable Ito ay isang Tkinter variable  na pinagsasanib ang Radiobutton. Sa code, ito ay self.player_answer.
                                                   value=choice_text,   # value: Ito ay ang value na nakatalaga para sa Radiobutton, at dito ginamit ang choice_text.                                             
                                                   background="#2A225A", # violet 
                                                   foreground="orange", # color of texts choices
                                                   activebackground="green",  # color pag kinlick ang napiling sagot                                                                                            
                                                   cursor='hand2',
                                                   font=("Comic sans MS", 20, "bold"))
                    choice_button.config(command=lambda arg=choice_button:select(arg)) # lambda expression ay ginagamit para maipasa ang choice_button bilang argument sa select function.
                    choice_button.grid(row=i, column=j, padx=10, pady=20, sticky="w")
                    rbs.append(choice_button) # adding choice button

        button_frame = tk.Frame(quiz1_frame, bg="#2A225A") # violet                                               
        button_frame.pack(pady=20)
        
        # submit button function
        self.submit_button = tk.Button(button_frame, text=" Submit ",
                                     command=self.submit_button_sound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#990066",
                                     foreground="white",
                                     activebackground="#FF0066",
                                     activeforeground="white",
                                     font=("Comic sans MS",25, "bold"))
        self.submit_button.pack(side=tk.LEFT, padx=25,pady=15)
        
        # save button function
        self.save_button = tk.Button(button_frame, text="  Save  ",
                                     command=self.save_button_sound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#009900",
                                     foreground="white",
                                     activebackground="#00FF00",
                                     activeforeground="white",
                                     font=("Comic sans MS",25, "bold"))                                    
        self.save_button.pack(side=tk.LEFT, padx=25,pady=15)
        
        # Give up button function
        self.back_button = tk.Button(button_frame, text=" Give Up ",
                                     command=self.gameover2_withsound,
                                     padx=10,
                                     border=4,
                                     cursor='hand2',
                                     background="#000066",
                                     foreground="white",
                                     activebackground="#0033CC",
                                     activeforeground="white",
                                     font=("Comic sans MS", 25, "bold"))
        self.back_button.pack(side=tk.LEFT, padx=25,pady=15)
        
    def submit_button_sound(self):
        self.button_music.play()
        self.check_answer()
        
    def save_button_sound(self):
        self.button_music.play()
        self.saved_progress() 
        
    def gameover2_withsound(self):
        self.button_music.play()
        self.give_up()
        

    # validating answers
    def validate_answer(self, *args):
        if self.submit_button and self.submit_button.winfo_exists() and self.player_answer.get():
            self.submit_button.config(state=tk.NORMAL)
    
    # checking answers
    def check_answer(self):
       # checking kung wala pa napipiling sagot at nag submit agad..
        if self.currentQuestionIndex < len(self.topics):
            pick_answer = self.player_answer.get()
            if not pick_answer:
                messagebox.showinfo("Error", "Please select an answer before moving to the next question.")
                return

            correct_answer = self.topics[self.currentQuestionIndex]["answer"]  
            self.player_answers[str(self.currentQuestionIndex)] = pick_answer

            if pick_answer == correct_answer:
                self.score += 1
                self.que_var += 1 # counting the answered questions
                self.correct_sound.play()
            else:
                self.lives -= 1
                self.wrong_var += 1
                self.que_var += 1 # counting the answered questions
                
                if self.lives <= 0: # if life is lessthan zero -
                    self.game_over(self.calculated_iq,self.score,self.wrong_var,self.que_var) # - run game_over frame
                    return
                self.wrong_sound.play()
                time.sleep(0.1)
                messagebox.showinfo("W R O N G ! ! !",f"The correct answer is {correct_answer}")
                
                
                    
            self.currentQuestionIndex += 1
            if self.currentQuestionIndex < len(self.topics):
                self.update_question()
            else:
                self.finish_quiz(self.calculated_iq,self.wrong_var,self.que_var)
        
    def finish_quiz(self,score, wrong_var, que_var):
        
        pygame.mixer.music.stop()
        self.congrats_music.play()
        
        # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)
        
        # Finish main frame 
        finish_frame = tk.Frame(self.root,bg="#2A225A") # violet
        finish_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.calculated_iq = 100 / self.que_var
        self.calculated_iq = self.calculated_iq * self.score
           
           
        # pag-compute ng dami ng tamang sagot ng player sa quiz game. 
        total_score = sum(
            [1 for index, answer in self.player_answers.items() if
             answer == self.topics[int(index)]["answer"]])
        
        
             

        # Done frame \ congratulations
        done_label0 = tk.Label(finish_frame,
                              text=f"Congratulations!",
                              bg="#2A225A",
                              fg="yellow",
                              font=("Comic sans MS", 45, "bold"))
        done_label0.grid(row=0, column=0, columnspan=2)

        done_Label1 = tk.Label(finish_frame,
                              text=f"You have completed the quiz.. ",
                              bg="#2A225A",
                              fg="white",
                              font=("Comic sans MS", 20, "bold"))
        done_Label1.grid(row=1, column=0, columnspan=2,pady=20)

        # showing score 
        done_Label2 = tk.Label(finish_frame,
                              text=f"    Score: {self.score}      ",
                              bg="black",
                              fg="green",
                              font=("Comic sans MS", 20, "bold"))
        done_Label2.grid(row=2, column=0, padx=60)

        # showing mistakes
        done_Label3 = tk.Label(finish_frame,
                              text=f"    Mistakes: {wrong_var}    ",
                              bg="black",
                              fg="red",
                              font=("Comic sans MS", 20, "bold"))
        done_Label3.grid(row=2, column=1, padx=60)

        # showing number of items
        done_Label4 = tk.Label(finish_frame,
                              text=f"Question Items : {que_var}",
                              bg="black",
                              fg="#04ABA1",
                              font=("Comic sans MS", 20, "bold"))
        done_Label4.grid(row=3, column=0, padx=60)

        # showing IQ %
        done_Label5 = tk.Label(finish_frame,
                              text=f"  IQ: {self.calculated_iq:.2f}%    ",
                              bg="black",
                              fg="orange",
                              font=("Comic sans MS", 20, "bold"))
        done_Label5.grid(row=3, column=1, padx=60)

        # Play again button
        back_button = tk.Button(finish_frame,
                                text="Play again?",
                                command=self.playagain_buttonsound,
                                cursor='hand2',
                                border=6,
                                background="#CB4F07",
                                foreground="WHITE",
                                activebackground="orange",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        back_button.grid(row=4, column=0, padx=25,pady=10)

         # nah .. button
        quit2_button = tk.Button(finish_frame,
                                text="   Nah..   ",
                                command=self.nah_buttonsound,
                                border=6,
                                cursor='hand2',
                                background="#B60A2E",
                                foreground="white",
                                activebackground="red",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        quit2_button.grid(row=4, column=1, padx=25,pady=10)
        
        # finish quiz sound button
    def playagain_buttonsound(self):
        self.button_music.play()
        self.destroy_finish_frame()
        
    def nah_buttonsound(self):
        self.button_music.play()
        self.quit_game()     


        
    def destroy_finish_frame(self):
        done_frame = self.root.nametowidget(self.root.winfo_children()[-1])
        done_frame.destroy()
        
        # reset all 
        self.calculated_iq = 0
        self.que_var = 0
        self.reset_score()
        self.reset_lives()
        self.reset_topics()
       
        self.show_frame2()# showing frame2 after destroying finish_frame
        
    def update_question(self):
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100) 
        self.generate_quiz_frame()
        
        
    def give_up(self):
        
        pygame.mixer.music.stop()
        self.gameover_music.play()

        self.destroy_current_game_frame() # destroying current frame bagu i-run ang submit frame
        
        
         # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)
        
        # Game over main frame
        game_over_frame = tk.Frame(self.root, bg="#2A225A")
        game_over_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Gameover frame
        game_over_label = tk.Label(game_over_frame,
                                   text="G A M E   O V E R !",
                                   pady=50,
                                   bg="#2A225A",
                                   fg="RED",
                                   font=("Comic sans MS", 35, "bold"))
        game_over_label.grid(row=0, column=0, columnspan=2)
        
         # Play again button
        back_button2 = tk.Button(game_over_frame,
                                text="Try again?",
                                command=self.tryagain_buttonsound,
                                cursor='hand2',
                                border=6,
                                background="#39BC00",
                                foreground="WHITE",
                                activebackground="#90ED67",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        back_button2.grid(row=4, column=0, padx=25,pady=10)  # Adjusted row, padx
        # nah .. button
        quit2_button2 = tk.Button(game_over_frame,
                                text="   Booo !  ",
                                command=self.boo_buttonsound,
                                border=6,
                                cursor='hand2',
                                background="#B60A2E",
                                foreground="white",
                                activebackground="red",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        quit2_button2.grid(row=4, column=1, padx=25,pady=10)  # Adjusted row, padx
  
     # give up button sounds
    def tryagain_buttonsound(self):
        self.button_music.play()
        self.destroy_finish_frame()
        
    def boo_buttonsound(self):
        self.button_music.play()
        self.quit_game()


    def game_over(self, calculated_iq, score, wrong_var, que_var):
        
        pygame.mixer.music.stop()
        self.gameover_music.play()

        self.destroy_current_game_frame() # destroying current frame bagu i-run ang submit frame
        
        
         # smooth forgeting current frame to go sa next frame 
        if self.currentFrame:
            self.currentFrame.pack_forget()
        self.root.after(100)
        
        # Finish main frame 
        finish_frame = tk.Frame(self.root,bg="#2A225A")
        finish_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.calculated_iq = 100 / self.que_var
        self.calculated_iq = self.calculated_iq * self.score
           
           
        # functions of counting right answers gamit ang " == "
        total_score = sum(
            [1 for index, answer in self.player_answers.items() if
             answer == self.topics[int(index)]["answer"]])
        
        # function for counting the mistakes gamit ang " != "
        wrong_var = sum(
            [1 for index, answer in self.player_answers.items()
             if answer != self.topics[int(index)]["answer"]])
        
        # function sa pag bilang ng nasagutang questions
        que_var = sum(
            [1 for index, answer in self.player_answers.items()
             if answer == self.topics[int(index)]["answer"] or answer != self.topics[int(index)]["answer"]])
             
        
        # Game over main frame
        game_over_frame = tk.Frame(self.root, bg="#2A225A")
        game_over_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Gameover frame
        game_over_label = tk.Label(game_over_frame,
                                   text="G A M E   O V E R !",
                                   bg="#2A225A",
                                   fg="RED",
                                   font=("Comic sans MS", 35, "bold"))
        game_over_label.grid(row=0, column=0, columnspan=2)

        game_over5_label = tk.Label(game_over_frame,
                                    text="You ran out of lives. Better luck next time!",
                                    pady=15,
                                    bg="#2A225A",
                                    fg="white",
                                    font=("Comic sans MS", 20, "bold"))
        game_over5_label.grid(row=1, column=0, columnspan=2,pady=10)  # Adjusted row

        # showing score 
        done_Label6 = tk.Label(game_over_frame,
                              text=f"   Score:{self.score}    ",
                              bg="black",
                              fg="green",
                              font=("Comic sans MS", 20, "bold"))
        done_Label6.grid(row=2, column=0, padx=60)  # Adjusted padx

        # showing mistakes
        done_Label7 = tk.Label(game_over_frame,
                              text=f"Mistakes: {wrong_var}",
                              bg="black",
                              fg="red",
                              font=("Comic sans MS", 20, "bold"))
        done_Label7.grid(row=2, column=1, padx=60)  # Adjusted row, padx,

        # showing number of items
        done_Label8 = tk.Label(game_over_frame,
                              text=f"Question Items: {que_var}",
                              bg="black",
                              fg="#04ABA1",
                              font=("Comic sans MS", 20, "bold"))
        done_Label8.grid(row=3, column=0, padx=60)  

        # showing IQ %
        done_Label9 = tk.Label(game_over_frame,
                              text=f"IQ: {self.calculated_iq:.2f}%",
                              bg="black",
                              fg="orange",
                              font=("Comic sans MS", 20, "bold"))
        done_Label9.grid(row=3, column=1, padx=60)  # Adjusted row, padx, 

        # Play again button
        back_button2 = tk.Button(game_over_frame,
                                text="Try again?",
                                command=self.tryagain_buttonsound,
                                cursor='hand2',
                                border=6,
                                background="#39BC00",
                                foreground="WHITE",
                                activebackground="#90ED67",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        back_button2.grid(row=4, column=0, padx=25,pady=10)  # Adjusted row, padx
        # nah .. button
        quit2_button2 = tk.Button(game_over_frame,
                                text="   Booo !  ",
                                command=self.boo_buttonsound,
                                border=6,
                                cursor='hand2',
                                background="#B60A2E",
                                foreground="white",
                                activebackground="red",
                                activeforeground="white",
                                font=("Comic sans MS", 20, "bold"))
        quit2_button2.grid(row=4, column=1, padx=25,pady=10)  # Adjusted row, padx
    
    
    def tryagain_buttonsound(self):
        self.button_music.play()
        self.destroy_finish_frame()
        
    def boo_buttonsound(self):
        self.button_music.play()
        self.quit_game()
    
        
     # destroy gameover frame function
    def destroy_game_over_frame(self):
        game_over_frame = self.root.nametowidget(self.root.winfo_children()[-1])
        game_over_frame.destroy()
        
        # reset all 
        self.calculated_iq = 0
        self.que_var = 0
        self.reset_score()
        self.reset_lives()
        self.reset_topics()

        self.show_frame2()

    # destroy current game frame function
    def destroy_current_game_frame(self):
        if self.currentFrame:
            self.currentFrame.destroy()

    def quit_game(self):
        self.root.destroy()
        pygame.mixer.music.stop()


root = tk.Tk()
group = InteractiveQuiz(root)
root.mainloop()


