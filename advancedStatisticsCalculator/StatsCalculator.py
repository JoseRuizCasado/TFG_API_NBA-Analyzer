def team_off_rtg(tm_pts, fga, fgm, tov, fta, oreb, opp_dreb):
    return 100 * (tm_pts / team_poss(fga, fgm, tov, fta, oreb, opp_dreb))


def team_poss(fga, fgm, tov, fta, oreb, opp_dreb):
    return fga - ((oreb / (oreb + opp_dreb)) * (fga - fgm) * 1.07) + tov + 0.4 * fta


def team_scoring_poss(fgm, fta, ft_per):
    return fgm + (1 - (1 - ft_per) ** 2) * fta * 0.4


def team_plays(fga, fta, tov):
    return fga + fta * 0.4 + tov


def team_play_per(fgm, fga, fta, ft_per, tov):
    return team_scoring_poss(fgm, fta, ft_per) / team_plays(fga, fta, tov)


def player_off_rtg_floor_per(pts, mins, fgm, fga, fg3m, ftm, fta, ft_per, oreb, ast, tov,
                             tm_pts, tm_min, tm_fgm, tm_fga, tm_fg3m, tm_ftm, tm_fta, tm_ft_per, tm_oreb,
                             tm_ast, tm_tov, tm_oreb_per):
    q5 = 1.14 * ((tm_ast - ast) / tm_fgm)
    q12 = ((tm_ast / tm_min) * mins * 5 - ast) / ((tm_fgm / tm_min) * mins * 5 - fgm)
    qast = ((5 * mins) / tm_min) * q5 + (1 - ((5 * mins) / tm_min)) * q12
    fg_part = fgm * (1 - 0.5 * ((pts - ftm) / (2 * fga))) * qast

    ast_part = 0.5 * (((tm_pts - tm_ftm) - (pts - ftm)) / (2 * (tm_fga - fga))) * ast

    ft_part = (1 - (1 - ft_per) ** 2) * 0.4 * fta

    tm_play_per = team_play_per(tm_fgm, tm_fga, tm_fta, tm_ft_per, tm_tov)
    tm_oreb_weight = ((1 - tm_oreb_per) * tm_play_per) \
                     / ((1 - tm_oreb_per) * tm_play_per + tm_oreb_per * (1 - tm_play_per))
    or_part = oreb * tm_oreb_weight * tm_play_per

    scoring_possessions = ((fg_part + ast_part + ft_part)
                           * (1 -
                              (tm_oreb / team_scoring_poss(tm_fgm, tm_fta, tm_ft_per)) * tm_oreb_weight * tm_play_per))\
                          + or_part
    missed_fg_part = (fga - fgm) * (1 - 1.07 * tm_oreb_per)
    missed_ft_part = ((1 - ft_per)**2) * 0.4 * fta
    possessions = scoring_possessions + missed_fg_part + missed_ft_part + tov

    fg_pp_part = 2 * (fgm + 0.5 * fg3m) * (1 - 0.5 * ((pts - ftm) / (2 * fga)) * qast)
    ast_pp_part = 2 * ((tm_fgm - fgm + 0.5 * (tm_fg3m - fg3m)) / (tm_fgm - fgm)) * 0.5 \
                  * (((tm_pts - tm_ftm) - (pts - ftm)) / (2 * (tm_fga - fga))) * ast
    or_pp_part = oreb * tm_oreb_weight * tm_play_per * (tm_pts / (tm_fgm + (1 - (1 - tm_ft_per)**2) * 0.4 * tm_fta))
    points_produced = ((fg_pp_part + ast_pp_part + ft_part)
                       * (1 - (tm_oreb / team_scoring_poss(tm_fgm, tm_fta, tm_ft_per)) * tm_oreb_weight * tm_play_per))\
                      + or_pp_part

    return (100 * (points_produced / possessions)), (scoring_possessions / possessions)


def team_floor_per(fga, fgm, tov, fta, ftm, oreb, opp_dreb):
    return team_scoring_poss(fgm, fta, ftm / fta) / team_poss(fga, fgm, tov, fta, oreb, opp_dreb)


def team_def_rtg(op_pts, fga, fgm, tov, fta, oreb, opp_dreb):
    return 100 * (op_pts / team_poss(fga, fgm, tov, fta, oreb, opp_dreb))


def player_def_rtg(mins, dreb, stl, blk, pf,
                   tm_min, tm_fgm, tm_fga, tm_dreb, tm_blk, tm_tov, tm_fta, tm_oreb, tm_stl, tm_pf, tm_df_rtg,
                   opp_pts, opp_fgm, opp_fga, opp_ftm, opp_fta, opp_oreb, opp_dreb, opp_tov):
    d_pts_per_poss = opp_pts / (opp_fgm + (1 - (1 - (opp_ftm / opp_fta))**2) * opp_fta * 0.4)

    opp_off_reb_per = team_off_rebound_per(opp_oreb, tm_dreb) / 100
    opp_fg_per = opp_fgm / opp_fga
    fm_wt = (opp_fg_per * (1 - opp_off_reb_per)) / \
            ((opp_fg_per * (1 - opp_off_reb_per)) + (1 - opp_fg_per) * opp_off_reb_per)
    stop1 = stl + blk * fm_wt * (1 - 1.07 * opp_off_reb_per) + dreb * (1 - fm_wt)
    stop2 = (((opp_fga - opp_fgm - tm_blk) / tm_min) * fm_wt * (1 - 1.07 * opp_off_reb_per)
             + ((opp_tov - tm_stl) / tm_min)) * mins \
            + (pf / tm_pf) * 0.4 * opp_fta * (1 - (opp_ftm / opp_fta))**2
    stops = stop1 + stop2
    stops_per = (stops * tm_min) / (team_poss(tm_fga, tm_fgm, tm_tov, tm_fta, tm_oreb, opp_dreb) * mins)

    return tm_df_rtg + 0.2 * (100 * d_pts_per_poss * (1 - stops_per) - tm_df_rtg)


def team_pace(tm_min, fga, fgm, tov, fta, oreb, opp_dreb, opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, dreb):
    return 48 * ((team_poss(fga, fgm, tov, fta, oreb, opp_dreb)
                  + team_poss(opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, dreb)) / (2 * tm_min))


def true_shooting_per(pts, fga, fta):
    return pts / ((2 * fga) + (0.44 * fta))


def effective_field_goals_per(two_fgm, three_fgm, fga):
    return (two_fgm + (1.5 * three_fgm)) / fga


def free_throws_att_rate(fta, fga):
    return fta / fga


def three_field_goals_att_rate(three_fga, fga):
    return three_fga / fga


def team_off_rebound_per(oreb, opp_dreb):
    return 100 * (oreb / (oreb + opp_dreb))


def player_off_rebound_per(mins, oreb, tm_mins, tm_oreb, opp_dreb):
    return 100 * ((oreb * (tm_mins / 5)) / (mins * (tm_oreb + opp_dreb)))


def team_def_rebound_per(dreb, opp_oreb):
    return 100 * (dreb / (dreb + opp_oreb))


def player_def_rebound_per(mins, dreb, tm_mins, tm_dreb, opp_oreb):
    return 100 * ((dreb * (tm_mins / 5)) / (mins * (tm_dreb + opp_oreb)))


def team_blocks_per(blk, opp_fga, opp_3fga):
    return 100 * (blk / (opp_fga - opp_3fga))


def player_blocks_per(mins, blk, tm_min, opp_fga, opp_3fga):
    return 100 * ((blk * (tm_min / 5)) / (mins * (opp_fga - opp_3fga)))


def turnovers_per(tov, fga, fta):
    return 100 * (tov / (fga + 0.44 * fta + tov))


def team_assists_per(ast, fgm):
    return 100 * (ast / fgm)


def player_assists_per(mins, fgm, ast, tm_mins, tm_fgm):
    return 100 * (ast / (((mins * 5 / tm_mins) * tm_fgm) - fgm))


def team_steals_per(stl, opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, dreb):
    return 100 * (stl / team_poss(opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, dreb))


def player_steals_per(mins, stl, tm_mins, opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, tm_dreb):
    return 100 * (stl * (tm_mins / 5) / (mins * team_poss(opp_fga, opp_fgm, opp_tov, opp_fta, opp_oreb, tm_dreb)))


def usage_per(mins, fga, fta, tov, tm_min, tm_fga, tm_fta, tm_tov):
    return 100 * (((fga + 0.44 * fta + tov) * (tm_min / 5)) / (mins * (tm_fga + 0.44 * tm_fta + tm_tov)))
