"""
Plot are present in the final notebook.
"""

from common_utils import *
def gen_plot(obj):
    gen_plot_rew(obj)
    gen_plot_runningAvg(obj)
    gen_plot_Eps_T_U(obj)

"""
A generic function to create plots and save them at the provided path.
"""
def gen_basic_plot(items_count, var, path, x_label = '', y_label = ''):
    if items_count is None:
        plt.plot(var,'.')
    else:
        for i in range(items_count):
            plt.plot(var[i],'.')

    
    plt.rc('ytick', labelsize=18)
    plt.rc('xtick', labelsize=18)

    plt.ylabel(y_label,fontsize=22)
    plt.xlabel(x_label,fontsize=22)
    # plt.xticks([10000,20000,30000,40000,50000,60000,70000,80000],['10','20','30','40','50', '60', '70', '80'])
    plt.tight_layout()

    if common_RUNNING_ON_COLAB:
        plt.show()
    else:
        plt.savefig(path)
    plt.clf()

def gen_basic_bar_plot(path,x, y, yerr,  x_label = '', y_label = ''):
    plt.clf()

    # plt.rcParams['axes.axisbelow'] = True
    # plt.rc('axes', axisbelow=True)

    plt.bar(x ,y, yerr=yerr, align='center', alpha=0.8, ecolor='black', capsize=10, width=0.5, color=['hotpink','lightblue','lightgreen','gold','bisque'], edgecolor='k', zorder = 10000)
    plt.rc('ytick', labelsize=18)
    plt.rc('xtick', labelsize=18)
    
    plt.ylabel(y_label,fontsize=22)
    plt.xlabel(x_label,fontsize=22)
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.7, zorder = -10000)

    # plt.rcParams['axes.axisbelow'] = True
    # plt.rc('axes', axisbelow=True)

    if common_RUNNING_ON_COLAB:
        plt.show()
    else:
        plt.savefig(path)

def gen_plot_rew(obj, dir):
    path = dir + "Reward.jpg"
    gen_basic_plot(obj.numUsers, obj.Rewards, path, x_label = 'Reward', y_label = 'No. of Iterations, x10^3')
        
def gen_plot_runningAvg(obj, dir):
        path = dir + "RunningAvg.jpg"
        gen_basic_plot(obj.numUsers, obj.runningAvg, path, x_label = 'Reward, Running Average', y_label = 'No. of Iterations, x10^3')

def gen_plot_Eps_T_U(obj, dir):
        
        for u in range(obj.numUsers):
          if u>0:
            break
          for s in range(obj.numStatesPerUser):
            tag = "NS"
            if s in obj.rsList:
                tag = "RS"
            plt.plot(obj.ALL_ANOMALY_SAMPL_DISTR[u, s, :][:-2])
            y_l = 'Eps Hat for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel(y_l)
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "EpsHat"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

            plt.plot(obj.T_ANOMALY_T[u, s, :][:-2])
            y_l = 'T Anomaly for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel(y_l)
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "T_Anomaly"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

            plt.plot(obj.U_NORMAL_T[u, s, :][:-2])
            y_l = 'U Norm for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel(y_l)
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "U_Normal"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

def gen_plot_Eps(obj, dir):
        
        for u in range(obj.numUsers):
          if u>0:
            break
          for s in range(obj.numStatesPerUser):
            tag = "NS"
            if s in obj.rsList:
                tag = "RS"
            plt.plot(obj.ALL_ANOMALY_SAMPL_DISTR[u, s, :][:-2])
            y_l = 'Eps Hat for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel(y_l)
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "EpsHat"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

def gen_plot_T(obj, dir):
        
        for u in range(obj.numUsers):
          if u>0:
            break
          for s in range(obj.numStatesPerUser):
            tag = "NS"
            if s in obj.rsList:
                tag = "RS"
            plt.plot(obj.T_ANOMALY_T[u, s, :][:-2])
            y_l = 'T Anomaly for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel('')
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "T_Anomaly"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

def gen_plot_U(obj, dir):
        
        for u in range(obj.numUsers):
          if u>0:
            break
          for s in range(obj.numStatesPerUser):
            tag = "NS"
            if s in obj.rsList:
                tag = "RS"
            plt.plot(obj.U_NORMAL_T[u, s, :][:-2])
            y_l = 'U Norm for U:'+str(u)+", S:"+str(s) + tag
            plt.ylabel(y_l)
            plt.xlabel('No. of Iterations, 10^3')
            # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
            if common_RUNNING_ON_COLAB:
                plt.show()
            else:
                name = dir + "U_Normal"+"_U_"+str(u)+"_S_"+str(s)+".jpg"
                plt.savefig(name)
            plt.clf()

def gen_online_plots(online_obj, dir, print_only = False):
    if not print_only:
        path = dir + "Online_Reward.jpg"
        gen_basic_plot(None, online_obj.Reward_online, path, x_label = 'Online Reward', y_label = 'No. of Iterations, x10^3')

        path = dir + "Online_Running_Avg.jpg"
        gen_basic_plot(None, online_obj.runningAvg_online, path, x_label = 'Reward, Running Average', y_label = 'No. of Iterations, x10^3')

    print('avg reward across time', online_obj.mean_Reward_online)
    
    print('mean RE reward', online_obj.mean_REreward_online)
    # if online_obj.mean_REmigration_online > 0:
    print(' mean RE migration', online_obj.mean_REmigration_online)
    # else:
    #     print("**NO RE MIGR COST**")
    # if (online_obj.mean_REdelay_online) > 0:
    print(' mean RE delay', (online_obj.mean_REdelay_online))
    # else:
    #     print("**NO RE DELAY COST**")
    # if (online_obj.mean_REstorage_online) > 0:
    print(' mean RE storage', (online_obj.mean_REstorage_online))
    # else:
    #     print("**NO RE STORAGE COST**")
    # if (online_obj.mean_REcompDelay_online) > 0:
    print(' mean RE Comp Cost:', (online_obj.mean_REcompDelay_online))
    # else:
    #     print("**NO RE COMP_DELAY COST**")
    
    print('mean NS reward', (online_obj.mean_NSreward_online))
    # if (online_obj.mean_NSmigration_online) > 0:
    print(' mean NS migration', (online_obj.mean_NSmigration_online))
    # else:
    #     print("**NO NS MIGR COST**")
    # if (online_obj.mean_NSdelay_online) > 0:
    print(' mean NS delay', (online_obj.mean_NSdelay_online))
    # else:
    #     print("**NO NS DELAY COST**")
    # if (online_obj.mean_NSstorage_online) > 0:
    print(' mean NS storage', (online_obj.mean_NSstorage_online))
    # else:
    #     print("**NO NS STORAGE COST**")
    # if (online_obj.mean_NScompDelay_online) > 0:
    print(' mean RE Comp Cost:', (online_obj.mean_NScompDelay_online))
    # else:
    #     print("**NO RE COMP_DELAY COST**")

    # print('avg reward across time', np.mean(online_obj.Reward_online))
    
    # print('mean RE reward', mean(online_obj.REreward_online))
    # if len(online_obj.REmigration_online) > 0:
    #     print(' mean RE migration', mean(online_obj.REmigration_online))
    # else:
    #     print("**NO RE MIGR COST**")
    # if len(online_obj.REdelay_online) > 0:
    #     print(' mean RE delay', mean(online_obj.REdelay_online))
    # else:
    #     print("**NO RE DELAY COST**")
    # if len(online_obj.REstorage_online) > 0:
    #     print(' mean RE storage', mean(online_obj.REstorage_online))
    # else:
    #     print("**NO RE STORAGE COST**")
    # if len(online_obj.REcompDelay_online) > 0:
    #     print(' mean RE Comp Cost:', mean(online_obj.REcompDelay_online))
    # else:
    #     print("**NO RE COMP_DELAY COST**")
    
    # print('mean NS reward', mean(online_obj.NSreward_online))
    # if len(online_obj.NSmigration_online) > 0:
    #     print(' mean NS migration', mean(online_obj.NSmigration_online))
    # else:
    #     print("**NO NS MIGR COST**")
    # if len(online_obj.NSdelay_online) > 0:
    #     print(' mean NS delay', mean(online_obj.NSdelay_online))
    # else:
    #     print("**NO NS DELAY COST**")
    # if len(online_obj.NSstorage_online) > 0:
    #     print(' mean NS storage', mean(online_obj.NSstorage_online))
    # else:
    #     print("**NO NS STORAGE COST**")
    # if len(online_obj.NScompDelay_online) > 0:
    #     print(' mean RE Comp Cost:', mean(online_obj.NScompDelay_online))
    # else:
    #     print("**NO RE COMP_DELAY COST**")

def generate_bar_graphs(coalated_results, dir):
    x = ['ImDQL', 'QL-NIS', 'QL-WBA', 'QL-RES', 'GRD']
    
    path = dir + "rewards.jpg"
    y = []
    yerr = []
    for algo in ALGO_NAMES:
        y.append(-1*coalated_results.algo_names_to_objects[algo].mean_Reward_online)
        yerr.append(coalated_results.algo_names_to_objects[algo].stdev_Reward_online)
    gen_basic_bar_plot(path,x, y, yerr,  x_label = 'Algorithm', y_label = 'Average Cost')

    path = dir + "re_rewards.jpg"
    y = []
    yerr = []
    for algo in ALGO_NAMES:
        y.append(-1*coalated_results.algo_names_to_objects[algo].mean_REreward_online)
        yerr.append(coalated_results.algo_names_to_objects[algo].stdev_REreward_online)
    gen_basic_bar_plot(path,x, y, yerr,  x_label = 'Algorithm', y_label = 'Average Cost, Rare State')

    path = dir + "ns_rewards.jpg"
    y = []
    yerr = []
    for algo in ALGO_NAMES:
        y.append(-1*coalated_results.algo_names_to_objects[algo].mean_NSreward_online)
        yerr.append(coalated_results.algo_names_to_objects[algo].stdev_NSreward_online)
    gen_basic_bar_plot(path,x, y, yerr,  x_label = 'Algorithm', y_label = 'Average Cost, Normal State')

def generate_basic_line_plots(path, x, y, x_label = '', y_label = ''):
    plt.clf()
    plt.plot(x, y, marker = "o", c = "r")
    plt.rc('ytick', labelsize=18)
    plt.rc('xtick', labelsize=18)

    plt.ylabel(y_label,fontsize=22)
    plt.xlabel(x_label,fontsize=22)
    
    plt.tight_layout()
    plt.grid(True)
    
    if common_RUNNING_ON_COLAB:
        plt.show()
    else:
        plt.savefig(path)

def generate_risk_aware_n_risk_taking_graphs(etas_to_models_mapping, dir):
    etas = etas_to_models_mapping.keys()
    sorted(etas)
    tot_rew = []
    ns_rew = []
    re_rew = []
    for eta in etas:
        obj = etas_to_models_mapping[eta]
        tot_rew.append(obj.mean_Reward_online)
        ns_rew.append(obj.mean_NSreward_online)
        re_rew.append(obj.mean_REreward_online)
    
    generate_basic_line_plots(dir + "tot_rew.jpg", etas, tot_rew, x_label = 'Algorithm', y_label = 'Average Cost, Total')
    generate_basic_line_plots(dir + "ns_rew.jpg", etas, ns_rew, x_label = 'Algorithm', y_label = 'Average Cost, Normal State')
    generate_basic_line_plots(dir + "re_rew.jpg", etas, re_rew, x_label = 'Algorithm', y_label = 'Average Cost, Rare State')
