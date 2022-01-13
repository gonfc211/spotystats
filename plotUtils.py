import numpy as np
import matplotlib.pyplot as plt
import telegramUtils
import spotyUtils


def plotStat(popularity, feature, feature_name, playlist_name):


    x = feature[0]
    labels = feature[1]


    x = np.array(x)
    y = np.array(popularity)

    fig = plt.figure(figsize = (40,20))

    plt.scatter(x, y, s = 500, color ='green', marker = 'o', edgecolors='k')

    plt.xlabel(feature_name, fontsize = 50)

    plt.ylabel('Popularity', fontsize = 50)

    plt.xticks(fontsize=50)
    plt.yticks(fontsize=50)

    title = playlist_name +': ' +feature_name+ ' vs Popularity'

    plt.title(title, fontsize = 50)

    num_tracks = len(labels)

    for i in labels:
        label_index = labels.index(i)
        if label_index %5 != 0 and num_tracks > 20:
            continue
        xs_index = x[label_index]
        ys_index = y[label_index]
        plt.annotate(i, (xs_index,ys_index), fontsize = 40)


    name = (title + '.jpg')

    plt.savefig('plots/'+name)

    return title


def plot_histogram(features, popularities, playlist_name):

    mean_pop = np.mean(popularities)
    mean_acoustic = np.mean(telegramUtils.get_feature(features, 'Acousticness')[0])
    mean_dance = np.mean(telegramUtils.get_feature(features, 'Danceability')[0])
    mean_energy = np.mean(telegramUtils.get_feature(features, 'Energy')[0])
    mean_instru = np.mean(telegramUtils.get_feature(features, 'Instrumentalness')[0])
    mean_speech = np.mean(telegramUtils.get_feature(features, 'Speechiness')[0])
    mean_valence = np.mean(telegramUtils.get_feature(features, 'Valence')[0])

    eje_x = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Speechiness', 'Valence']
    eje_y = [mean_pop, mean_acoustic, mean_dance, mean_energy, mean_instru, mean_speech, mean_valence]

    x = np.arange(len(eje_x))

    fig, ax = plt.subplots(figsize=(40,20))
    ax.bar(x, eje_y, color = 'g')

    ax.set_ylabel('Percentage', fontsize = 40)

    ax.set_xticks(x)
    ax.set_xticklabels(eje_x)

    #plt.ylabel('Percentage', fontsize = 50)
    #plt.xlabel('Features', fontsize = 50)

    plt.yticks(fontsize = 30)
    plt.xticks(fontsize = 36)

    title = playlist_name +': Histogram'

    plt.title(title, fontsize = 45)

    name = title + '.jpg'

    plt.savefig('plots/'+name)

    return title

def correlation(features, popularity):
    np_features = ([np.array(item[0]) for item in features])
    np_features = np.transpose(np_features)
    np_popularity = np.array(popularity)

    data = np.insert(np_features, 0, np_popularity, axis=0)
    all_correlations = np.corrcoef(data)

    correlations = all_correlations[0]

    return correlations
