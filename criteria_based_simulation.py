import numpy as np
import pandas as pd

from generator import generate_responses_gt
from helpers.utils import run_quiz_criteria_confm, get_loss_dong
from m_run import get_loss_cost_mrun
from sm_run import get_loss_cost_smrun

if __name__ == '__main__':
    z = 0.3
    cr = 5
    n_papers = 500
    papers_page = 10
    criteria_power = [0.14, 0.14, 0.28, 0.42]
    criteria_difficulty = [1., 1., 1.1, 0.9]
    criteria_num = len(criteria_power)
    fr_p_part = 0.1
    data = []
    for Nt in range(1, 11, 1):
        for J in [2, 3, 5, 10]:
    # for Nt in [3]:
    #     for J in [5]:
            print 'Nt: {}. J: {}'.format(Nt, J)
            cost_baseline = (Nt + papers_page * criteria_num) * J / float(papers_page)
            loss_baseline_list = []
            fi_b, fe_b, rec_b, pre_b = [], [], [], []
            loss_mrun_list = []
            cost_mrun_list = []
            fi_m, fe_m, rec_m, pre_m = [], [], [], []
            loss_smrun_list = []
            cost_smrun_list = []
            fi_sm, fe_sm, rec_sm, pre_sm = [], [], [], []
            for _ in range(10):
                # quiz, generation responses
                acc = run_quiz_criteria_confm(Nt, z, [1.])
                responses, GT = generate_responses_gt(n_papers, criteria_power, papers_page,
                                                      J, acc, criteria_difficulty)
                # baseline
                loss_baseline, fi_rate_b, fe_rate_b, rec_b_, pre_b_ = get_loss_dong(responses, criteria_num, n_papers,
                                                                                    papers_page, J, GT, cr)
                loss_baseline_list.append(loss_baseline)
                fi_b.append(fi_rate_b)
                fe_b.append(fe_rate_b)
                rec_b.append(rec_b_)
                pre_b.append(pre_b_)
                # m-run
                loss_mrun, cost_mrun, fi_rate_m, fe_rate_m, rec_m_, \
                pre_m_ = get_loss_cost_mrun(criteria_num, n_papers, papers_page, J, cr, Nt, acc,
                                            criteria_power, criteria_difficulty, GT, fr_p_part)
                loss_mrun_list.append(loss_mrun)
                cost_mrun_list.append(cost_mrun)
                fi_m.append(fi_rate_m)
                fe_m.append(fe_rate_m)
                rec_m.append(rec_m_)
                pre_m.append(pre_m_)
                # sm-run
                loss_smrun, cost_smrun, fi_rate_sm, fe_rate_sm, \
                rec_sm_, pre_sm_ = get_loss_cost_smrun(criteria_num, n_papers, papers_page, J, cr, Nt, acc,
                                                       criteria_power, criteria_difficulty, GT, fr_p_part)
                loss_smrun_list.append(loss_smrun)
                cost_smrun_list.append(cost_smrun)
                fi_sm.append(fi_rate_sm)
                fe_sm.append(fe_rate_sm)
                rec_sm.append(rec_sm_)
                pre_sm.append(pre_sm_)
            print 'BASELINE  loss: {:1.2f}, price: {:1.2f}, fi_rate: {:1.2f}, fe_rate: {:1.2f}, ' \
                  'recall: {:1.2f}, precision: {:1.2f}'.\
                format(np.mean(loss_baseline_list), cost_baseline, np.mean(fi_b), np.mean(fe_b),
                       np.mean(rec_b), np.mean(pre_b))

            print 'M-RUN     loss: {:1.2f}, price: {:1.2f}, fi_rate: {:1.2f}, fe_rate: {:1.2f}, ' \
                  'recall: {:1.2f}, precision: {:1.2f}'.\
                format(np.mean(loss_mrun_list), np.mean(cost_mrun_list), np.mean(fi_m), np.mean(fe_m),
                       np.mean(rec_m), np.mean(pre_m))

            print 'SM-RUN    loss: {:1.2f}, price: {:1.2f}, fi_rate: {:1.2f}, fe_rate: {:1.2f}, ' \
                  'recall: {:1.2f}, precision: {:1.2f}'.\
                format(np.mean(loss_smrun_list), np.mean(cost_smrun_list), np.mean(fi_sm), np.mean(fe_sm),
                       np.mean(rec_sm), np.mean(pre_sm))
            print '---------------------'

            data.append([Nt, J, cr, np.mean(loss_baseline_list), np.std(loss_baseline_list),
                         np.mean(fi_b), np.mean(fe_b), cost_baseline, 0., 'Baseline',
                         np.mean(rec_b), np.mean(pre_b)])
            data.append([Nt, J, cr, np.mean(loss_mrun_list), np.std(loss_mrun_list), np.mean(fi_m),
                         np.mean(fe_m), np.mean(cost_mrun_list), np.std(cost_mrun_list), 'M-runs',
                         np.mean(rec_m), np.mean(pre_m)])
            data.append([Nt, J, cr, np.mean(loss_smrun_list), np.std(loss_smrun_list), np.mean(fi_sm),
                         np.mean(fe_sm), np.mean(cost_smrun_list), np.std(cost_smrun_list), 'SM-runs',
                         np.mean(rec_sm), np.mean(pre_sm)])
    pd.DataFrame(data, columns=['Nt', 'J', 'lr', 'loss_mean', 'loss_std', 'fi_rate', 'fe_rate',
                                'price_mean', 'price_std', 'alg', 'recall', 'precision']). \
                                to_csv('output/data/loss_tests_cr5.csv', index=False)
