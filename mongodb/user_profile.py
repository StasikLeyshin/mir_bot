from pymongo import MongoClient
#from settings import *

# localhost = "localhost"
# port = 27017
# client = MongoClient(localhost, int(port))


class user_profile:

    def __init__(self, client, user_id, documents="profile_bs", **kwargs):
        self.client = client
        self.user_id = user_id
        self.documents = documents

        self.user_info_bs = None
        self.user_info = None
        self.kwargs = kwargs
        self.user_info_update(kwargs.get("globan"))
        #self.user_info_update()
        # if self.is_int(self.documents):
        #     self.user_info_bs = self.add_value_bs_profile(self.documents)
        #     for attr in self.user_info_bs[1]:
        #         if attr not in ['_id', 'user_id', 'user_info_bs', 'documents']:
        #             setattr(self, attr, self.user_info_bs[1][attr])
        #
        # # self.score = score
        # # self.influence_score = influence_score
        # self.user_info = self.add_value_bs_profile()
        # for attr in self.user_info[1]:
        #     if attr not in ['_id', 'user_id', 'user_info', 'documents']:
        #         setattr(self, attr, self.user_info[1][attr])
        #print(self.__dict__)
        #self.__dict__["user_id"] = 13

    def is_int(self, txt):
        try:
            int(txt)
            return True
        except:
            return False

    # @property
    # def score(self):
    #     return round(self.score, 3)


    def user_info_update(self, globan=None):
        if self.is_int(self.documents):
            self.user_info_bs = self.add_value_bs_profile(documents=self.documents)
            for attr in self.user_info_bs[1]:
                if attr not in ['_id', 'user_id', 'user_info_bs', 'documents']:
                    setattr(self, attr, self.user_info_bs[1][attr])
        if not globan:
            self.user_info = self.add_value_bs_profile()
            for attr in self.user_info[1]:
                if attr not in ['_id', 'user_id', 'user_info', 'documents']:
                    setattr(self, attr, self.user_info[1][attr])

    def self_update(self):
        self.user_info = self.add_value_bs_profile()
        for i in self.user_info[1]:
            if i not in ['_id', 'user_id', 'user_info', 'documents', 'user_info_bs']:
                if self.user_info[1][i] != self.__dict__.get(i):
                    self.__dict__[i] = self.user_info[1][i]
        if self.is_int(self.documents):
            self.user_info_bs = self.add_value_bs_profile(self.documents)
            for i in self.user_info_bs[1]:
                if i not in ['_id', 'user_id', 'user_info', 'documents', 'user_info_bs']:
                    if self.user_info_bs[1][i] != self.__dict__.get(i):
                        self.__dict__[i] = self.user_info_bs[1][i]


    def add_value_bs_profile(self, collections="bots", documents="profile_bs"):
        db = self.client[f"{collections}"]
        posts = db[f"{documents}"]
        post = posts.find_one({'user_id': int(self.user_id)})
        if post is None:

            if self.is_int(documents):
                posts.insert_one({"user_id": int(self.user_id), "admin": False, "output": False, "kicked": False})
            else:
                posts.insert_one({
                    "user_id": int(self.user_id),
                    "score": 0,
                    "influence": 0.25,
                    "achievements": {}

                })
            return True, posts.find_one({'user_id': int(self.user_id)}), posts
        else:
            # posts.save(post)
            return False, post, posts

    def change_score_bs_profile(self, score: int, flag=False):
        #result = self.add_value_bs_profile(user_id)
        sl = "score"
        if flag:
            sl = "influence"
        if not self.user_info[1].get(sl):
            self.user_info[1][sl] = round(score, 3)
            total_score = self.user_info[1][sl]
        else:
            self.user_info[1][sl] += round(score, 3)
            total_score = self.user_info[1][sl]
        self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
                                     {'$set': {sl: round(self.user_info[1][sl], 3)}})
        #self.user_info_update()
        return round(total_score, 3)

    def add_statistics_bs(self, update="update", user_id=None, score=0):
        db = self.client[f"bots"]
        posts = db[f"statistics_bs"]
        post = posts.find_one({'peer_id': int(self.documents)})
        if post is None:
            if user_id:
                sl = {
                    'peer_id': int(self.documents),
                    'number_days': {
                        '1': {
                            update: 1,
                            str(self.user_id): {
                                update: 1,
                            }
                        },
                        'end_day': 1,
                        'time_day': 0
                    },
                    'score': score
                }
            else:
                sl = {
                    'peer_id': int(self.documents),
                    'number_days': {
                        '1': {
                            update: 1,

                        },
                        'end_day': 1,
                        'time_day': 0,
                    },
                    'score': score
                }
            posts.insert_one(sl)
        else:
            if post['number_days'][f'{post["number_days"]["end_day"]}'].get(f'{update}'):
                post['number_days'][f'{post["number_days"]["end_day"]}'][f'{update}'] += 1
            else:
                post['number_days'][f'{post["number_days"]["end_day"]}'][f'{update}'] = 1

            post[f'score'] += score

            if user_id:
                if post['number_days'][f'{post["number_days"]["end_day"]}'].get(f'{self.user_id}'):
                    if post['number_days'][f'{post["number_days"]["end_day"]}'][f'{self.user_id}'].get(f'{update}'):
                        post['number_days'][f'{post["number_days"]["end_day"]}'][f'{self.user_id}'][f'{update}'] += 1
                    else:
                        post['number_days'][f'{post["number_days"]["end_day"]}'][f'{self.user_id}'][f'{update}'] = 1
                else:
                    post['number_days'][f'{post["number_days"]["end_day"]}'][f'{self.user_id}'] = {
                        f'{update}': 1
                    }
            posts.save(post)
            # posts.update_one({'_id': post['_id']},
            #                  {'$inc': {update: 1}})


    def add_warn_bs_profile(self, start_time, end_time, cause, admin_id):
        warn = "warn"
        if not self.user_info_bs:
            return False

        if not self.user_info_bs[1].get(warn):
            self.user_info_bs[1][warn] = {
                "1": {
                    "status": True,
                    "start_time": start_time,
                    "end_time": end_time,
                    "cause": cause,
                    "admin_id": admin_id
                },
                "count": 1,
                "count_old": 2
            }
            self.user_info_bs[2].update_one({'_id': self.user_info_bs[1]['_id']},
                                         {
                                             '$set': {
                                                 warn: self.user_info_bs[1][warn]
                                             }
                                         })
        else:
            self.user_info_bs[1][warn][str(self.user_info_bs[1][warn]["count_old"])] = {
                "status": True,
                "end_time": end_time,
                "start_time": start_time,
                "cause": cause,
                "admin_id": admin_id
            }
            if self.user_info_bs[1]["warn"]["count"] == 2:
                self.user_info_bs[1][warn]["count"] = 0
            else:
                self.user_info_bs[1][warn]["count"] += 1
            self.user_info_bs[1][warn]["count_old"] += 1
            # self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
            #                              {
            #                                  '$set': {
            #                                      "warn": {
            #                                          str(self.user_info[1]["warn"]["count_old"]):
            #                                              self.user_info[1]["warn"][str(self.user_info[1]["warn"]["count_old"] - 1)],
            #                                          "count": self.user_info[1]["warn"]["count"],
            #                                          "count_old": self.user_info[1]["warn"]["count_old"]
            #                                      }
            #                                  }
            #                              })
        self.user_info_bs[2].save(self.user_info_bs[1])
        #self.user_info[2].replace_one({'_id': self.user_info[1]['_id']}, self.user_info[1], upsert=False)

        self.user_info_update()
        self.add_statistics_bs(warn)

        return self.user_info_bs[1][warn]["count"]

    def add_ban_bs_profile(self, end_time, start_time, cause, admin_id):
        warn = "ban"
        if not self.user_info_bs:
            return 0
        if not self.user_info_bs[1].get(warn):
            self.user_info_bs[1][warn] = {
                "1": {
                    "status": True,
                    "end_time": end_time,
                    "start_time": start_time,
                    "cause": cause,
                    "admin_id": admin_id
                },
                "count": 1,
            }
            self.user_info_bs[2].update_one({'_id': self.user_info_bs[1]['_id']},
                                         {
                                             '$set': {
                                                 warn: self.user_info_bs[1][warn]
                                             }
                                         })
        else:
            if self.user_info_bs[1][warn][str(self.user_info_bs[1][warn]["count"])]["status"]:
                return -1

            self.user_info_bs[1][warn][str(int(self.user_info_bs[1][warn]["count"] + 1))] = {
                "status": True,
                "end_time": end_time,
                "start_time": start_time,
                "cause": cause,
                "admin_id": admin_id
            }
            self.user_info_bs[1][warn]["count"] += 1

        self.user_info_bs[2].save(self.user_info_bs[1])

        self.user_info_update()
        self.add_statistics_bs(warn)

        return self.user_info_bs[1][warn]["count"]

    def add_globan_bs_profile(self, start_time, cause, admin_id):
        warn = "globan"
        if not self.user_info_bs:
            return 0
        if not self.user_info_bs[1].get(warn):
            self.user_info_bs[1][warn] = {
                "1": {
                    "status": True,
                    "start_time": start_time,
                    "cause": cause,
                    "admin_id": admin_id
                },
                "count": 1,
            }
            self.user_info_bs[2].update_one({'_id': self.user_info_bs[1]['_id']},
                                         {
                                             '$set': {
                                                 warn: self.user_info_bs[1][warn]
                                             }
                                         })
            db = self.client[f"bots"]
            posts_peer_ids = db[f"settings"]
            pos_new = posts_peer_ids.find_one({"perv": 1})
            peer_ids = pos_new["peer_ids"].split(", ")
            return 1, peer_ids
        else:
            if self.user_info_bs[1][warn][str(self.user_info_bs[1][warn]["count"])]["status"]:
                db = self.client[f"bots"]
                posts_peer_ids = db[f"settings"]
                pos_new = posts_peer_ids.find_one({"perv": 1})
                peer_ids = pos_new["peer_ids"].split(", ")
                return 2, peer_ids

            self.user_info_bs[1][warn][str(int(self.user_info_bs[1][warn]["count"] + 1))] = {
                "status": True,
                "start_time": start_time,
                "cause": cause,
                "admin_id": admin_id
            }
            self.user_info_bs[1][warn]["count"] += 1

        self.user_info_bs[2].save(self.user_info_bs[1])

        self.user_info_update()
        self.add_statistics_bs(warn)

        db = self.client[f"bots"]
        posts_peer_ids = db[f"settings"]
        pos_new = posts_peer_ids.find_one({"perv": 1})
        peer_ids = pos_new["peer_ids"].split(", ")
        return 1, peer_ids


    async def get_globan_peer_ids(self):
        db = self.client[f"bots"]
        posts_peer_ids = db[f"settings"]
        pos_new = posts_peer_ids.find_one({"perv": 1})
        peer_ids = pos_new["peer_ids"].split(", ")
        return peer_ids
        # db = client[f"{collections}"]
        # posts = db[f"{documents}"]
        # po_new = posts.find_one({'user_id': int(self.user_id)})
        # if po_new is None:
        #     posts.insert_one(
        #         {"user_id": int(self.user_id), "status": True, "cause": cause,
        #          "start_time": start_time, "admin_id": admin_id})
        #     posts_peer_ids = db[f"settings"]
        #     pos_new = posts_peer_ids.find_one({"perv": 1})
        #     peer_ids = pos_new["peer_ids"].split(", ")
        #     return 1, peer_ids
        # else:
        #     if po_new["status"]:
        #         posts_peer_ids = db[f"settings"]
        #         pos_new = posts_peer_ids.find_one({"perv": 1})
        #         peer_ids = pos_new["peer_ids"].split(", ")
        #         return 2, peer_ids
        #     else:
        #         po_new["status"] = True
        #         po_new["start_time"] = start_time
        #         po_new["admin_id"] = admin_id
        #         po_new["cause"] = cause
        #         posts.save(po_new)
        #         posts_peer_ids = db[f"settings"]
        #         pos_new = posts_peer_ids.find_one({"perv": 1})
        #         peer_ids = pos_new["peer_ids"].split(", ")
        #         return 1, peer_ids

    def change_info_bs_profile(self, **kwargs):
        self.user_info_bs[2].update_one({'_id': self.user_info[1]['_id']},
                                        {
                                            '$set': kwargs
                                        })
        self.user_info_update()

    def add_sms_bs_profile(self, type_sms="text"):
        self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
                                     {
                                         '$inc': {
                                             type_sms: 1
                                         }

                                     })
        self.add_statistics_bs(type_sms, user_id=self.user_id)
        self.user_info_update()
        return

    def add_achievements_bs_profile(self, score: int, text, time_issuing, admin_id, achievements_type):
        warn = "achievements"
        if not self.user_info[1].get(warn):
            self.user_info[1][warn] = {
                "1": {
                    "status": True,
                    "text": text,
                    "score": score,
                    "time_issuing": time_issuing,
                    "admin_id": admin_id,
                    "type": achievements_type
                },
                "count": 1,
            }
            self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
                                            {
                                                '$set': {
                                                    warn: self.user_info[1][warn]
                                                }
                                            })
        else:
            self.user_info[1][warn][str(self.user_info[1][warn]["count"])] = {
                "status": True,
                "text": text,
                "score": score,
                "time_issuing": time_issuing,
                "admin_id": admin_id,
                "type": achievements_type
            }
            self.user_info[1][warn]["count"] += 1

        self.user_info[2].save(self.user_info[1])

        self.user_info_update()
        self.add_statistics_bs(warn)

        return self.user_info[1][warn]["count"]


    def update_rep(self, start_time, reps, access_amount):
        sl = reps.copy()
        k = 0
        gg = []
        print(sl)
        for i in enumerate(reps):
            if i[1]["end_time"] < start_time:
                if k > access_amount:pass
                    #print(i[0])
                    #del sl[i[0]]
                else:
                    #sl[i[0]] = {"status": True, "start_time": 0, "end_time": 0}
                    gg.append({"status": True, "start_time": 0, "end_time": 0})
            elif k > access_amount:pass
                #del sl[i[0]]
            else:
                gg.append(i[1])
            k += 1
        if access_amount > len(sl):
            for i in range(len(sl), access_amount):
                gg.append({"status": True, "start_time": 0, "end_time": 0})
                #sl.append({"status": True, "start_time": 0, "end_time": 0})
        return gg


    def plus_rep(self, access_amount, number_issued, start_time, plus, warn="rep_plus_new"):
        #warn = "rep_plus"
        if not self.user_info[1].get(warn):
            # self.user_info[1][warn] = {
            #     "1": {
            #         "status": True,
            #         "text": text,
            #         "score": score,
            #         "time_issuing": time_issuing,
            #         "admin_id": admin_id
            #     },
            #     "count": 1,
            # }
            sl = []
            kk = 0
            for i in range(0, access_amount):
                if i < number_issued:
                    sl.append({"status": True, "start_time": start_time, "end_time": start_time + plus})
                    kk += 1
                else:
                    sl.append({"status": True, "start_time": 0, "end_time": 0})
            self.user_info[1][warn] = {
                "reps": sl,
                "access_amount": access_amount,
                "count": kk
            }
            self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
                                         {
                                             '$set': {
                                                 warn: self.user_info[1][warn]
                                             }
                                         })
        else:
            kk = 0
            k = 1
            #sl = self.user_info[1][warn].copy()
            sl = self.update_rep(start_time, self.user_info[1][warn]["reps"], access_amount)
            sll = sl.copy()
            for i in enumerate(sl):
                if kk < number_issued:
                    if i[1]["end_time"] < start_time:
                        sll[i[0]] = {"status": True, "start_time": start_time, "end_time": start_time + plus}
                        kk += 1
                else:
                    break
                k += 1
            if kk == 0:
                return -1
            self.user_info[1][warn]["count"] += kk
            self.user_info[1][warn]["access_amount"] = access_amount
            self.user_info[1][warn]["reps"] = sll
            # self.user_info[1][warn] = {
            #     "reps": sl,
            #     "access_amount": access_amount
            # }

            # for i in enumerate(self.user_info[1][warn]["reps"]):
            #     if i[1]["status"] == True:
            #         if i[1]["end_time"] < start_time:
            #             sl[i[0]] = {"status": True, "start_time": 0, "end_time": 0}
            #             k += 1
            #         #sl[i[0]][""]
            #     kk += 1



            # self.user_info[1][warn][str(self.user_info[1][warn]["count"])] = {
            #     "status": True,
            #     "text": text,
            #     "score": score,
            #     "time_issuing": time_issuing,
            #     "admin_id": admin_id
            # }
            # self.user_info[1][warn]["count"] += 1

        self.user_info[2].save(self.user_info[1])

        self.user_info_update()
        self.add_statistics_bs(warn)

        return kk

    def add_roulette(self, access_amount, number_issued, start_time, plus, result, warn='roulette'):
        if not self.user_info[1].get(warn):
            # self.user_info[1][warn] = {
            #     "1": {
            #         "status": True,
            #         "text": text,
            #         "score": score,
            #         "time_issuing": time_issuing,
            #         "admin_id": admin_id
            #     },
            #     "count": 1,
            # }
            sl = []
            kk = 0
            for i in range(0, access_amount):
                if i < number_issued:
                    sl.append({"status": True, "start_time": start_time, "end_time": start_time + plus})
                    kk += 1
                    end_time = start_time + plus
                else:
                    sl.append({"status": True, "start_time": 0, "end_time": 0})
            if not result:
                self.user_info[1][warn] = {
                    "roulettes": sl,
                    "access_amount": access_amount,
                    "count": 0
                }
            else:
                self.user_info[1][warn] = {
                    "roulettes": sl,
                    "access_amount": access_amount,
                    "count": kk
                }
            self.user_info[2].update_one({'_id': self.user_info[1]['_id']},
                                         {
                                             '$set': {
                                                 warn: self.user_info[1][warn]
                                             }
                                         })
        else:
            kk = 0
            k = 1
            #sl = self.user_info[1][warn].copy()
            sl = self.update_rep(start_time, self.user_info[1][warn]["roulettes"], access_amount)
            sll = sl.copy()
            for i in enumerate(sl):
                if kk < number_issued:
                    if i[1]["end_time"] < start_time:
                        sll[i[0]] = {"status": True, "start_time": start_time, "end_time": start_time + plus}
                        kk += 1
                        end_time = start_time + plus
                else:
                    break
                k += 1
            if kk == 0:
                return self.user_info[1][warn]["roulettes"][len(self.user_info[1][warn]["roulettes"]) - 1]["end_time"]
            if result:
                #kk = 0
                self.user_info[1][warn]["count"] += kk
            self.user_info[1][warn]["access_amount"] = access_amount
            self.user_info[1][warn]["roulettes"] = sll
            kk = k


        self.user_info[2].save(self.user_info[1])

        self.user_info_update()
        self.add_statistics_bs(warn)

        return end_time


if __name__ == "__main__":
    # s = (-13 * 2) / 1000
    # print(s)
    #us = user_profile(12)
    #us.change_score_bs_profile(-1)
    #us.add_warn_bs_profile(2399943, 999, "дд", 76765)
    #us.add_warn_bs_profile(7689986, 45876876, "gg", 333)
    #us.change_info_bs_profile(test=True)
    #us.add_statistics_bs("text_spam", True)

    score = -7
    reputation_minus = {
        (20, 999): 0.05,
        (6, 20): 0.03,
        (0, 5): 0.01,
        (0, -5): 0.03,
        (-6, -10): -0.05,
        (-10, -999): -0.07
    }

    if score < 0:

        for i in reputation_minus:
            #print(i)
            if i[1] <= score <= i[0]:
                print(i)
