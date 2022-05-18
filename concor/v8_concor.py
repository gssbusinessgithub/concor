from distutils.log import error
from lib2to3.pgen2.token import RIGHTSHIFT
from spv8 import * 
from tkinter import *
from playsound import playsound

#os.system("say welcome to concor")
#AppKit.NSBeep()
playsound('sound/success.wav')


# main terminal
root = Tk()
root.option_add('*Font','Courier','15')
root.title('V8_Concor')
#root.iconbitmap(None)
root.geometry('750x1600')
root.configure(bg='#FFFFFF')

#output boxes:
output = Text(root,width=60,height=15,bg='gainsboro')
output.pack(fill=X, side=TOP, ipady = 75)

# enter key phrases here:
key_phrases_directions = Text(root, height = 2, width = 25, bg ="gainsboro")
key_phrases_directions.pack(fill=X,side=TOP)
key_phrases_directions.insert(END, 'Type Desired Key Phrases to be Searched Below - Phrases can be one or two words \t \n Example: cash transfers,loans,cash grants, ... | NO SPACES after commas')
key_phrases = Entry(root,textvariable=StringVar())
key_phrases.pack(fill=X,side=TOP)

title_directions = Text(root, height = 1, width = 10, bg ="gainsboro")
title_directions.pack(fill=X,side=TOP)
title_directions.insert(END, 'Type Desired Title for Bar Chart Below')
title_name = Entry(root,textvariable=StringVar())
title_name.pack(fill=X,side=TOP)

graph_file = Text(root, height = 1, width = 10, bg ="gainsboro")
graph_file.pack(fill=X,side=TOP)
graph_file.insert(END, 'Type Desired Graph File Name Below (Will be saved as .png file)')
graph_file_entry = Entry(root,textvariable=StringVar())
graph_file_entry.pack(fill=X,side=TOP)

concor_width_text = Text(root, height = 1, width = 10, bg ="gainsboro")
concor_width_text.pack(fill=X,side=TOP)
concor_width_text.insert(END, 'Type Desired Length of Soft Mention Vicinity (Recommendation: 60)')
concor_width = Entry(root,textvariable=StringVar())
concor_width.pack(fill=X,side=TOP)
concor_width.insert(END, '60')

match_ratio_text = Text(root, height = 1, width = 10, bg ="gainsboro")
match_ratio_text.pack(fill=X,side=TOP)
match_ratio_text.insert(END, 'Type Desired FuzzyWuzzy Match Ratio Below (Recommendation: 80)')
match_ratio = Entry(root,textvariable=StringVar())
match_ratio.pack(fill=X,side=TOP)
match_ratio.insert(END, '80')

errorput = Text(root,width=30,height=1,bg='#0000D6',
                font=("Courier",15),
                fg='white')
errorput.pack(side=LEFT, ipady = 100)

infoput = Text(root,width=60,height=10,bg='gainsboro')
infoput.pack(side=LEFT, ipady = 100)

#create startup and error sounds: for mac




output.insert(END, logo)
output.insert(END, '\n Version 8.2 | 2022 \n')
output.insert(END, '______________________________________________________ \n')
output.insert(END, '\n *** Place all text (.txt) files to be analyzed in the directory folder: concor/data/to_read\n')

errorput.insert(END,'ERROR MESSAGES HERE: \n')

def delete_merge():
    if os.path.exists("merge_file_concor.txt"):
        os.remove("merge_file_concor.txt")
        output.insert(END, '>> Successfully Deleted merge_file_concor.txt \n')
        playsound('sound/success.wav')
    else:
        #AppKit.NSBeep()
        errorput.insert(END, '>> ERROR OCCURED: Unable to delete file that does not exist.\n')
        playsound('sound/error.wav')

def run_analysis(save_name1 = graph_file_entry,
                    title_name1 = title_name, 
                    entry_key = key_phrases,
                    concor_width1 = concor_width,
                    match_ratio1 = match_ratio):
    from glob import glob

    PATH_DATA = 'data/'
    PATH_TO_LOAD = 'to_read/'
    FILE_PATTERN = '*.txt'

    filenames = glob(PATH_DATA + PATH_TO_LOAD + FILE_PATTERN)
    filenames.sort()
    output.insert(END,'\n Loading... \n')
    #output.insert(END,'>> Variable type of filenames: '+str(type(filenames))+'\n')

    # merge all text files listed in variable filenames into one text file:
    with open('merge_file_concor.txt', 'w') as outfile:
        for names in filenames:
            with open(names) as infile:
                outfile.write(infile.read())
            outfile.write("\n")

    output.insert(END,'>> Number of Files: ' + str(len(filenames))+'\n')
    # 11.4 MB size

    with open('merge_file_concor.txt','r') as file:
        file = file.read()
        text = file.lower()
        punct = '.,;:"?!."-'
        text = text.translate(text.maketrans('','',punct))
        tokens = word_tokenize(text)
        #tokens = [token for token in tokens if token not in eng_stops and not token.isdigit()]
        textList = nltk.Text(tokens)

    string_var = entry_key.get()
    #output.insert(END,'>> key_phrase type:' + str(type(string_var)) + '\n')
    output.insert(END,'>> Entered Key Phrases: ' + str(string_var) + '\n')
    if len(string_var) == 0:
        errorput.insert(END,'>> ERROR OCCURED: No Key Phrases Entered \n')
        playsound('sound/error.wav')
        return False

    try:
        concor_width = int(str(concor_width1.get()))
        match_ratio = int(str(match_ratio1.get()))

    except Exception as e: 
        errorput.insert(END,'>> ERROR OCCURED: '+str(e))
        playsound('sound/error.wav')

    if (concor_width < 0) or (match_ratio < 0):
        errorput.insert(END, '>> ERROR OCCURED: Vicinity nor ratio can be negative.\n')
        playsound('sound/error.wav')
        return False
    
    if (concor_width > 100) or (match_ratio > 100):
        errorput.insert(END, '>> ERROR OCCURED: Vicinity nor ratio can be over 100.\n')
        playsound('sound/error.wav')
        return False
    
    convert_list = list(string_var.split(","))

    #output.insert(END,'>> Successfully convert key phrases as: ' + str(type(convert_list)) + '\n')
    output.insert(END,'>> Number of Key Phrases in List: ' + str(len(convert_list)) + '\n')

    # def convert(phrase_entry = string_var):
    #     convert_list = key_phrases(phrase_entry.split(","))
    #     return convert_list

    output.insert(END, '>> Successfully Merged All Files and Tokenized Words. \n Saved As: merge_file_concor.txt \n')
    output.insert(END, '------------------------------------------- \n')

    def phrase_search(phrases = convert_list,
                        data = textList,
                        concor_width2 = concor_width1,
                        match_ratio2 = match_ratio1,
                        file_tokens = tokens):
        ''' ~~ Documentation for phrase_search ~~ 
        The phrase_search function counts the number of mentions of each 
        phrase from the user provided list. The results will be returned 
        as a pandas dataframe with 3 columns: phrases (the phrase 
        searched), mentions (the count of the respective phrase), 
        category (the user specified group the phrase belongs to)

        1. phrases = list that houses the phrases desired to be searched.
        If an entry in phrases is one word, then phrase_search will hard
        search the one word.
        If an entry is a phrase of two words, then the first word in the
        phrase will be hard searched. The second word in the phrase will
        be soft searched. Soft search means the use of fuzzywuzzy python
        library which will assess if each token in a concordance result
        of the hard word is similar enough to the soft word. 
        
        2. data = the .txt file that houses the entire text desired to 
        be analyzed.
        
        3. category = the category you desire to refer this word/phrase
        as. Category will have its own column in the dataframe.
        
        4. concor_width = the desired token list length with respect to the vicinity
        of the query word.
        
        5. match_ratio = the desired ratio threshold for the FuzzyWuzzy 
        token_sort_ratio scrutinizing the similarity of the token compared
        to the queried phrase.'''

        concor_width = int(str(concor_width2.get()))
        match_ratio = int(str(match_ratio2.get()))

        tStart = dt.now()
        k = 0
        d_phrase = {}
        mentions = []
        print(phrases)
        while k < len(phrases):

            if len(phrases[k].split()) == 1:
                first_word = phrases[k]
                print(first_word)

                counter1 = 0
                for token in file_tokens:
                    if token == first_word:
                        print(token)
                        counter1 += 1
                        
                d_phrase["phrase{0}".format(k)] = counter1
                mentions.append(counter1)

                print(d_phrase)

                k+=1


            else:
                split_phrase = phrases[k].split()

                first_word = split_phrase[0]
                second_word = split_phrase[1]

                counter1 = 0
                for token in file_tokens:
                    if token == first_word:
                        counter1 += 1
                #print('textList:', data)
                #print(counter1)

                # use concordance list to recieve a list output ***
                # concordance itself will only print results and then return a none type

                concor = data.concordance_list(first_word, width = concor_width, lines = counter1) #
                #print(concor)

                # creating this while loop:
                # https://stackoverflow.com/questions/6181935/how-do-you-create-different-variable-names-while-in-a-loop
                # https://stackoverflow.com/questions/12453580/how-to-concatenate-items-in-a-list-to-a-single-string

                i = 0
                d_concor={}
                d_fuzz = {}
                while i < counter1:
                    #variables will be overwritten for each i
                    #clear_output()
                    #print('> Processing line ', i)
                    #complete_concor = wordlistR + keyword search + wordlistL
                    complete_concor = concor[i][0]+[concor[i][1]]+concor[i][2]
                    d_concor["sentence{0}".format(i)] = ' '.join(complete_concor)
                    #print('> Concordance line ', type(complete_concor))

                    j = 0
                    word_list = []
                    while j < len(complete_concor):
                        ratio = fuzz.token_sort_ratio(second_word,complete_concor[j])
                        if ratio > match_ratio:
                            word_list.append(complete_concor[j])
                            j+=1
                        else:
                            j+=1
                    d_fuzz["sentence{0}".format(i)] = ' '.join(word_list)
                    i += 1

                #print(d_fuzz)

                #avoid double dipping and counting a mention more than once solely 
                # because fuzzy word appeared more than once 
                # here we count as long as value is not empty:
                counter2 = 0
                for key, value in d_fuzz.items():
                    if value != '':
                        counter2 += 1
                #print(counter2)

                d_phrase["phrase{0}".format(k)] = counter2
                mentions.append(counter2)
                #print(d_phrase)
                #print(mentions)

                # Unique values in a python dictionary:
                # https://stackoverflow.com/questions/17218139/print-all-unique-values-in-a-python-dictionary
                uniqueValues = set(d_fuzz.values())
                infoput.insert(END,'___________________________________________\n')
                infoput.insert(END,'>> Unique similar or exact soft mentions instances near vicinity of hard mention: '+str(first_word)+'\n')
                for value in uniqueValues:
                     infoput.insert(END,str(value)+'\n')
                infoput.insert(END,'\n')
                infoput.insert(END,'>> Number of unique hard and soft mention combinations found: '+str(len(uniqueValues))+'\n')

                #ratio = fuzz.token_sort_ratio('transfer',d["sentence0"])
                #print('> Similarity score: {}'.format(ratio))
                k+=1

        d_mentions = {
            'phrases'  : phrases, 
            'mentions' : mentions        
        }
        df = pd.DataFrame(d_mentions)

        output.insert(END,'>> Successfully read through text sources \n')
        output.insert(END,'>> Total words in sources: '+str(len(data))+'\n')
        output.insert(END,'>> Time Lapsed to Run Analysis:'+str(dt.now()-tStart)+'\n')
        output.insert(END,'\n')
        output.insert(END,'Results: Key Phrase & Mention Count:\n'+str(df))
        return(df)
    dfKey = phrase_search()

    def make_graph(save_name2 = save_name1,
                    title_name2 = title_name1,
                    df = dfKey, FONTSIZE = 20):
        df = df.sort_values(['mentions'])
        title_name2 = title_name2.get()
        save_name2 = save_name2.get()

        #dfFinal.set_index('category',inplace = True)

        y = df['mentions']

        #fig, ax = plt.subplots(figsize=(24,18))
        #ax.barh(y.index, y, height=0.75, color='navy')

        ax = df.plot(kind='barh',x='phrases',y='mentions',
                            figsize=(24,18), color = 'navy')
        #ax.legend(labels=dfFinal['category'].unique().tolist(), handles=ax.patches,
        #            fancybox=True)
        #for p in ax.patches:
        #    ax.annotate("{:.1f}".format(p.get_height()), xy=(p.get_x() * 1.015, p.get_height() * 1.015))

        # Hide all spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.tick_params(axis='both', which='major', labelsize=FONTSIZE)
        
        plt.title(str(title_name2), fontsize = FONTSIZE+5)
        plt.xlabel('Count of Key Phrases', fontsize = FONTSIZE)
        plt.ylabel('')
        _, xmax = plt.xlim()
        plt.xlim(0, xmax+75)
        for i, v in enumerate(y):
            ax.text(v+10, i, str(v), color='black', 
                fontweight='bold', fontsize=FONTSIZE,
                ha='left', va='center')
        ax.get_legend().remove()
            
        plt.savefig(str(save_name2)+'.png',bbox_inches='tight')
        #plt.show()
        output.insert(END,"\n")
        output.insert(END,"\n>> Horizontal Bar Graph Successfully Created \t \n Saved As:" + str(save_name2)+'.png\n')
        playsound('sound/success.wav')
    make_graph()

#the run button merges all text files in to_read folder and returns the dataframe
# housing the mention count by key phrase:
run_button = Button(root, height = 1, width = 15, text = "Run Analysis", command=lambda: run_analysis()).place(x=550, y=25)
delete_merge_button = Button(root, height = 1, width = 15, text = "Delete Merge File", command=lambda: delete_merge()).place(x=550, y=50)
root.mainloop()