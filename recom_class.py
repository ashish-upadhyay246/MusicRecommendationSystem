#
import numpy as np
import pandas

class Similar_Items_Recommender():
    def __init__(self):
        self.user_id = None
        self.song = None
        self.coc_matrix = None
        self.dataframe_entered = None
    
    def construct(self, dataframe_entered, user_id, song):
        self.dataframe_entered = dataframe_entered
        self.user_id = user_id
        self.song = song
#



    def get_item_users(self, item):
        item_data = self.dataframe_entered[self.dataframe_entered[self.song] == item]
        item_users = set(item_data[self.user_id].unique()) 
        return item_users
        
    def construct_coc_matrix(self, user_songs, all_songs):
        #getting all the users of the entered song
        user_songs_users = []        
        for i in range(0, len(user_songs)):
            user_songs_users.append(self.get_item_users(user_songs[i]))
        
        #making a coocurence matrix of dimension (user_songs x all_songs), and initializing it to '0'.  
        coc_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)
        
        #finding similarity between entered song and all the unique songs in the dataframe.
        for i in range(0,len(all_songs)):
            #finding unique listeners of individual songs in the dataframe.
            songs_i_data = self.dataframe_entered[self.dataframe_entered[self.song] == all_songs[i]]
            users_i = set(songs_i_data[self.user_id].unique())
            
            for j in range(0,len(user_songs)):       
                users_j = user_songs_users[j]
                users_intersection = users_i.intersection(users_j)
                
                #calculating coc_matrix[i,j] as Jaccard Index
                if len(users_intersection) != 0:
                    users_union = users_i.union(users_j)
                    coc_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    coc_matrix[j,i] = 0
        return coc_matrix

    def generate_top_recommendations(self, coc_matrix, all_songs, user_songs):
        print("SIMILAR songs found : %d\n" % np.count_nonzero(coc_matrix))
        user_sim_scores = coc_matrix.sum(axis=0)/float(coc_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()
        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)
    
        #creating a dataframe for the solution
        columns = ['Rank', 'Song', '  Similarity Score']
        df = pandas.DataFrame(columns=columns)
        
        rank = 1 
        iterate=1
        for i in range(0,len(sort_index)):
            if iterate==11:
                break
            else:
                if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= 30:
                    df.loc[len(df)]=[rank,all_songs[sort_index[i][1]],sort_index[i][0]]
                    iterate+=1
                    rank = rank+1
        return df

    def get_similar_items(self, item_list):
        user_songs = item_list
        all_songs =list(self.dataframe_entered[self.song].unique())
        print("\nNumber of UNIQUE songs in the dataframe : %d" % len(all_songs))
        coc_matrix = self.construct_coc_matrix(user_songs, all_songs)
        df_recommendations = self.generate_top_recommendations(coc_matrix, all_songs, user_songs)
        print("==================================================================")
        print(df_recommendations.to_string(index=False))
        print("==================================================================")