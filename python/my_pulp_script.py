import pandas as pd
import pulp

def hiryou_pulp(c_yasai,c_hiryou,custom_yasai,custom_hiryou):

    #元データの定義
    hiryou_data = {
    'hiryou': ['牛ふん堆肥', '発酵鶏ふん', '豚ふん堆肥', '油かす', '魚粉', '骨粉', '米ぬか', 'もみ殻', '草木灰', '腐葉土',
               '化成肥料(8-8-8)', '高度化成(14-14-14)', '尿素', '硫安', '塩安', '石灰窒素', '過りん酸石灰',
               'よう成りん肥', '塩化加里', '硫酸加里'],
    'Price': [0.084740741, 0.1211, 0.125, 0.3978, 1.386266094, 0.4836, 1.48, 0.408333333, 1.02,
              0.101851852, 0.566666667, 1.078, 0.764, 0.427142857, 1.98, 0.856, 1.457142857,
              0.5455, 0.264, 0.524285714],
    'N': [0.018, 0.02, 0.0161, 0.03, 0.06, 0.04, 0.0269, 0.0032, 0, 0.0084, 0.08, 0.14, 0.46,
          0.21, 0.25, 0.2, 0, 0, 0, 0],
    'P': [0.025, 0.067, 0.0211, 0.07, 0.06, 0.16, 0.0234, 0.0003, 0.19, 0.0008, 0.08, 0.14, 0,
          0, 0, 0, 0.175, 0.2, 0, 0],
    'K': [0.024, 0.045, 0.0133, 0.04, 0, 0, 0.0176, 0.0031, 0.14, 0.0042, 0.08, 0.14, 0, 0, 0,
          0, 0, 0, 0.6, 0.5]
    }

    hiryou_df = pd.DataFrame(hiryou_data)

    # Pydanticモデルから辞書への変換
    custom_hiryou_dict = custom_hiryou

    # その後、リストに変換
    custom_hiryou_list = list(zip(*[custom_hiryou_dict[key] for key in ['hiryou', 'Price', 'N', 'P', 'K']]))
    custom_hiryou_df = pd.DataFrame(custom_hiryou_list, columns=['hiryou', 'Price', 'N', 'P', 'K'])

    # 既存のデータフレームに追加
    hiryou_df = pd.concat([hiryou_df, custom_hiryou_df], ignore_index=True)

    yasai_data = {
    'yasai': ['きゅうり', 'トマト', 'ナス', 'ピーマン', 'イチゴ', 'とうもろこし', 'さやえんどう', 'インゲン', '枝豆',
              '白菜', 'キャベツ', 'カリフラワー', 'ブロッコリー', '小松菜', 'レタス', 'ほうれん草', '春菊',
              '玉ねぎ', 'ねぎ', 'サトイモ', 'ジャガイモ', 'かぼちゃ', 'さつまいも', 'カブ', '大根', 'ニンジン'],
    'N': [49, 48, 52, 46, 44, 51, 31, 22, 24, 44, 51, 48, 30, 27.5, 44, 52, 50, 44, 44, 48, 15, 44, 21, 10, 12, 8],
    'P': [70, 71, 82, 67, 70, 60, 55.5, 34, 35, 62, 68, 64, 39, 30.75, 62, 66, 62, 70, 64, 64, 16, 60, 33, 8, 10, 14],
    'K': [58, 58, 64, 58, 56, 58, 40, 32, 30, 56, 58, 60, 34, 30, 52, 60, 60, 54, 52, 62, 18, 52, 39, 10, 8, 8],
    'W': [2000, 2000, 2000, 2000, 2000, 2000, 1500, 1000, 1000, 2000, 2000, 2000, 1000, 750, 2000, 2000, 2000, 2000, 2000, 2000, 0, 2000, 1000, 0, 0, 0]
    }

    yasai_df = pd.DataFrame(yasai_data)

    # custom_yasai を組み込む
    if custom_yasai:
        # Pydanticモデルから辞書への変換
        custom_yasai_dict = custom_yasai.dict()
        # その後、リストに変換
        custom_yasai_list = list(zip(*[custom_yasai_dict[key] for key in ['yasai', 'N', 'P', 'K', 'W']]))
        custom_yasai_df = pd.DataFrame(custom_yasai_list, columns=['yasai', 'N', 'P', 'K', 'W'])

        # 既存のデータフレームに追加
        yasai_df = pd.concat([yasai_df, custom_yasai_df], ignore_index=True)


    #リストへ変換
    hiryou = hiryou_df["hiryou"].tolist()
    yasai = yasai_df["yasai"].tolist()

    #計算の定数として定義
    cost = {row.hiryou:row.Price for row in hiryou_df.itertuples()}
    require = {row.yasai:(row.N, row.P, row.K, row.W) for row in yasai_df.itertuples()}
    nutrition = {row.hiryou:(row.N, row.P, row.K,) for row in hiryou_df.itertuples()}
    print(nutrition)
    #yasai
    c_yasai_req=require[c_yasai]
    c_yasai_N=c_yasai_req[0]
    c_yasai_P=c_yasai_req[1]
    c_yasai_K=c_yasai_req[2]
    c_yasai_W=c_yasai_req[3]
    #hiryou
    c_hiryo_list_N=[]
    c_hiryo_list_P=[]
    c_hiryo_list_K=[]
    for h in c_hiryou:
        nutirition_sample=nutrition[h]
        c_hiryo_list_N.append(nutirition_sample[0])
        c_hiryo_list_P.append(nutirition_sample[1])
        c_hiryo_list_K.append(nutirition_sample[2])



    #計算
    problem = pulp.LpProblem('LP2', pulp.LpMinimize)
    #変数
    x = pulp.LpVariable.dicts('x', c_hiryou, cat='Continuous')

    #制約条件
    #各々の肥料は0～10㎏の範囲
    for h in c_hiryou:
        problem += x[h] >= 0
        problem += x[h] <= 10000

    #各々の成分誤差は0.1%以内
    problem += pulp.lpSum(c_hiryo_list_N[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) <= c_yasai_N+0.1
    problem += pulp.lpSum(c_hiryo_list_N[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) >= c_yasai_N-0.1
    problem += pulp.lpSum(c_hiryo_list_P[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) <= c_yasai_P+0.1
    problem += pulp.lpSum(c_hiryo_list_P[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) >= c_yasai_P-0.1
    problem += pulp.lpSum(c_hiryo_list_K[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) <= c_yasai_K+0.1
    problem += pulp.lpSum(c_hiryo_list_K[i]*x[c_hiryou[i]] for i in range(len(c_hiryou))) >= c_yasai_K-0.1

    #肥料の合計重量はc_yasai_W（2㎏ぐらい）以上→有機質考慮
    problem +=pulp.lpSum([x[h] for h in c_hiryou])>=c_yasai_W

    #目的関数（肥料の総費用）
    problem += pulp.lpSum([cost[h]*x[h] for h in c_hiryou])

    #解く
    status = problem.solve()


    #計算結果
    status = pulp.LpStatus[status]

    hituyouryou_change=[]

    for h in c_hiryou:
        hituyouryou_change.append(x[h].value())

    sum_costs = problem.objective.value()

    saiteki_NPKW = [
        sum(c_hiryo_list_N[i]*x[c_hiryou[i]].value() for i in range(len(c_hiryou))),
        sum(c_hiryo_list_P[i]*x[c_hiryou[i]].value() for i in range(len(c_hiryou))),
        sum(c_hiryo_list_K[i]*x[c_hiryou[i]].value() for i in range(len(c_hiryou))),
        sum(x[h].value() for h in c_hiryou)
    ]

    risou_NPKW = [
        c_yasai_N,
        c_yasai_P,
        c_yasai_K,
        c_yasai_W,
    ]

    df_c2 = {
        'status': status,
        '肥料名': c_hiryou,
        '野菜名': c_yasai,
        '必要な量': hituyouryou_change,
        '最適化後NPKW': saiteki_NPKW,
        '理想量': risou_NPKW,
        '総費用': sum_costs*0.5,
        'カスタム野菜': custom_yasai,
        'カスタム肥料': custom_hiryou,
    }

    return df_c2
