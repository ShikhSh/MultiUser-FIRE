# from constants import *
# # from utils import WORKING_DIR
# def gen_plot(obj):
#     gen_plot_rew(obj)
#     gen_plot_runningAvg(obj)

# """
# A generic function to create plots and save them at the provided path.
# """
# def gen_basic_plot(items_count, var, path, x_label = '', y_label = ''):
#         if items_count is None:
#             plt.plot(var,'.')
#         else:
#             for i in range(items_count):
#                 plt.plot(var[i],'.')
        
#         plt.ylabel(y_label,fontsize=15)
#         plt.xlabel(x_label,fontsize=15)
#         # plt.xticks([10000,20000,30000,40000,50000,60000,70000,80000],['10','20','30','40','50', '60', '70', '80'])
#         if RUNNING_ON_COLAB:
#             plt.show()
#         else:
#             plt.savefig(path)
#         plt.clf()
# def gen_plot_rew(obj, dir):
#     path = dir + "Reward.jpg"
#     gen_basic_plot(obj.numUsers, obj.Rewards, path, x_label = 'Reward', y_label = 'No. of Iterations, x10^3')
# def gen_plot_runningAvg(obj, dir):
#         path = dir + "RunningAvg.jpg"
#         gen_basic_plot(obj.numUsers, obj.runningAvg, path, x_label = 'Reward, Running Average', y_label = 'No. of Iterations, x10^3')

# # def gen_plot_rew(obj):
# #         for u in range(obj.numUsers):
# #             plt.plot(obj.Rewards[u],'.')
# #         plt.ylabel('Reward',fontsize=15)
# #         plt.xlabel('No. of Iterations, x10^3',fontsize=15)
# #         # plt.xticks([10000,20000,30000,40000,50000,60000,70000,80000],['10','20','30','40','50', '60', '70', '80'])
# #         if RUNNING_ON_COLAB:
# #             plt.show()
# #         else:
            
# #             name = WORKING_DIR + "Reward.jpg"
# #             plt.savefig(name)
# #         plt.clf()
        
# # def gen_plot_runningAvg(obj):
# #         #print('avg reward across time', np.mean(Reward))
# #         for u in range(obj.numUsers):
# #             plt.plot(obj.runningAvg[u])
# #         plt.ylabel('Reward, Running Average')
# #         plt.xlabel('No. of Iterations, 10^3')
# #         # plt.xticks([1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],['1', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'])
# #         if RUNNING_ON_COLAB:
# #             plt.show()
# #         else:
            
# #             name = WORKING_DIR + "RunningAvg.jpg"
# #             plt.savefig(name)
# #         plt.clf()


# def gen_online_plots(online_obj):
#     path = dir + "Online_Reward.jpg"
#     gen_basic_plot(None, online_obj.Reward_online, path, x_label = 'Online Reward', y_label = 'No. of Iterations, x10^3')
    
#     path = dir + "Online_Running_Avg.jpg"
#     gen_basic_plot(None, online_obj.runningAvg_online, path, x_label = 'Reward, Running Average', y_label = 'No. of Iterations, x10^3')
    
#     path = dir + "Online_NS_Rew.jpg"
#     gen_basic_plot(None, online_obj.NSreward_online, path, x_label = 'No. of Iterations, x10^3', y_label = 'Normal States')
    
#     path = dir + "Online_RS_Rew.jpg"
#     gen_basic_plot(None, online_obj.REreward_online, path, x_label = 'No. of Iterations, x10^3', y_label = 'Rare Events States')
    

#     print('avg reward across time', online_obj.mean_Reward_online)
    
#     print('mean RE reward', online_obj.mean_REreward_online)
#     # if online_obj.mean_REmigration_online > 0:
#     print(' mean RE migration', online_obj.mean_REmigration_online)
#     # else:
#     #     print("**NO RE MIGR COST**")
#     # if (online_obj.mean_REdelay_online) > 0:
#     print(' mean RE delay', (online_obj.mean_REdelay_online))
#     # else:
#     #     print("**NO RE DELAY COST**")
#     # if (online_obj.mean_REstorage_online) > 0:
#     print(' mean RE storage', (online_obj.mean_REstorage_online))
#     # else:
#     #     print("**NO RE STORAGE COST**")
#     # if (online_obj.mean_REcompDelay_online) > 0:
#     print(' mean RE Comp Cost:', (online_obj.mean_REcompDelay_online))
#     # else:
#     #     print("**NO RE COMP_DELAY COST**")
    
#     print('mean NS reward', (online_obj.mean_NSreward_online))
#     # if (online_obj.mean_NSmigration_online) > 0:
#     print(' mean NS migration', (online_obj.mean_NSmigration_online))
#     # else:
#     #     print("**NO NS MIGR COST**")
#     # if (online_obj.mean_NSdelay_online) > 0:
#     print(' mean NS delay', (online_obj.mean_NSdelay_online))
#     # else:
#     #     print("**NO NS DELAY COST**")
#     # if (online_obj.mean_NSstorage_online) > 0:
#     print(' mean NS storage', (online_obj.mean_NSstorage_online))
#     # else:
#     #     print("**NO NS STORAGE COST**")
#     # if (online_obj.mean_NScompDelay_online) > 0:
#     print(' mean RE Comp Cost:', (online_obj.mean_NScompDelay_online))
    
#     # plt.plot(online_obj.Reward_online,'.')
#     # if RUNNING_ON_COLAB:
#     #     plt.show()
#     # else:
#     #     name = WORKING_DIR + "Online_Reward.jpg"
#     #     plt.savefig(name)

#     # plt.plot(online_obj.runningAvg_online)
#     # plt.ylabel('Reward, Running Average')
#     # plt.xlabel('No. of Iterations, x10^3')
#     # #plt.xlabel('Price Pr, Po={}, Qo={}'.format(Po,qo))   
#     # plt.xticks([25000,50000,75000, 100000,125000,150000,175000,200000], ['25', '50', '75','100','125','150','175','200'])#,
#     # # plt.savefig(nameR, bbox_inches="tight")
#     # if RUNNING_ON_COLAB:
#     #     plt.show()
#     # else:
#     #     name = WORKING_DIR + "Online_Running_Avg.jpg"
#     #     plt.savefig(name)
#     # plt.clf()


#     # plt.plot(online_obj.NSreward_online)
#     # plt.ylabel('Normal States')
#     # # nameR=DIAG_DIRECTORY + 'Norm_St'
#     # # plt.savefig(nameR)
#     # if RUNNING_ON_COLAB:
#     #     plt.show()
#     # else:
#     #     name = WORKING_DIR + "Online_NS_Rew.jpg"
#     #     plt.savefig(name)
#     # plt.clf()


#     # plt.plot(online_obj.REreward_online)
#     # plt.ylabel('Rare Events States')
#     # # nameR=DIAG_DIRECTORY + 'Rare_ev_st'
#     # # plt.savefig(nameR)
#     # if RUNNING_ON_COLAB:
#     #     plt.show()
#     # else:
#     #     name = WORKING_DIR + "Online_RS_Rew.jpg"
#     #     plt.savefig(name)
#     # plt.clf()

#     # if RUNNING_ON_COLAB:
#     # print('avg reward across time', np.mean(online_obj.Reward_online))

#     # print('mean RE reward', mean(online_obj.REreward_online))
#     # if len(online_obj.REmigration_online) > 0:
#     #     print(' mean RE migration', mean(online_obj.REmigration_online))
#     # else:
#     #     print("**NO RE MIGR COST**")
#     # if len(online_obj.REdelay_online) > 0:
#     #     print(' mean RE delay', mean(online_obj.REdelay_online))
#     # else:
#     #     print("**NO RE DELAY COST**")
#     # if len(online_obj.REstorage_online) > 0:
#     #     print(' mean RE storage', mean(online_obj.REstorage_online))
#     # else:
#     #     print("**NO RE STORAGE COST**")
#     # if len(online_obj.REcompDelay_online) > 0:
#     #     print(' mean RE Comp Cost:', mean(online_obj.REcompDelay_online))
#     # else:
#     #     print("**NO RE COMP_DELAY COST**")
    

#     # print('mean NS reward', mean(online_obj.NSreward_online))
#     # if len(online_obj.NSmigration_online) > 0:
#     #     print(' mean NS migration', mean(online_obj.NSmigration_online))
#     # else:
#     #     print("**NO NS MIGR COST**")
#     # if len(online_obj.NSdelay_online) > 0:
#     #     print(' mean NS delay', mean(online_obj.NSdelay_online))
#     # else:
#     #     print("**NO NS DELAY COST**")
#     # if len(online_obj.NSstorage_online) > 0:
#     #     print(' mean NS storage', mean(online_obj.NSstorage_online))
#     # else:
#     #     print("**NO NS STORAGE COST**")
#     # if len(online_obj.NScompDelay_online) > 0:
#     #     print(' mean RE Comp Cost:', mean(online_obj.NScompDelay_online))
#     # else:
#     #     print("**NO RE COMP_DELAY COST**")






#     # else:
#     #     print('avg reward across time', np.mean(online_obj.Reward_online))

#     #     print('mean RE reward', mean(online_obj.REreward_online))
#     #     if len(online_obj.REmigration_online) > 0:
#     #         print(' mean RE migration', mean(online_obj.REmigration_online))
#     #     else:
#     #         print("**NO RE MIGR COST**")
#     #     if len(online_obj.REdelay_online) > 0:
#     #         print(' mean RE delay', mean(online_obj.REdelay_online))
#     #     else:
#     #         print("**NO RE DELAY COST**")
#     #     if len(online_obj.REstorage_online) > 0:
#     #         print(' mean RE storage', mean(online_obj.REstorage_online))
#     #     else:
#     #         print("**NO RE STORAGE COST**")
#     #     if len(online_obj.REcompDelay_online) > 0:
#     #         print(' mean RE Comp Cost:', mean(online_obj.REcompDelay_online))
#     #     else:
#     #         print("**NO RE COMP_DELAY COST**")
        

#     #     print('mean NS reward', mean(online_obj.NSreward_online))
#     #     if len(online_obj.NSmigration_online) > 0:
#     #         print(' mean NS migration', mean(online_obj.NSmigration_online))
#     #     else:
#     #         print("**NO NS MIGR COST**")
#     #     if len(online_obj.NSdelay_online) > 0:
#     #         print(' mean NS delay', mean(online_obj.NSdelay_online))
#     #     else:
#     #         print("**NO NS DELAY COST**")
#     #     if len(online_obj.NSstorage_online) > 0:
#     #         print(' mean NS storage', mean(online_obj.NSstorage_online))
#     #     else:
#     #         print("**NO NS STORAGE COST**")
#     #     if len(online_obj.NScompDelay_online) > 0:
#     #         print(' mean RE Comp Cost:', mean(online_obj.NScompDelay_online))
#     #     else:
#     #         print("**NO RE COMP_DELAY COST**")