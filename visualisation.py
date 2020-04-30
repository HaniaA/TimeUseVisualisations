#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:34:42 2019

@author: haniaadamczyk
"""
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from palettable.colorbrewer.diverging import *


class Visualisation:

    def __init__(self, tEmail):
        self.email = tEmail
    
    def shortenNames(df, max_length = 55):
        for index, row in df.iterrows():
            if len(row['Activity'])>max_length:
                short_activity = ''
                words = row['Activity'].split()
                charsum = 0
                for word in words:
                    charsum+=len(word)
                    charsum+=1
                    if(charsum<max_length):
                        short_activity=short_activity+word+" "
                    else:
                        short_activity=short_activity[:-1]
                        short_activity+=" ..."
                        break                    
                df.at[index, 'Activity'] = short_activity
        return df
                
    
    def timeDistributionTable(self, df, start_date, end_date):
        df = Visualisation.shortenNames(df, 30)
        headerColor = '#1BA41B'
        rowEvenColor = '#FFFFFF'
        rowOddColor = '#f5f5f5'
        
        n = df.shape[0]
        
        fig = go.Figure(data=[go.Table(
            columnwidth = [150,75],
            header=dict(values=list(df.columns),
                        line_color=headerColor,
                        fill_color=headerColor,
                        align=['center','center'],
                        font=dict(family="Arial, monospace", color='white', size=8),
                        height = 22
                        ),
            cells=dict(values=[df['Activity'], df['Total time']],
                            # 2-D list of colors for alternating rows
                            line_color = [[rowOddColor,rowEvenColor]*5],
                            fill_color = [[rowOddColor,rowEvenColor]*5],
                            align = ['left', 'center'],
                            font = dict(family="Arial, monospace", color = '#8c908f', size = 8),
                            height= 22
                            
            ))
        ])
        
        fig.update_layout(width=225, height=22*(n+1), margin={"l": 0, "r": 0, "t": 0, "b": 0})
        fig.show()
        name_current = str(self.email) + "_top10activities" + ".jpg"
        path_current = "/Users/" + name_current
        
        fig.write_image(path_current,width=225, height=22*(n+1), scale=4)
      
        return name_current
    
    def total_time_distribution_pie_chart(self, df, start_date, end_date):
        df = Visualisation.shortenNames(df, 40)
        labels = list(df["Activity"])
        values = list(df["Total time"])
        text = list()
        for value in values:
            text.append(str(value)+"h")
        colors = Spectral_8.hex_colors
        colors.reverse()
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, text=text, marker=dict(colors=colors
                                                            , line=dict(color='#FFF', width=2))
                                                            , showlegend=False, textinfo="label+percent")])
        fig.update_layout(margin={"l": 30, "r": 30, "t": 30, "b": 30})

        fig.show()
        
        name_current = str(self.email) + "_piechart" + ".jpg"
        path_current = "/Users/" + name_current
        fig.write_image(path_current, scale=4)
        return name_current
        
        
    def total_time_distribution_word_cloud(self, text, start_date, end_date):
        # Create stopword list:
        stopwords = set(STOPWORDS)
        name_current = str(self.email) + "_wordcloud" + ".jpg"
        path_current = "/Users/"+ name_current 
        try:
            # Generate a word cloud image
            wordcloud = WordCloud(width=1600, height=800, stopwords=stopwords, background_color="white").generate(text)
            
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout(pad=0.5)

            wordcloud.to_file(path_current)
            plt.show()
        except ValueError:
            fig = plt.figure()
            fig.show()
            fig.savefig(path_current)
            print("ValueError: We need at least 1 word to plot a word cloud, got 0.")
        
        return name_current
    
    def total_time_distribution_word_cloud_from_frequencies(self, word_frequencies, start_date, end_date):
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_frequencies)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0.5)
        
        name_current = str(self.email) + "_wordcloudfreq" + ".jpg"
        path_current = "/Users/" + name_current        
        wordcloud.to_file(path_current)
        plt.show()
        return name_current
        