from operator import itemgetter
from math import sqrt


def load_data():
    filename_user_movie = 'u.data'
    filename_movieInfo = 'u.item'

    user_movie = {}
    for line in open(filename_user_movie,'r',encoding = "ISO-8859-1"):
        (userId, itemId, rating, timestamp) = line.strip().split('\t')
        user_movie.setdefault(userId, {})
        user_movie[userId][itemId] = float(rating)

    movies = {}
    for line in open(filename_movieInfo,'r',encoding = "ISO-8859-1"):
        (movieId, movieTitle) = line.split('|')[0:2]
        movies[movieId] = movieTitle

    return user_movie, movies


def average_rating(user):
    average = 0
    for u in user_movie[user].keys():
        average += user_movie[user][u]
    average = average * 1.0 / len(user_movie[user].keys())
    return average


def calUserSim(user_movie):
    # build inverse table for movie_user
    movie_user = {}
    for ukey in user_movie.keys():
        for mkey in user_movie[ukey].keys():
            if mkey not in movie_user:
                movie_user[mkey] = []
            movie_user[mkey].append(ukey)

            # calculated co-rated movies between users
    C = {}
    for movie, users in movie_user.items():
        for u in users:
            C.setdefault(u, {})
            for n in users:
                if u == n:
                    continue
                C[u].setdefault(n, [])
                C[u][n].append(movie)

                # calculate user similarity (perason correlation)
    userSim = {}
    for u in C.keys():

        for n in C[u].keys():

            userSim.setdefault(u, {})
            userSim[u].setdefault(n, 0)

            average_u_rate = average_rating(u)
            average_n_rate = average_rating(n)

            part1 = 0
            part2 = 0
            part3 = 0
            for m in C[u][n]:
                part1 += (user_movie[u][m] - average_u_rate) * (user_movie[n][m] - average_n_rate) * 1.0
                part2 += pow(user_movie[u][m] - average_u_rate, 2) * 1.0
                part3 += pow(user_movie[n][m] - average_n_rate, 2) * 1.0

            part2 = sqrt(part2)
            part3 = sqrt(part3)
            if part2 == 0:
                part2 = 0.001
            if part3 == 0:
                part3 = 0.001
            userSim[u][n] = part1 / (part2 * part3)
    return userSim


def getRecommendations(user, user_movie, movies, userSim, N):
    pred = {}
    interacted_items = user_movie[user].keys()
    average_u_rate = average_rating(user)
    sumUserSim = 0
    for n, nuw in sorted(userSim[user].items(), key=itemgetter(1), reverse=True)[0:N]:
        average_n_rate = average_rating(n)
        for i, nrating in user_movie[n].items():
            # filter movies user interacted before
            if i in interacted_items:
                continue
            pred.setdefault(i, 0)
            pred[i] += nuw * (nrating - average_n_rate)
        sumUserSim += nuw

    for i, rating in pred.items():
        pred[i] = average_u_rate + (pred[i] * 1.0) / sumUserSim

        # top-6 pred
    pred = sorted(pred.items(), key=itemgetter(1), reverse=True)[0:6]
    return pred


if __name__ == "__main__":

    # load data
    user_movie, movies = load_data()

    # Calculate user similarity
    userSim = calUserSim(user_movie)

    # Recommend
    for id in range(1,944):
        pred = getRecommendations(str(id), user_movie, movies, userSim, 20)
        print("%3d\t"%id,end="")
        # display recommend result (top-10 results)
        for i, rating in pred:
            print("%4d\t"%int(i),end="")
            print("%10.8f\t"%rating,end="")
        print("")


